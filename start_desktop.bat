@echo off
echo ========================================================
echo GURUKUL AI — DESKTOP LAUNCHER
echo ========================================================
echo Starting FastAPI Backend Server on port 8001...
start cmd /k "cd backend && python run_server.py"

echo Waiting 3 seconds for backend initialization...
timeout /t 3 /nobreak >nul

echo Starting Tauri Desktop App...
cd desktop
npm run tauri dev
