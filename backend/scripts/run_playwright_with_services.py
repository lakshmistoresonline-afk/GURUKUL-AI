import os
import sys
import time
import subprocess
import requests
from pathlib import Path

REPO_ROOT = Path(r"D:/GURUKUL")

def start_services():
    print("Starting FastAPI backend server...")
    backend_proc = subprocess.Popen([sys.executable, str(REPO_ROOT / "backend" / "src" / "main.py")], cwd=str(REPO_ROOT / "backend"))

    print("Starting Next.js frontend dev server...")
    frontend_proc = subprocess.Popen("npm run dev --prefix frontend-nextjs", shell=True)

    # Wait for health
    print("Waiting for backend and frontend health...")
    for _ in range(30):
        try:
            r = requests.get("http://localhost:8080/health", timeout=2)
            if r.status_code == 200:
                print("Backend is healthy!")
                break
        except:
            pass
        time.sleep(1)

    for _ in range(30):
        try:
            r = requests.get("http://localhost:3000", timeout=2)
            if r.status_code == 200:
                print("Frontend is healthy!")
                break
        except:
            pass
        time.sleep(1)

    return backend_proc, frontend_proc

def stop_services(backend_proc, frontend_proc):
    print("Stopping services...")
    try:
        backend_proc.terminate()
        backend_proc.wait(timeout=5)
    except:
        backend_proc.kill()

    try:
        frontend_proc.terminate()
        frontend_proc.wait(timeout=5)
    except:
        frontend_proc.kill()

if __name__ == "__main__":
    b_proc, f_proc = start_services()
    try:
        print("Running Playwright UAT script...")
        ret = subprocess.run([sys.executable, str(REPO_ROOT / "backend" / "scripts" / "run_playwright_uat.py")])
        sys.exit(ret.returncode)
    finally:
        stop_services(b_proc, f_proc)
