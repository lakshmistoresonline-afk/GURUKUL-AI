import asyncio
import os
import sys
import traceback

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from src.orchestrator.ai_orchestrator import AIOrchestrator


async def main():
    print("=" * 60)
    print("        GURUKUL AI PROVIDER HEALTH CHECK")
    print("=" * 60)

    try:
        orchestrator = AIOrchestrator()

        print(f"Provider instances: {len(orchestrator.providers)}")
        print(
            "Providers:",
            ", ".join(p.get_name() for p in orchestrator.providers)
        )
        print()

        # --------------------------------------------------
        # HEALTH CHECK
        # --------------------------------------------------

        print("Checking provider health...")
        print()

        health = await orchestrator.get_health_status()

        print(f"Health result type: {type(health).__name__}")
        print(f"Health providers returned: {len(health)}")
        print()

        # --------------------------------------------------
        # PRINT EVERY PROVIDER
        # --------------------------------------------------

        for provider in orchestrator.providers:

            name = provider.get_name()
            status = health.get(name, {"status": "missing"})

            print(f"Provider: {name}")
            print(f"  Enabled: {provider.is_enabled()}")
            print(f"  Status: {status.get('status', 'unknown')}")

            if status.get("error"):
                print(f"  Error: {status['error']}")

            # --------------------------------------------------
            # SIMPLE GENERATION
            # --------------------------------------------------

            if status.get("status") == "available":

                print("  Testing simple generation...")

                try:

                    result = await provider.generate(
                        "Respond with exactly: PASS"
                    )

                    if result and "PASS" in result.upper():
                        print("  Generation: PASS")
                    else:
                        print("  Generation: FAIL")
                        print(f"  Response: {result}")

                except Exception as exc:

                    print("  Generation: FAIL")
                    print(f"  Error: {exc}")

            print("-" * 60)

        print()
        print("=" * 60)
        print("HEALTH CHECK COMPLETE")
        print("=" * 60)

    except Exception as exc:

        print()
        print("=" * 60)
        print("HEALTH CHECK FAILED")
        print("=" * 60)
        print(f"Exception: {exc}")
        print()
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
