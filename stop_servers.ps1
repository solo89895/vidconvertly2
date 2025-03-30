# Stop FastDownloadLK Servers
Write-Host "============================================" -ForegroundColor Red
Write-Host "         FastDownloadLK Server Manager" -ForegroundColor Red
Write-Host "============================================" -ForegroundColor Red
Write-Host

# Step 1: Stop processes on ports 8000 and 8080
Write-Host "Step 1: Stopping servers on ports 8000 and 8080..." -ForegroundColor Yellow
$ports = @(8000, 8080)
foreach ($port in $ports) {
    $process = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($process) {
        Stop-Process -Id $process.OwningProcess -Force
        Write-Host "Stopped process on port $port" -ForegroundColor Green
    }
}

# Step 2: Stop any remaining Python and Node processes
Write-Host "`nStep 2: Cleaning up remaining processes..." -ForegroundColor Yellow
$processes = @("python", "node")
foreach ($proc in $processes) {
    Get-Process $proc -ErrorAction SilentlyContinue | ForEach-Object {
        Stop-Process -Id $_.Id -Force
        Write-Host "Stopped $proc process (PID: $($_.Id))" -ForegroundColor Green
    }
}

Write-Host "`n============================================" -ForegroundColor Red
Write-Host "         All Servers Stopped Successfully!" -ForegroundColor Red
Write-Host "============================================" -ForegroundColor Red
Write-Host "`nPress any key to close this window..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 