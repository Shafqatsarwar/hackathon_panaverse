@echo off
echo Starting Panaversity Assistant Local Development...

REM Start Backend
start "Backend API (Port 8000)" cmd /k "python -m uvicorn src.api.chat_api:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to init
timeout /t 3

REM Start Frontend
cd frontend
start "Next.js Frontend (Port 3000)" cmd /k "npm run dev"

echo.
echo Local environment started!
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000/docs
echo.
echo Press any key to exit this launcher (servers will keep running)...
pause
