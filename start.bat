@echo off
cd /d "%~dp0"
title Panaversity Assistant Launcher
color 0b

echo ========================================================
echo      Panaversity Student Assistant - Launcher
echo ========================================================
echo.

:: 1. Cleanup First
echo [INFO] Cleaning up old processes...
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM node.exe /T 2>nul
timeout /t 2 >nul

:: 2. Check for virtual environment
set "PYTHON_EXE=python"
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
    echo [INFO] Using Virtual Environment
) else (
    echo [INFO] Using System Python
)

:: 3. Check Frontend Dependencies
if not exist "frontend\node_modules" (
    echo [SETUP] Installing Frontend Dependencies...
    cd frontend
    call npm install
    cd ..
)

:: 4. Start Backend in new window
echo [START] Launching Backend API (Port 8000)...
start "Backend API - Port 8000" cmd /k "%PYTHON_EXE% src\api\chat_api.py"

:: Wait a bit for backend to start
timeout /t 3 >nul

:: 5. Start Frontend in new window
echo [START] Launching Frontend UI (Port 3000)...
cd frontend
start "Frontend UI - Port 3000" cmd /k "npm run dev"
cd ..

echo.
echo ========================================================
echo [SUCCESS] System Started!
echo.
echo Backend:  http://localhost:8000/api/status
echo Frontend: http://localhost:3000
echo.
echo Two windows have opened - check them for logs.
echo Use 'stop.bat' to stop everything.
echo ========================================================
echo.
pause
