import asyncio
import os
import sys

BACKEND_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, BACKEND_ROOT)

from src.orchestrator.ai_orchestrator import AIOrchestrator


async def main():
    print("PROVIDER HEALTH RESULTS")
    print("=" * 60)

    orchestrator = AIOrchestrator()

    for provider in orchestrator.providers:
        print()
        print("TESTING:", provider.get_name())

        try:
            enabled = provider.is_enabled()
            print("Enabled:", enabled)

            if not enabled:
                print("RESULT: DISABLED")
                continue

            print("Calling check_health()...")

            result = await provider.check_health()

            print("RESULT:", result)

        except Exception as exc:
            print("EXCEPTION:", repr(exc))

        print("-" * 60)


if __name__ == "__main__":
    asyncio.run(main())