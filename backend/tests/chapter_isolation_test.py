import asyncio
import os
import sys

BACKEND_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from src.jobs.job_engine import JobEngine
from src.orchestrator.ai_orchestrator import AIOrchestrator
from src.models.job import ChapterJob, JobStatus


async def main():
    print("CHAPTER ISOLATION TEST")
    print("=" * 60)

    engine = JobEngine(AIOrchestrator())
    await engine.init_db()

    student_id = "__TEST_STUDENT_ISOLATION__"

    # Clean previous test records.
    async with engine.AsyncSession() as session:
        from sqlalchemy import delete

        await session.execute(
            delete(ChapterJob).where(
                ChapterJob.student_id == student_id
            )
        )
        await session.commit()

    # Create the first dummy active job directly in the database.
    async with engine.AsyncSession() as session:
        job = ChapterJob(
            student_id=student_id,
            book_id="__TEST_BOOK__",
            chapter_id="CHAPTER_1",
            source_file="./storage/__test_chapter_1.pdf",
            source_file_hash="__TEST_HASH_1__",
            status=JobStatus.GENERATING,
        )

        session.add(job)
        await session.commit()

        print("FIRST ACTIVE JOB: CREATED")
        print("Chapter:", job.chapter_id)

    # Attempt to create a second active chapter.
    try:
        await engine.create_job(
            student_id=student_id,
            book_id="__TEST_BOOK__",
            chapter_id="CHAPTER_2",
            file_path="./storage/__test_chapter_2.pdf",
            file_hash="__TEST_HASH_2__",
        )

        print("RESULT: FAIL")
        print("A second active chapter job was allowed.")

    except RuntimeError as exc:
        if str(exc).startswith("ACTIVE_CHAPTER_EXISTS:"):
            print("SECOND ACTIVE JOB: CORRECTLY REJECTED")
            print("RESULT: PASS")
        else:
            print("RESULT: FAIL")
            print("Unexpected RuntimeError:", exc)

    except Exception as exc:
        print("RESULT: FAIL")
        print("Unexpected exception:", repr(exc))

    # Clean up test records.
    async with engine.AsyncSession() as session:
        from sqlalchemy import delete

        await session.execute(
            delete(ChapterJob).where(
                ChapterJob.student_id == student_id
            )
        )
        await session.commit()

    print("TEST RECORDS: CLEANED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
