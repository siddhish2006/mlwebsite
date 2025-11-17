@echo off
echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo Setup complete!
echo.
echo To run the app:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Run: python app.py
echo.
echo Or use: run_local.bat
echo ========================================


