@echo off
cd /d "%~dp0"
echo Starting Panaversity Assistant Local Development...

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not found in PATH.
    pause
    exit /b 1
)

REM Check if npm is available
call npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: npm is not found in PATH.
    pause
    exit /b 1
)

REM Start Backend
echo Starting Backend...
start "Backend API (Port 8000)" cmd /k "python -m uvicorn src.api.chat_api:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to init
timeout /t 5

REM Start Frontend
echo Starting Frontend...
cd frontend
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
)
start "Next.js Frontend (Port 3000)" cmd /k "npm run dev"

echo.
echo Local environment started!
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000/docs
echo.
echo Press any key to exit this launcher (servers will keep running)...
pause
