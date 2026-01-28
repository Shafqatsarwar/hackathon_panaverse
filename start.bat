@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
title Panaversity Assistant Launcher
color 0b

echo ========================================================
echo      Panaversity Student Assistant - Auto Launcher
echo ========================================================
echo.

:: 1. Cleanup First
echo [INFO] Ensuring ports are clear...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM node.exe /T >nul 2>&1
timeout /t 2 >nul

:: 2. Determine Python Interpreter
set "PYTHON_EXE=python"
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
    echo [INFO] Using Virtual Environment
) else (
    echo [INFO] Using System Python
)

:: 3. Frontend Setup
if not exist "frontend\node_modules" (
    echo [SETUP] Installing Frontend Dependencies...
    cd frontend
    call npm install
    cd ..
)

:: 4. Start Backend (New Window)
echo [START] Launching Backend API (Port 8000)...
set "PYTHONPATH=%CD%"
start "Backend API" cmd /k "%PYTHON_EXE% src/api/chat_api.py"

:: Delay for backend start
timeout /t 5 >nul

:: 5. Start Frontend (New Window)
echo [START] Launching Frontend UI (Port 3000)...
cd frontend
start "Next.js Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ========================================================
echo [SUCCESS] System Starting...
echo.
echo Backend:  http://localhost:8000/api/status
echo Frontend: http://localhost:3000
echo.
echo Use 'stop.bat' to stop everything.
echo ========================================================
pause
