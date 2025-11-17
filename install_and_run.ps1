# PowerShell script to install and run the Flask app

Write-Host "Step 1: Creating virtual environment..." -ForegroundColor Green
python -m venv venv

Write-Host "`nStep 2: Activating virtual environment..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

Write-Host "`nStep 3: Upgrading pip..." -ForegroundColor Green
python -m pip install --upgrade pip

Write-Host "`nStep 4: Installing all packages..." -ForegroundColor Green
pip install Flask==3.0.0
pip install flask-cors==4.0.0
pip install pandas==2.1.3
pip install numpy==1.26.2
pip install scikit-learn==1.3.2
pip install scipy==1.11.4
pip install matplotlib==3.8.2
pip install Werkzeug==3.0.1

Write-Host "`nStep 5: Verifying installation..." -ForegroundColor Green
python -c "import flask; import pandas; import sklearn; print('✓ All packages installed successfully!')"

Write-Host "`n" -NoNewline
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host "Setup Complete! Starting Flask app..." -ForegroundColor Green
Write-Host "Open your browser to: http://127.0.0.1:5000" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host "`n" -NoNewline

python app.py


