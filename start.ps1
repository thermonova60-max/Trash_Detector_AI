# TrashCollector AI - Simple Startup Script (PowerShell)
# Usage: .\start.ps1

$backendPath = Join-Path $PSScriptRoot "backend"
$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

Set-Location $backendPath
$env:PYTHONPATH = $backendPath

Write-Host ""
Write-Host "================================================"
Write-Host "  TrashCollector AI - Starting Server" -ForegroundColor Green
Write-Host "================================================"
Write-Host ""
Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Health: http://localhost:8000/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

& $venvPython -c "from main import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8000)"
