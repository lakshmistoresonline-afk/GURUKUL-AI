import os
import subprocess
import time
import asyncio
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from class5_final_forensic_runtime_auditor import audit_c01_deep_trace

async def main():
    print("Starting FastAPI backend on port 8080...")
    p1 = subprocess.Popen([sys.executable, "-m", "uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8080"], cwd=r"D:\GURUKUL\backend")

    print("Starting Next.js frontend on port 3000...")
    p2 = subprocess.Popen(["npm.cmd", "run", "dev"], cwd=r"D:\GURUKUL\frontend-nextjs")

    print("Waiting 10 seconds for servers to initialize...")
    await asyncio.sleep(10)

    try:
        await audit_c01_deep_trace()
    finally:
        print("Terminating servers...")
        p1.terminate()
        p2.terminate()
        p1.wait()
        p2.wait()

if __name__ == "__main__":
    asyncio.run(main())
