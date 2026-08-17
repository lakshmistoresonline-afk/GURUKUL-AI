import asyncio
import os
import sys

BACKEND_ROOT = os.getcwd()

if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from src.jobs.job_engine import JobEngine
from src.models.job import ChapterJob
from src.orchestrator.ai_orchestrator import AIOrchestrator
from sqlalchemy import select


async def main():
    print("=" * 70)
    print("GURUKUL - CHAPTER JOB DETAILS")
    print("=" * 70)

    engine = JobEngine(AIOrchestrator())
    await engine.init_db()

    async with engine.AsyncSession() as session:
        result = await session.execute(
            select(ChapterJob)
        )

        jobs = result.scalars().all()

        print("TOTAL JOBS:", len(jobs))
        print()

        for i, job in enumerate(jobs, 1):
            print("=" * 70)
            print("JOB", i)
            print("=" * 70)

            print("Job ID       :", job.job_id)
            print("Student      :", job.student_id)
            print("Book         :", job.book_id)
            print("Chapter      :", job.chapter_id)
            print("Status       :", job.status)
            print("Stage        :", job.current_stage)
            print("Progress     :", job.progress)
            print("Error        :", job.error)

            completed = job.completed_stages or {}

            print(
                "Completed    :",
                ", ".join(completed.keys())
                if completed else "NONE"
            )

            print()

    print("=" * 70)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
