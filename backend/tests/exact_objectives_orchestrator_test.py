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
    print("GURUKUL AI - EXACT OBJECTIVES ORCHESTRATOR TEST")
    print("=" * 70)

    orchestrator = AIOrchestrator()
    engine = JobEngine(orchestrator)

    await engine.init_db()

    async with engine.AsyncSession() as session:

        job = await session.get(ChapterJob, JOB_ID)

        if not job:
            print("ERROR: Job not found")
            return

        completed = dict(job.completed_stages or {})
        context = str(
            completed.get("source_digest", "")
        ).strip()

        print("JOB:", job.job_id)
        print("STATUS:", job.status)
        print("STAGE:", job.current_stage)
        print("CONTEXT LENGTH:", len(context))
        print()

        if not context:
            print("ERROR: source_digest missing")
            return

        prompt = (
            "You are generating content for ONE textbook chapter only.\n\n"
            "Use ONLY the supplied chapter-derived source context. "
            "Do not invent facts that are not supported by it.\n\n"
            f"CHAPTER CONTEXT:\n{context}\n\n"
            "TASK:\nGenerate learning objectives.\n"
        )

        print("PROMPT LENGTH:", len(prompt))
        print()

        print("ACTIVE PROVIDERS:")
        for provider in orchestrator.active_providers:
            print("  -", provider.get_name())

        print()
        print("=" * 70)
        print("CALLING EXACT ORCHESTRATOR.generate()")
        print("=" * 70)

        try:

            result = await orchestrator.generate(
                prompt,
                task_type="objectives",
            )

            print()
            print("RESULT:")
            print(result)

            print()
            print("SUCCESS:", result.get("success"))
            print("PROVIDER:", result.get("provider"))
            print("MODEL:", result.get("model"))
            print("DURATION:", result.get("duration"))

            print()
            print("ATTEMPTS:")

            for attempt in result.get("attempts", []):
                print("  PROVIDER:", attempt.get("provider"))
                print("  ERROR:", attempt.get("error"))
                print()

        except Exception as exc:

            print()
            print("ORCHESTRATOR EXCEPTION:")
            print(repr(exc))

    print()
    print("=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
