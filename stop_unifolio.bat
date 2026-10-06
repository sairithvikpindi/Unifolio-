@echo off
echo Stopping UniFolio server instances...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5000" ^| findstr "LISTENING"') do (
    taskkill /f /pid %%a >nul 2>&1
    echo [OK] Stopped process %%a on port 5000.
)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":80" ^| findstr "LISTENING"') do (
    taskkill /f /pid %%a >nul 2>&1
    echo [OK] Stopped process %%a on port 80.
)
echo.
echo UniFolio server is stopped.
pause
