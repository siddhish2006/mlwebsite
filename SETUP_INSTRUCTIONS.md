# Setup Instructions for Local Development

## Quick Start (Windows)

### Step 1: Create and Setup Virtual Environment
Run this command in your terminal (PowerShell or Command Prompt):
```bash
setup_venv.bat
```

This will:
- Create a virtual environment
- Install all required packages
- Set everything up for you

### Step 2: Run the Application
After setup, you can run the app using:
```bash
run_local.bat
```

Or manually:
```bash
venv\Scripts\activate
python app.py
```

## Manual Setup (Alternative)

If the batch file doesn't work, follow these steps:

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   ```bash
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```bash
   python app.py
   ```

## Fixing IDE Import Errors

If your IDE (VS Code, PyCharm, etc.) still shows import errors:

### VS Code:
1. Press `Ctrl+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose the interpreter from `venv\Scripts\python.exe`

### PyCharm:
1. Go to File → Settings → Project → Python Interpreter
2. Click the gear icon → Add
3. Select "Existing environment"
4. Browse to `venv\Scripts\python.exe`

## Verify Installation

To check if packages are installed correctly:
```bash
venv\Scripts\activate
python -c "import flask; import pandas; print('All packages installed!')"
```


