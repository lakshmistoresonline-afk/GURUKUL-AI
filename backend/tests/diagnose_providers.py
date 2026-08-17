import asyncio
import os
import sys

BACKEND_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from src.orchestrator.ai_orchestrator import AIOrchestrator


async def main():
    print("=" * 60)
    print("GURUKUL PROVIDER DIAGNOSTIC")
    print("=" * 60)

    orchestrator = AIOrchestrator()

    print("Provider count:", len(orchestrator.providers))
    print()

    for provider in orchestrator.providers:
        name = provider.get_name()

        print("PROVIDER:", name)

        try:
            enabled = provider.is_enabled()
            print("  Enabled:", enabled)
        except Exception as e:
            print("  Enabled check ERROR:", repr(e))
            print("-" * 60)
            continue

        if not enabled:
            print("  Status: DISABLED")
            print("-" * 60)
            continue

        try:
            result = await provider.check_health()
            print("  Health:", repr(result))
        except Exception as e:
            print("  Health ERROR:", repr(e))

        print("-" * 60)

    print()
    print("DIAGNOSTIC COMPLETE")


if __name__ == "__main__":
    asyncio.run(main())