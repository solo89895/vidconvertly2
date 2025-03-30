@echo off
title FastDownloadLK - Starting All Servers
color 0A

echo ============================================
echo         FastDownloadLK Server Manager
echo ============================================
echo.

:: Step 1: Check Python Installation
echo [Step 1/6] Checking Python Installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed! Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo Python check passed!
echo.

:: Step 2: Kill any existing Python processes
echo [Step 2/6] Cleaning up existing processes...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM node.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul
echo Cleanup complete!
echo.

:: Step 3: Setup Backend Environment
echo [Step 3/6] Setting up Backend Environment...
if not exist "backend\.venv" (
    echo Creating virtual environment...
    cd backend
    python -m venv .venv
    call .\.venv\Scripts\activate.bat
    echo Installing required packages...
    pip install fastapi uvicorn python-multipart yt-dlp requests python-dotenv aiohttp
    cd ..
) else (
    echo Virtual environment exists, updating packages...
    cd backend
    call .\.venv\Scripts\activate.bat
    pip install fastapi uvicorn python-multipart yt-dlp requests python-dotenv aiohttp
    cd ..
)
echo Backend environment setup complete!
echo.

:: Step 4: Check if ports are available
echo [Step 4/6] Checking port availability...
netstat -ano | find ":8000" >nul
if not errorlevel 1 (
    echo Warning: Port 8000 is in use. Attempting to free it...
    for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000"') do taskkill /F /PID %%a
    timeout /t 2 /nobreak >nul
)

netstat -ano | find ":8080" >nul
if not errorlevel 1 (
    echo Warning: Port 8080 is in use. Attempting to free it...
    for /f "tokens=5" %%a in ('netstat -aon ^| find ":8080"') do taskkill /F /PID %%a
    timeout /t 2 /nobreak >nul
)
echo Port check complete!
echo.

:: Step 5: Start Backend Server
echo [Step 5/6] Starting Backend Server...
cd backend
call .\.venv\Scripts\activate.bat
start cmd /k "title FastDownloadLK Backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
cd ..
echo Backend server started!
echo.

:: Step 6: Wait for Backend to Initialize
echo [Step 6/6] Waiting for Backend to initialize...
timeout /t 5 /nobreak >nul

:: Test backend connection
echo Testing backend connection...
curl -s http://localhost:8000/docs >nul
if errorlevel 1 (
    echo Error: Backend server is not responding! Please check the backend window for errors.
    pause
    exit /b 1
)
echo Backend connection successful!
echo.

:: Start Frontend Server
echo Starting Frontend Server...
start cmd /k "title FastDownloadLK Frontend && npm run dev"
echo Frontend server started!
echo.

echo ============================================
echo         All Servers Started Successfully!
echo ============================================
echo.
echo Frontend URL: http://localhost:8080
echo Backend URL: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo If you encounter any issues:
echo 1. Make sure both servers are running
echo 2. Check the browser console for errors
echo 3. Try refreshing the page
echo 4. Check the backend window for any error messages
echo.
echo Press any key to close this window...
pause >nul 