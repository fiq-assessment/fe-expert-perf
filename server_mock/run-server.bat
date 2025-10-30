@echo off
echo ====================================
echo FE Expert - Virtualized Logs API
echo ====================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [1/3] Python detected: 
python --version
echo.

:: Check if we're in the correct directory
if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found.
    echo Please run this script from the server_mock directory.
    pause
    exit /b 1
)

echo [2/3] Installing Python dependencies...
echo This may take a minute on first run...
echo.
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo [3/3] Starting FastAPI server...
echo.
echo ========================================
echo Server will be available at:
echo   http://localhost:4001
echo.
echo API Documentation:
echo   http://localhost:4001/docs
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

uvicorn app.main:app --reload --port 4001

