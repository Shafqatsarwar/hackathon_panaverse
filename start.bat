@echo off
cd /d "%~dp0"
title Panaversity Assistant Launcher
color 0b

echo ========================================================
echo      Panaversity Student Assistant - Auto Launcher
echo ========================================================
echo.

echo [INFO] Starting Panaversity Assistant...

:: Install Frontend Deps if missing (Simple check)
if not exist "frontend\node_modules" (
    echo [SETUP] Installing Frontend Dependencies...
    cd frontend
    call npm install
    cd ..
)

echo [1/2] Launching Backend Server (New Window)...
start "Backend API (Port 8000)" cmd /k "python -m uvicorn src.api.chat_api:app --reload --host 0.0.0.0 --port 8000"

echo [WAIT] Waiting for backend to initialize...
timeout /t 5 >nul

echo [2/2] Launching Frontend Interface (New Window)...
cd frontend
start "Next.js Frontend (Port 3000)" cmd /k "npm run dev"

echo.
echo ========================================================
echo [SUCCESS] System is running!
echo.
echo  - Frontend: http://localhost:3000
echo  - Backend:  http://localhost:8000
echo.
echo You can close this window now.
echo ========================================================
pause
