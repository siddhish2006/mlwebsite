# Deploy to Render - Simple Guide

## ✅ Everything is Configured!

Your app is ready to deploy on Render.

## Quick Deploy Steps

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### Step 2: Deploy on Render

1. Go to https://render.com
2. Sign up/Login with GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Select your `Aimlproject` repository

### Step 3: Configure Settings

Render will auto-detect settings from `render.yaml`, but verify:

- **Name:** `mlwebsite` (or your choice)
- **Region:** Choose closest to you
- **Branch:** `main`
- **Root Directory:** (leave empty)
- **Runtime:** Python 3 (should auto-detect)
- **Build Command:** (auto-filled from render.yaml)
- **Start Command:** (auto-filled from render.yaml)

### Step 4: Set Python Version (IMPORTANT!)

1. In the service settings, look for **"Python Version"** or **"Environment"**
2. Select **Python 3.12** (NOT 3.13!)
3. If you can't find it, add environment variable:
   - **Key:** `PYTHON_VERSION`
   - **Value:** `3.12.8`

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Wait for build to complete (5-10 minutes first time)
3. Your app will be live at: `https://mlwebsite.onrender.com`

## Configuration Files

- ✅ `render.yaml` - Render configuration (auto-detected)
- ✅ `runtime.txt` - Specifies Python 3.12.8
- ✅ `requirements.txt` - All dependencies
- ✅ `Procfile` - Start command (backup)

## Build Process

The build command will:
1. Upgrade pip, setuptools, wheel
2. Install numpy, scipy, scikit-learn first (with binary wheels)
3. Install remaining packages from requirements.txt

This ensures packages install correctly without building from source.

## Troubleshooting

**If build fails:**
- Make sure Python 3.12 is selected (not 3.13)
- Check build logs for specific errors
- Verify all files are committed and pushed

**If app doesn't start:**
- Check that gunicorn is in requirements.txt ✅
- Verify start command: `gunicorn app:app --bind 0.0.0.0:$PORT`

## Free Tier Notes

- Free instances spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- Perfect for testing and development!

That's it! Your app should deploy successfully on Render! 🚀

