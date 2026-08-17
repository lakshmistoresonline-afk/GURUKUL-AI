import asyncio
import os
import sys

BACKEND_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from sqlalchemy import select
from src.jobs.job_engine import JobEngine
from src.models.job import ChapterJob
from src.orchestrator.ai_orchestrator import AIOrchestrator
from src.config.app_config import settings

async def main():
    print("=" * 70)
    print("GURUKUL - CHAPTER JOB DATABASE DIAGNOSTIC")
    print("=" * 70)

    print("DATABASE URL:", settings.DATABASE_URL)

    engine = JobEngine(AIOrchestrator())
    await engine.init_db()

    async with engine.AsyncSession() as session:
        result = await session.execute(
            select(ChapterJob).order_by(
                ChapterJob.updated_at.desc()
            )
        )

        jobs = result.scalars().all()

        print("TOTAL JOBS:", len(jobs))
        print()

        if not jobs:
            print("NO CHAPTER JOBS FOUND.")
        else:
            for job in jobs[:20]:
                print("JOB ID:", job.job_id)
                print("STATUS:", job.status)
                print("STUDENT:", job.student_id)
                print("BOOK:", job.book_id)
                print("CHAPTER:", job.chapter_id)
                print("STAGE:", job.current_stage)
                print("PROGRESS:", job.progress)
                print("UPDATED:", job.updated_at)
                print("ERROR:", job.error)
                print("-" * 70)

asyncio.run(main())
