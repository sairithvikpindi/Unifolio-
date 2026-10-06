@echo off
:: Enable UniFolio to start automatically on Windows boot
set STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set TARGET_VBS=C:\Users\sai rithvik\.gemini\antigravity\scratch\unifolio\launch_silent.vbs

powershell -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%STARTUP_DIR%\UniFolio_AutoStart.lnk');$s.TargetPath='wscript.exe';$s.Arguments='\"%TARGET_VBS%\"';$s.WorkingDirectory='C:\Users\sai rithvik\.gemini\antigravity\scratch\unifolio';$s.Save()"

echo ========================================================
echo [SUCCESS] UniFolio is now set to start automatically 
echo whenever your Windows PC turns on!
echo ========================================================
echo.
pause
