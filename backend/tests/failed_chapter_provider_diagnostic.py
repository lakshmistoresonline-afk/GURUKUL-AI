import asyncio
import os
import sys

BACKEND_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from src.jobs.job_engine import JobEngine
from src.models.job import ChapterJob
from src.orchestrator.ai_orchestrator import AIOrchestrator


JOB_ID = "bfbd2b9d-0362-4bae-bf1f-130abe2af1a8"


async def main():
    print("=" * 70)
    print("GURUKUL AI - FAILED CHAPTER PROVIDER DIAGNOSTIC")
    print("=" * 70)

    orchestrator = AIOrchestrator()
    engine = JobEngine(orchestrator)

    await engine.init_db()

    async with engine.AsyncSession() as session:
        job = await session.get(ChapterJob, JOB_ID)

        if not job:
            print("ERROR: Job not found:", JOB_ID)
            return

        completed = dict(job.completed_stages or {})
        digest = str(completed.get("source_digest", "")).strip()

        print("Job:", job.job_id)
        print("Status:", job.status)
        print("Current stage:", job.current_stage)
        print("Source digest present:", bool(digest))
        print("Source digest length:", len(digest))
        print()

        if not digest:
            print("ERROR: source_digest is missing.")
            return

        prompt = (
            "You are generating content for ONE textbook chapter only.\n\n"
            "Use ONLY the supplied chapter-derived source context. "
            "Do not invent facts that are not supported by it.\n\n"
            "CHAPTER CONTEXT:\n"
            f"{digest}\n\n"
            "TASK:\n"
            "Generate learning objectives for this chapter."
        )

        print("Prompt length:", len(prompt))
        print()
        print("=" * 70)
        print("TESTING EACH ACTIVE PROVIDER")
        print("=" * 70)

        for provider in orchestrator.providers:

            name = provider.get_name()

            if not provider.is_enabled():
                print()
                print("PROVIDER:", name)
                print("RESULT: DISABLED")
                print("-" * 70)
                continue

            print()
            print("PROVIDER:", name)
            print("Enabled: True")

            try:
                result = await provider.generate(prompt)

                print("RESULT: SUCCESS")
                print("Response length:", len(str(result)))
                print("Response preview:")
                print(str(result)[:500])

            except Exception as exc:
                print("RESULT: FAILED")
                print("ERROR:", repr(exc))

            print("-" * 70)

    print()
    print("=" * 70)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
