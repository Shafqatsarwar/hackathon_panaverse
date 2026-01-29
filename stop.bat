@echo off
cd /d "%~dp0"
title Stopping Panaversity Assistant
color 0c

echo ========================================================
echo      Stopping Panaversity Student Assistant...
echo ========================================================
echo.

echo [1/3] Killing Python processes...
taskkill /F /IM python.exe /T 2>nul
if %errorlevel%==0 (
    echo Python processes stopped.
) else (
    echo No Python processes found.
)

echo [2/3] Killing Node.js processes...
taskkill /F /IM node.exe /T 2>nul
if %errorlevel%==0 (
    echo Node.js processes stopped.
) else (
    echo No Node.js processes found.
)

echo [3/3] Cleanup complete.
echo.
echo ========================================================
echo [SUCCESS] All processes stopped!
echo ========================================================
echo.
pause
