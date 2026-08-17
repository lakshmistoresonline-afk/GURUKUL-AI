import asyncio
import os
import sys
import traceback

BACKEND_ROOT = os.getcwd()

if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from src.orchestrator.ai_orchestrator import AIOrchestrator
from src.services.chapter_service import ChapterService


async def main():
    print("=" * 70)
    print("GURUKUL AI - EXACT QUIZ STRUCTURED TEST")
    print("=" * 70)

    orchestrator = AIOrchestrator()
    service = ChapterService(orchestrator)

    schema = service._get_schema_for_stage("quiz")

    print("Schema type:", schema.get("type"))
    print("Schema loaded: PASS")
    print()

    prompt = """
You are generating content for ONE Grade 5 textbook chapter only.

Generate exactly 5 multiple-choice questions suitable for the chapter.

Return ONLY structured JSON matching the supplied schema.
Do not return Markdown.
Do not return explanatory text outside the JSON.
"""

    print("Testing orchestrator structured failover...")
    print()

    try:
        result = await asyncio.wait_for(
            orchestrator.generate_structured(
                prompt,
                schema,
                task_type="quiz"
            ),
            timeout=180
        )

        print("SUCCESS:", result.get("success"))
        print("PROVIDER:", result.get("provider"))
        print("RESPONSE TYPE:", type(result.get("response")).__name__)
        print("RESPONSE:")
        print(str(result.get("response"))[:5000])

        if result.get("success"):
            print()
            print("=" * 70)
            print("EXACT QUIZ TEST: PASS")
            print("=" * 70)
        else:
            print()
            print("ERROR:", result.get("error"))
            print("ATTEMPTS:", result.get("attempts"))

    except Exception as exc:
        print()
        print("=" * 70)
        print("EXACT QUIZ TEST: FAILED")
        print("=" * 70)
        print(type(exc).__name__, str(exc))
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
