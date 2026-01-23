@echo off
REM Panaversity Student Assistant - Windows Startup Script

echo ================================================
echo Panaversity Student Assistant
echo ================================================
echo.

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and configure it.
    echo.
    pause
    exit /b 1
)

REM Check if credentials.json exists
if not exist credentials.json (
    echo WARNING: credentials.json not found!
    echo Please download it from Google Cloud Console.
    echo See SETUP.md for instructions.
    echo.
    pause
    exit /b 1
)

echo Starting Panaversity Student Assistant...
echo.

REM Run the assistant
python src/main.py start

pause
