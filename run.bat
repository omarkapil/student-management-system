@echo off
echo ================================
echo  Student Management System
echo  Helwan Int. Tech. University
echo ================================
echo.

:: Check if venv exists, create if not
if not exist ".venv" (
    echo [1/3] Creating virtual environment...
    python -m venv .venv
)

:: Activate venv
echo [2/3] Activating virtual environment...
call .venv\Scripts\activate.bat

:: Install dependencies
echo [3/3] Installing dependencies...
pip install -r requirements.txt --quiet

:: Run the app
echo.
echo Starting server at http://127.0.0.1:5000
echo Default login: admin@example.com / admin123
echo Press CTRL+C to stop.
echo.
cd backend
python app.py
