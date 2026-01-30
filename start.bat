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

:: 3. Start Odoo MCP Server (Optional background)
:: echo [START] Launching Odoo MCP Server...
:: start /B "Odoo MCP" %PYTHON_EXE% mcp/odoo_server.py

:: 4. Start Backend
echo [START] Launching Backend API (Port 8000)...
start "Backend API" cmd /k "%PYTHON_EXE% src/api/chat_api.py"

:: Wait for backend
timeout /t 5 >nul

:: 5. Start Frontend
echo [START] Launching Frontend UI (Port 3000)...
cd frontend
if not exist "node_modules" call npm install
start "Frontend UI" cmd /k "npm run dev"
cd ..

echo.
echo ========================================================
echo [SUCCESS] System Started!
echo.
echo Backend:  http://localhost:8000/api/status
echo Frontend: http://localhost:3000
echo.
echo Two windows have opened. Don't close them!
echo Press any key to stop everything.
echo ========================================================
pause

taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM node.exe /T 2>nul
echo [STOPPED]
