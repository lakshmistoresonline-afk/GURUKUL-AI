import uvicorn
import os
import sys
import subprocess
import socket
from pathlib import Path
from dotenv import load_dotenv

env_file = Path(__file__).resolve().parent / ".env"
if env_file.exists():
    load_dotenv(dotenv_path=env_file)

def kill_process_on_port(port: int):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return
        print(f"[PORT GUARDIAN] Port {port} is occupied. Clearing...")
        if sys.platform == 'win32':
            output = subprocess.check_output(f'netstat -ano | findstr :{port}', shell=True).decode()
            for line in output.strip().split('\n'):
                if 'LISTENING' in line:
                    pid = line.strip().split()[-1]
                    subprocess.run(f'taskkill /F /PID {pid}', shell=True, capture_output=True)
    except: pass

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    port = 8000
    kill_process_on_port(port)
    print(f"Starting Gurukul AI Backend on port {port}...")
    uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=True, log_level="info")
