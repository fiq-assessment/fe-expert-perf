#!/bin/bash

echo "===================================="
echo "FE Expert - Virtualized Logs API"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "[ERROR] Python 3 is not installed."
    echo "Please install Python 3.10+ from https://www.python.org/downloads/"
    exit 1
fi

echo "[1/3] Python detected:"
python3 --version
echo ""

# Check if we're in the correct directory
if [ ! -f "requirements.txt" ]; then
    echo "[ERROR] requirements.txt not found."
    echo "Please run this script from the server_mock directory."
    exit 1
fi

echo "[2/3] Installing Python dependencies..."
echo "This may take a minute on first run..."
echo ""
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies."
    exit 1
fi

echo ""
echo "[3/3] Starting FastAPI server..."
echo ""
echo "========================================"
echo "Server will be available at:"
echo "  http://localhost:4001"
echo ""
echo "API Documentation:"
echo "  http://localhost:4001/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

uvicorn app.main:app --reload --port 4001

