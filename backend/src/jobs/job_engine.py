import asyncio
import logging
from datetime import datetime
from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from ..config.app_config import settings
from ..models.job import Base, ChapterJob, JobStatus
from ..orchestrator.ai_orchestrator import AIOrchestrator
from ..services.chapter_service import ChapterService
from ..utils.pdf_utils import extract_pdf_text

logger = logging.getLogger(__name__)


class JobEngine:
    """Single-chapter job engine with per-student sequential enforcement."""

    _student_locks = {}
    _student_locks_guard = asyncio.Lock()

    def __init__(self, orchestrator: AIOrchestrator):
        self.engine = create_async_engine(settings.DATABASE_URL)
        self.AsyncSession = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        self.orchestrator = orchestrator
        self.chapter_service = ChapterService(orchestrator)

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def _get_student_lock(self, student_id: str) -> asyncio.Lock:
        async with self._student_locks_guard:
            lock = self._student_locks.get(student_id)
            if lock is None:
                lock = asyncio.Lock()
                self._student_locks[student_id] = lock
            return lock

    async def create_job(
        self,
        student_id: str,
        book_id: str,
        chapter_id: str,
        file_path: str,
        file_hash: str,
        class_name: Optional[str] = None,
        subject: Optional[str] = None,
    ) -> ChapterJob:
        """
        Create exactly one logical chapter job per source file.
        Implements TRUE source-level idempotency based on source_file_hash.
        """
        lock = await self._get_student_lock(student_id)

        async with lock:
            async with self.AsyncSession() as session:
                # 1. Sequential student check (one active job per student)
                active_job = await self._get_active_job(session, student_id)
                if active_job:
                    # If this is the SAME chapter, we can just return it
                    if active_job.source_file_hash == file_hash:
                        logger.info("ACTIVE_JOB_REUSED: job_id=%s chapter=%s", active_job.job_id, chapter_id)
                        return active_job

                    raise RuntimeError(
                        f"ACTIVE_CHAPTER_EXISTS:{active_job.job_id}:{active_job.chapter_id}"
                    )

                # 2. Universal idempotency check by hash
                existing_job = await self._find_latest_job_by_hash(session, file_hash)

                if existing_job:
                    status = existing_job.status

                    if status == JobStatus.COMPLETED:
                        logger.info("COMPLETED_JOB_REUSED: job_id=%s hash=%s", existing_job.job_id, file_hash)
                        return existing_job

                    if status in (JobStatus.FAILED, JobStatus.SKIPPED, JobStatus.INTERRUPTED):
                        # If it was SKIPPED (Index/Contents), we NEVER auto-retry.
                        if status == JobStatus.SKIPPED:
                            logger.info("PREVIOUS_SKIPPED_JOB_REUSED: %s", existing_job.job_id)
                            return existing_job

                        # If it was FAILED or INTERRUPTED, and we are here, it means a NEW upload request arrived.
                        # We will allow a NEW job to be created to attempt processing again.
                        logger.info("PREVIOUS_TERMINAL_JOB_FOUND: status=%s job_id=%s. Creating fresh attempt.", status.value, existing_job.job_id)

                    if status == JobStatus.RETRY_REQUIRED:
                        logger.info("RETRYABLE_JOB_RESTARTED: job_id=%s", existing_job.job_id)
                        # Re-trigger processing for the existing job
                        asyncio.create_task(self.process_job(existing_job.job_id))
                        return existing_job

                    # If it's somehow active but for a different student (sequential check missed it)
                    logger.info("ACTIVE_JOB_REUSED_CROSS_STUDENT: job_id=%s", existing_job.job_id)
                    return existing_job

                # 3. Create NEW job
                job = ChapterJob(
                    student_id=student_id,
                    book_id=book_id,
                    chapter_id=chapter_id,
                    class_name=class_name,
                    subject=subject,
                    source_file=file_path,
                    source_file_hash=file_hash,
                    status=JobStatus.UPLOADED,
                )

                session.add(job)
                await session.commit()
                await session.refresh(job)

                logger.info("NEW_JOB_CREATED: job_id=%s chapter=%s hash=%s", job.job_id, chapter_id, file_hash)
                asyncio.create_task(self.process_job(job.job_id))
                return job

    async def process_job(self, job_id: str):
        """Process one chapter through extraction, generation, validation and completion."""
        async with self.AsyncSession() as session:
            job = await session.get(ChapterJob, job_id)
            if not job:
                logger.error("Job %s not found", job_id)
                return

            try:
                completed = dict(job.completed_stages or {})

                # Stage 1: PDF extraction
                if "extraction" not in completed:
                    job.status = JobStatus.EXTRACTING
                    job.current_stage = "PDF_TEXT_EXTRACTION"
                    job.progress = 0.05
                    await session.commit()

                    text = extract_pdf_text(job.source_file)
                    if not text or not text.strip():
                        from ..services.chapter_service import SourceClassificationError
                        raise SourceClassificationError(
                            "PDF text extraction returned no usable text.",
                            "INVALID_PDF"
                        )

                    completed["extraction"] = text
                    job.completed_stages = completed
                    job.progress = 0.15
                    await session.commit()

                # Stage 2: sequential AI generation
                job.status = JobStatus.GENERATING
                await session.commit()

                try:
                    await asyncio.wait_for(
                        self.chapter_service.run_chapter_generation(session, job),
                        timeout=settings.CHAPTER_GENERATION_TIMEOUT
                    )
                except asyncio.TimeoutError:
                    logger.error("Job %s timed out during AI generation", job_id)
                    job.status = JobStatus.RETRY_REQUIRED
                    job.failure_category = "RETRYABLE_TIMEOUT"
                    job.error = f"TIMEOUT: Generation exceeded {settings.CHAPTER_GENERATION_TIMEOUT}s"
                    job.retry_count = (job.retry_count or 0) + 1
                    await session.commit()
                    return

            except Exception as exc:
                logger.exception("Job %s failed", job_id)

                # Classify failure
                from ..orchestrator.ai_orchestrator import AllProvidersUnavailableError
                from ..services.chapter_service import SourceClassificationError

                if isinstance(exc, AllProvidersUnavailableError):
                    job.status = JobStatus.PAUSED_PROVIDER_UNAVAILABLE
                    job.failure_category = "RETRYABLE_PROVIDER_ERROR"
                elif isinstance(exc, SourceClassificationError):
                    job.status = JobStatus.SKIPPED
                    job.failure_category = exc.category
                elif "VALIDATION" in str(exc).upper():
                    job.status = JobStatus.FAILED
                    job.failure_category = "STAGE_VALIDATION_ERROR"
                else:
                    job.status = JobStatus.FAILED
                    job.failure_category = "PERMANENT_ERROR"

                job.error = str(exc)
                await session.commit()

    async def _find_latest_job_by_hash(
        self,
        session: AsyncSession,
        file_hash: str,
    ) -> Optional[ChapterJob]:
        stmt = select(ChapterJob).where(
            ChapterJob.source_file_hash == file_hash
        ).order_by(ChapterJob.started_at.desc())
        result = await session.execute(stmt)
        return result.scalars().first()

    async def _get_active_job(
        self,
        session: AsyncSession,
        student_id: str,
    ) -> Optional[ChapterJob]:
        stmt = select(ChapterJob).where(
            and_(
                ChapterJob.student_id == student_id,
                ChapterJob.status.in_(
                    [
                        JobStatus.UPLOADED,
                        JobStatus.EXTRACTING,
                        JobStatus.GENERATING,
                        JobStatus.VALIDATING,
                        JobStatus.VALIDATING_OUTPUT
                    ]
                ),
            )
        )
        result = await session.execute(stmt)
        return result.scalars().first()
