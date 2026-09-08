import uvicorn
import logging
import os
import sys
import socket
import subprocess
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .presentation.routes import auth_routes, system_routes, student_routes
from .data.repositories.database.db_config import init_db

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

def kill_process_on_port(port: int):
    """
    Finds and kills any process using the specified port (Windows specific logic).
    """
    try:
        if sys.platform == 'win32':
            # Check for listeners multiple times to ensure port is really clear
            for attempt in range(3):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    if s.connect_ex(('127.0.0.1', port)) != 0:
                        return # Port is free

                print(f"[PORT GUARDIAN] Port {port} is occupied (Attempt {attempt+1}). Clearing...")

                output = subprocess.check_output(f'netstat -ano | findstr :{port}', shell=True).decode()
                pids = set()
                for line in output.strip().split('\n'):
                    if 'LISTENING' in line:
                        parts = line.strip().split()
                        if len(parts) > 0:
                            pid = parts[-1]
                            if int(pid) > 0: pids.add(pid)

                for pid in pids:
                    print(f"[PORT GUARDIAN] Killing process {pid} occupying port {port}...")
                    subprocess.run(f'taskkill /F /PID {pid}', shell=True, capture_output=True)

                time.sleep(2) # Give OS time to release socket

        else:
            subprocess.run(f'fuser -k {port}/tcp', shell=True, capture_output=True)
            time.sleep(1)

    except Exception as e:
        print(f"[PORT GUARDIAN] Warning: Could not auto-clear port {port}: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await init_db()
    yield
    # Shutdown logic (if any)

app = FastAPI(title="GURUKUL V60 API", lifespan=lifespan, debug=DEBUG)

# Configure CORS - Move to earliest possible position
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001", "http://0.0.0.0:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(system_routes.router)
app.include_router(student_routes.router)

if __name__ == "__main__":
    port = 8000
    kill_process_on_port(port)
    uvicorn.run(app, host="0.0.0.0", port=port)
