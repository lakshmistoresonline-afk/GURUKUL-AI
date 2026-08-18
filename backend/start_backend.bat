@echo off
cd /d %~dp0
set PYTHONPATH=.
python -m uvicorn src.main:app --host 127.0.0.1 --port 8001
