# PowerShell Installation Script for Coffee Shop Barista Agent

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Coffee Shop Barista Agent Setup" -ForegroundColor Cyan
Write-Host "  Day 2 - Murf AI Voice Agent Challenge" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running from correct directory
if (-not (Test-Path ".\backend") -or -not (Test-Path ".\frontend")) {
    Write-Host "ERROR: Please run this script from the project root directory!" -ForegroundColor Red
    Write-Host "The directory should contain 'backend' and 'frontend' folders." -ForegroundColor Red
    exit 1
}

# Function to check if a command exists
function Test-CommandExists {
    param($command)
    $null = Get-Command $command -ErrorAction SilentlyContinue
    return $?
}

Write-Host "Step 1: Checking prerequisites..." -ForegroundColor Yellow
Write-Host ""

# Check for Python
$pythonInstalled = Test-CommandExists python
if ($pythonInstalled) {
    $pythonVersion = python --version
    Write-Host "✓ Python is installed: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python is NOT installed" -ForegroundColor Red
    Write-Host "  Please install Python 3.9+ from https://www.python.org/" -ForegroundColor Red
    $missingTools = $true
}

# Check for uv
$uvInstalled = Test-CommandExists uv
if ($uvInstalled) {
    Write-Host "✓ uv is installed" -ForegroundColor Green
} else {
    Write-Host "✗ uv is NOT installed" -ForegroundColor Red
    Write-Host "  Install with: powershell -c `"irm https://astral.sh/uv/install.ps1 | iex`"" -ForegroundColor Yellow
    $missingTools = $true
}

# Check for Node.js
$nodeInstalled = Test-CommandExists node
if ($nodeInstalled) {
    $nodeVersion = node --version
    Write-Host "✓ Node.js is installed: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Node.js is NOT installed" -ForegroundColor Red
    Write-Host "  Please install Node.js 18+ from https://nodejs.org/" -ForegroundColor Red
    $missingTools = $true
}

# Check for pnpm
$pnpmInstalled = Test-CommandExists pnpm
if ($pnpmInstalled) {
    Write-Host "✓ pnpm is installed" -ForegroundColor Green
} else {
    Write-Host "✗ pnpm is NOT installed" -ForegroundColor Red
    Write-Host "  Install with: npm install -g pnpm" -ForegroundColor Yellow
    $missingTools = $true
}

# Check for LiveKit
$livekitInstalled = Test-CommandExists livekit-server
if ($livekitInstalled) {
    Write-Host "✓ LiveKit is installed" -ForegroundColor Green
} else {
    Write-Host "✗ LiveKit is NOT installed" -ForegroundColor Red
    Write-Host "  Download from: https://github.com/livekit/livekit/releases" -ForegroundColor Yellow
    $missingTools = $true
}

Write-Host ""

if ($missingTools) {
    Write-Host "Please install missing tools and run this script again." -ForegroundColor Red
    Write-Host "See SETUP_GUIDE.md for detailed installation instructions." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "Step 2: Installing backend dependencies..." -ForegroundColor Yellow
Write-Host ""

Push-Location backend

Write-Host "Running: uv sync" -ForegroundColor Cyan
uv sync

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install backend dependencies" -ForegroundColor Red
    Pop-Location
    exit 1
}

Write-Host "✓ Backend dependencies installed" -ForegroundColor Green
Write-Host ""

Write-Host "Step 3: Downloading required models..." -ForegroundColor Yellow
Write-Host ""

Write-Host "Running: uv run python src/agent.py download-files" -ForegroundColor Cyan
uv run python src/agent.py download-files

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to download models" -ForegroundColor Red
    Pop-Location
    exit 1
}

Write-Host "✓ Models downloaded" -ForegroundColor Green
Write-Host ""

Pop-Location

Write-Host "Step 4: Installing frontend dependencies..." -ForegroundColor Yellow
Write-Host ""

Push-Location frontend

Write-Host "Running: pnpm install" -ForegroundColor Cyan
pnpm install

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install frontend dependencies" -ForegroundColor Red
    Pop-Location
    exit 1
}

Write-Host "✓ Frontend dependencies installed" -ForegroundColor Green
Write-Host ""

Pop-Location

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Installation Complete! ✓" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your Coffee Shop Barista Agent is ready!" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the application:" -ForegroundColor Yellow
Write-Host "  1. Run: .\start_app.ps1" -ForegroundColor White
Write-Host "  2. Open browser to: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "For manual start, see QUICKSTART.md" -ForegroundColor Gray
Write-Host ""
Write-Host "Environment files:" -ForegroundColor Yellow
Write-Host "  - backend\.env.local (API keys configured)" -ForegroundColor White
Write-Host "  - frontend\.env.local (LiveKit configured)" -ForegroundColor White
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Yellow
Write-Host "  - DAY2_COMPLETE.md - Task completion summary" -ForegroundColor White
Write-Host "  - SETUP_GUIDE.md - Detailed setup guide" -ForegroundColor White
Write-Host "  - ADVANCED_FEATURES.md - HTML visualization docs" -ForegroundColor White
Write-Host "  - QUICKSTART.md - Quick reference" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
