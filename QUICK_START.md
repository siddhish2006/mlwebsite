# Quick Start Guide

## Method 1: PowerShell (Recommended)

1. Open PowerShell in this folder
2. Run:
   ```powershell
   .\install_and_run.ps1
   ```

If you get an execution policy error, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Method 2: Command Prompt (Manual Steps)

Open Command Prompt and run these commands **one by one**:

```cmd
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install Flask flask-cors pandas numpy scikit-learn scipy matplotlib Werkzeug
python app.py
```

## Method 3: Direct Install (No Virtual Environment)

If virtual environment is causing issues, install directly:

```cmd
pip install Flask flask-cors pandas numpy scikit-learn scipy matplotlib Werkzeug
python app.py
```

## Fix IDE Import Errors

### VS Code:
1. Press `Ctrl+Shift+P`
2. Type: `Python: Select Interpreter`
3. Choose: `.\venv\Scripts\python.exe` (if using venv)
   OR your system Python: `Python 3.13.6`

### If still not working:
1. Close VS Code
2. Open VS Code from the project folder
3. VS Code should auto-detect the Python interpreter

## Troubleshooting

**Error: "python is not recognized"**
- Use `py` instead of `python` (Windows)
- Or add Python to PATH

**Error: "pip is not recognized"**
- Use `python -m pip` instead of `pip`

**Error: "ModuleNotFoundError"**
- Make sure you activated the virtual environment: `venv\Scripts\activate`
- Or install packages globally: `pip install -r requirements.txt`


