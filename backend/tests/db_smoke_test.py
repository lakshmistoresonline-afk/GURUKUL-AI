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


async def main():
    print("DATABASE SMOKE TEST")
    print("=" * 50)

    engine = JobEngine(AIOrchestrator())

    await engine.init_db()

    print("DATABASE INIT: PASS")
    print("DATABASE URL:", engine.engine.url)


if __name__ == "__main__":
    asyncio.run(main())