@echo off
title UniFolio - Academic Project Portfolio System
cd /d "%~dp0"

for /f "tokens=*" %%i in ('powershell -NoProfile -Command "(Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notmatch 'Loopback|vEthernet|WSL' -and $_.IPAddress -notlike '169.254*' } | Select-Object -First 1 -ExpandProperty IPAddress)"') do set LOCAL_IP=%%i
if "%LOCAL_IP%"=="" set LOCAL_IP=127.0.0.1

echo ========================================================
echo   UniFolio - Academic Project Portfolio System
echo   Real-Time CO-PO Mapping & Analytics (Phase 1)
echo ========================================================
echo.
echo Starting UniFolio Server...
echo Local PC Link:       http://127.0.0.1:5000
echo Mobile / Wi-Fi Link: http://%LOCAL_IP%:5000
echo.

:: Automatically open default browser after 2 seconds in background
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:5000"

:: Start Python Flask application
python app.py

pause
