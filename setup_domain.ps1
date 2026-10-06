# UniFolio PowerShell Domain Setup Script
# Run in Administrator PowerShell to map unifolio.in -> 127.0.0.1

$hostsPath = "$env:WINDIR\System32\drivers\etc\hosts"

Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "UniFolio Local Domain Setup (unifolio.in)" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan

$content = Get-Content $hostsPath -Raw
if ($content -match "unifolio\.in") {
    Write-Host "[INFO] unifolio.in is already mapped in $hostsPath" -ForegroundColor Yellow
} else {
    try {
        Add-Content -Path $hostsPath -Value "`n127.0.0.1 unifolio.in" -ErrorAction Stop
        Write-Host "[SUCCESS] Added '127.0.0.1 unifolio.in' to hosts file." -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Could not write to hosts file. Please run PowerShell as Administrator." -ForegroundColor Red
        Exit
    }
}

# Flush DNS
Clear-DnsClientCache
Write-Host "[SUCCESS] Flushed DNS Cache." -ForegroundColor Green
Write-Host ""
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "UniFolio is now accessible at:" -ForegroundColor Green
Write-Host "http://unifolio.in:5000" -ForegroundColor Yellow
Write-Host "=======================================================" -ForegroundColor Cyan
