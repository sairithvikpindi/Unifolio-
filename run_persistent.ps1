$port5000 = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | Where-Object { $_.State -eq 'Listen' }
if (-not $port5000) {
    Set-Location "C:\Users\sai rithvik\.gemini\antigravity\scratch\unifolio"
    Start-Process -FilePath "python.exe" -ArgumentList "app.py" -WorkingDirectory "C:\Users\sai rithvik\.gemini\antigravity\scratch\unifolio" -WindowStyle Hidden
}
