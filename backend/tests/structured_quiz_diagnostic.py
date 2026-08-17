import asyncio
import os
import sys
import traceback

BACKEND_ROOT = os.getcwd()

if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from src.orchestrator.ai_orchestrator import AIOrchestrator


async def main():
    print("=" * 70)
    print("GURUKUL AI - STRUCTURED OUTPUT DIAGNOSTIC")
    print("=" * 70)

    try:
        orchestrator = AIOrchestrator()

        print("Provider count:", len(orchestrator.providers))
        print("Active providers:")
        for p in orchestrator.active_providers:
            print(" -", p.get_name())

        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "options": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "correctAnswer": {"type": "string"},
                    "explanation": {"type": "string"}
                },
                "required": [
                    "question",
                    "options",
                    "correctAnswer"
                ]
            }
        }

        prompt = """
Generate exactly TWO simple Grade 5 English multiple-choice questions.

Return ONLY valid JSON.
Do not use Markdown.
Do not add explanations outside the JSON.
"""

        print()
        print("TEST PROMPT READY")
        print("Schema READY")
        print()

        for provider in orchestrator.active_providers:

            name = provider.get_name()

            print("=" * 70)
            print("TESTING:", name)
            print("=" * 70)

            try:
                print("Calling generate_structured()...")

                result = await asyncio.wait_for(
                    provider.generate_structured(
                        prompt,
                        schema
                    ),
                    timeout=120
                )

                print("RESULT: SUCCESS")
                print("TYPE:", type(result).__name__)
                print("VALUE:")
                print(str(result)[:2000])

            except Exception as exc:

                print("RESULT: FAILED")
                print("TYPE:", type(exc).__name__)
                print("ERROR:", str(exc))
                traceback.print_exc()

            print()

        print("=" * 70)
        print("DIAGNOSTIC COMPLETE")
        print("=" * 70)

    except Exception as exc:
        print()
        print("DIAGNOSTIC SCRIPT FAILURE")
        print("TYPE:", type(exc).__name__)
        print("ERROR:", str(exc))
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
