@echo off
echo Starting Panaversity Student Assistant - Full Stack Demo...

:: 1. Start Backend API (FastAPI) in a new window
echo Launching Backend API...
start "Backend API (Port 8000)" cmd /k "python -m uvicorn src.api.chat_api:app --reload --host 0.0.0.0 --port 8000"

:: 2. Wait a moment for backend to initialize
timeout /t 5

:: 3. Start Frontend (Next.js) in a new window
echo Launching Frontend...
cd frontend
start "Frontend (Port 3000)" cmd /k "npm run dev"

echo.
echo ========================================================
echo  All systems launching! 
echo  Please wait for the Frontend window to show:
echo  "Ready in xxxxms"
echo.
echo  Then open: http://localhost:3000
echo ========================================================
pause
