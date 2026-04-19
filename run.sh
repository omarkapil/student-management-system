#!/bin/bash
echo "================================"
echo " Student Management System"
echo " Helwan Int. Tech. University"
echo "================================"

# Create venv if missing
if [ ! -d ".venv" ]; then
    echo "[1/3] Creating virtual environment..."
    python3 -m venv .venv
fi

echo "[2/3] Activating virtual environment..."
source .venv/bin/activate

echo "[3/3] Installing dependencies..."
pip install -r requirements.txt -q

echo ""
echo "Starting server at http://127.0.0.1:5000"
echo "Default login: admin@example.com / admin123"
echo "Press CTRL+C to stop."
echo ""
cd backend
python app.py
