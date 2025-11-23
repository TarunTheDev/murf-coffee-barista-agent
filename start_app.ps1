# PowerShell script to start all services for the Coffee Shop Barista Agent

Write-Host "Starting Coffee Shop Barista Voice Agent..." -ForegroundColor Green
Write-Host ""

# Start LiveKit Server
Write-Host "Starting LiveKit Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "livekit-server --dev"

# Wait a moment for LiveKit to start
Start-Sleep -Seconds 3

# Start Backend Agent
Write-Host "Starting Backend Agent..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; uv run python src/agent.py dev"

# Wait a moment for backend to initialize
Start-Sleep -Seconds 3

# Start Frontend
Write-Host "Starting Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; pnpm dev"

Write-Host ""
Write-Host "All services are starting up!" -ForegroundColor Green
Write-Host "Please wait a moment for all services to initialize." -ForegroundColor Green
Write-Host ""
Write-Host "Once ready, open your browser to: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit this script (services will continue running)..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
