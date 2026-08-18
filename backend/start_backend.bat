@echo off
cd /d %~dp0
set PYTHONPATH=.
python -m uvicorn src.main:app --host 0.0.0.0 --port 8001
