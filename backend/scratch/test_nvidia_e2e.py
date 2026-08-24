import sys
import asyncio

sys.path.insert(0, "backend")

from src.orchestrator.ai_orchestrator import AIOrchestrator


async def main():
    orchestrator = AIOrchestrator()

    result = await orchestrator.generate(
        "Reply with exactly: NVIDIA ROUTER WORKING",
        task_type="complex",
    )

    print("SUCCESS:", result.get("success"))
    print("PROVIDER:", result.get("provider"))
    print("MODEL:", result.get("model"))
    print("RESPONSE:", result.get("response"))
    print("ATTEMPTS:", result.get("attempts"))


if __name__ == "__main__":
    asyncio.run(main())
