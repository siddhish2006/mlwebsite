@echo off
echo Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found! Running setup_venv.bat first...
    call setup_venv.bat
    call venv\Scripts\activate.bat
)

echo.
echo Starting Flask application...
echo Open your browser and go to: http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

