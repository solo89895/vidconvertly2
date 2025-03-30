# Start FastDownloadLK Servers
Write-Host "============================================" -ForegroundColor Green
Write-Host "         FastDownloadLK Server Manager" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host

# Get local IP address
$localIP = (Get-NetIPAddress | Where-Object {$_.AddressFamily -eq "IPv4" -and $_.PrefixOrigin -eq "Dhcp"}).IPAddress
Write-Host "Your local IP address: $localIP" -ForegroundColor Cyan
Write-Host

# Step 1: Start Backend Server
Write-Host "Step 1: Starting Backend Server..." -ForegroundColor Yellow
Set-Location backend
.\.venv\Scripts\activate
Start-Process powershell -ArgumentList "-NoExit", "-Command", "uvicorn main:app --reload --host 0.0.0.0 --port 8000"
Set-Location ..

# Wait for backend to initialize
Write-Host "Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Step 2: Start Frontend Server
Write-Host "Step 2: Starting Frontend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev -- --host"

Write-Host "`n============================================" -ForegroundColor Green
Write-Host "         All Servers Started Successfully!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host "`nAccess URLs:"
Write-Host "`nFrom your PC:"
Write-Host "Frontend: http://localhost:8080"
Write-Host "Backend: http://localhost:8000"
Write-Host "`nFrom your phone (same WiFi network):"
Write-Host "Frontend: http://$localIP`:8080"
Write-Host "Backend: http://$localIP`:8000"
Write-Host "`nAPI Documentation:"
Write-Host "PC: http://localhost:8000/docs"
Write-Host "Phone: http://$localIP`:8000/docs"
Write-Host "`nTo access from your phone:"
Write-Host "1. Make sure your phone is connected to the same WiFi network"
Write-Host "2. Open the Frontend URL in your phone's browser"
Write-Host "`nPress any key to close this window..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 