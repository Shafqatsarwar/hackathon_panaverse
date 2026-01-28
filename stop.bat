@echo off
cd /d "%~dp0"
echo ========================================================
echo      Stopping Panaversity Student Assistant...
echo ========================================================

echo [1/4] Killing Python processes (Forcefully)...
taskkill /F /IM python.exe /T >nul 2>&1

echo [2/4] Killing Node.js processes (Forcefully)...
taskkill /F /IM node.exe /T >nul 2>&1

echo [3/4] Ensuring ports 8000 and 3000 are free...
powershell -Command "Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }"
powershell -Command "Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }"

echo [4/4] Cleanup complete.
echo.
echo [SUCCESS] System stopped.
echo ========================================================
pause
