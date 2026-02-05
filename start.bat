@echo off
REM TrashCollector AI - Simple Startup Script
REM Just run: start.bat from the project root

cd /d "%~dp0\backend"
set PYTHONPATH=%cd%

echo.
echo ================================================
echo   TrashCollector AI - Starting Server
echo ================================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8000 (served from backend)
echo API: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo.

"%~dp0\.venv\Scripts\python.exe" -c "from main import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8000)"

pause
