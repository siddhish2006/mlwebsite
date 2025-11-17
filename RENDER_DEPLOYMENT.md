# Render Deployment Fix Guide

## The Problem
Render is trying to build packages from source (scipy/scikit-learn) which fails because:
- Python 3.13 might be selected (newer, fewer pre-built wheels)
- Build tools (ninja, C compilers) may be missing or failing

## Solutions Applied

### 1. Updated Package Versions
- Using latest versions with better Python 3.12/3.13 wheel support
- Updated scikit-learn to 1.5.1 and scipy to 1.13.1

### 2. Build Command Optimization
- Upgrades pip, setuptools, wheel first
- Uses `--prefer-binary` to prefer pre-built wheels
- Uses `--no-cache-dir` to avoid cache issues

### 3. Python Version
- `runtime.txt` specifies Python 3.12.8

## Important: Set Python Version in Render Dashboard

**CRITICAL STEP:** You MUST set the Python version in Render dashboard:

1. Go to your Render dashboard
2. Click on your `mlwebsite` service
3. Go to **Settings** tab
4. Scroll to **Environment** section
5. Find **Python Version** dropdown
6. **Select Python 3.12** (NOT 3.13)
7. Click **Save Changes**
8. Render will automatically redeploy

## If Build Still Fails

### Option A: Use Python 3.11 (Most Stable)
In Render dashboard, set Python version to **3.11.x** and update requirements.txt:
```
scikit-learn==1.3.2
scipy==1.11.4
```

### Option B: Check Build Logs
Look for which specific package is failing and we can pin an older version.

### Option C: Use Render's Buildpack
Render should auto-detect Python, but you can explicitly set it in dashboard settings.

## Current Configuration

- **Python**: 3.12.8 (via runtime.txt)
- **Build Command**: `pip install --upgrade pip setuptools wheel && pip install --prefer-binary --no-cache-dir -r requirements.txt`
- **Start Command**: `gunicorn app:app`

## After Setting Python Version

1. Commit and push your changes:
   ```bash
   git add .
   git commit -m "Fix Render deployment - update packages and build config"
   git push origin main
   ```

2. Render will auto-deploy
3. Check the build logs - it should succeed now!

