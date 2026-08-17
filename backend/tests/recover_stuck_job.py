import asyncio
import sys

from src.jobs.job_engine import JobEngine
from src.models.job import ChapterJob, JobStatus
from src.orchestrator.ai_orchestrator import AIOrchestrator


JOB_ID = sys.argv[1] if len(sys.argv) > 1 else None

if not JOB_ID:
    raise SystemExit("Usage: python -m tests.recover_stuck_job JOB_ID")


async def main():
    engine = JobEngine(AIOrchestrator())
    await engine.init_db()

    async with engine.AsyncSession() as session:
        job = await session.get(ChapterJob, JOB_ID)

        if not job:
            raise SystemExit(f"JOB NOT FOUND: {JOB_ID}")

        print("JOB:", job.job_id)
        print("STATUS:", job.status)
        print("STAGE:", job.current_stage)
        print("PROGRESS:", job.progress)
        print("CHAPTER:", job.chapter_id)
        print("UPDATED:", job.updated_at)

        if job.status not in {
            JobStatus.UPLOADED,
            JobStatus.EXTRACTING,
            JobStatus.GENERATING,
            JobStatus.VALIDATING,
        }:
            raise SystemExit(
                f"JOB IS NOT AN ACTIVE JOB: {job.status}"
            )

        job.status = JobStatus.RETRY_REQUIRED
        job.error = (
            "Recovered from stale active job at "
            f"{job.current_stage}; safe batch retry."
        )
        job.retry_count = (job.retry_count or 0) + 1

        await session.commit()

        print()
        print("RECOVERY: PASS")
        print("NEW STATUS:", job.status)
        print("RETRY COUNT:", job.retry_count)


asyncio.run(main())