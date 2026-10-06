@echo off
:: UniFolio Local Domain Setup Script (Windows)
:: Maps unifolio.in to 127.0.0.1 in C:\Windows\System32\drivers\etc\hosts

echo =======================================================
echo UniFolio Local Domain Configurator (unifolio.in)
echo =======================================================
echo.

:: Check for administrative privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Running with Administrator permissions.
) else (
    echo [ERROR] This script requires Administrator privileges.
    echo Please right-click this file and select 'Run as administrator'.
    echo.
    pause
    exit /b 1
)

set HOSTS_FILE=%WINDIR%\System32\drivers\etc\hosts

:: Check if unifolio.in is already present
findstr /i "unifolio.in" "%HOSTS_FILE%" >nul
if %errorLevel% == 0 (
    echo [INFO] unifolio.in is already mapped in your hosts file!
) else (
    echo. >> "%HOSTS_FILE%"
    echo 127.0.0.1 unifolio.in >> "%HOSTS_FILE%"
    echo [SUCCESS] Added '127.0.0.1 unifolio.in' to %HOSTS_FILE%
)

:: Flush DNS cache
ipconfig /flushdns >nul
echo [SUCCESS] Flushed DNS Resolver Cache.
echo.
echo =======================================================
echo You can now access UniFolio in your browser at:
echo http://unifolio.in:5000
echo =======================================================
echo.
pause
