# How to Force Python 3.12 in Render

Render is using Python 3.13.4, which doesn't have wheels for scipy/scikit-learn yet. Here's how to fix it:

## Method 1: Delete and Recreate Service (Recommended)

1. **Go to Render Dashboard**
2. **Click on your `mlwebsite` service**
3. **Settings** → Scroll to bottom → **Delete Service**
4. **Create New Web Service:**
   - Click **New +** → **Web Service**
   - Connect your GitHub repository
   - **IMPORTANT:** Look for **"Python Version"** dropdown during setup
   - Select **Python 3.12** (NOT 3.13)
   - Name: `mlwebsite`
   - Region: Your choice
   - Branch: `main`
   - Build Command: `chmod +x build.sh && ./build.sh`
   - Start Command: `gunicorn app:app`
   - Plan: Free
5. **Click "Create Web Service"**

## Method 2: Check Advanced Settings

1. Go to your service → **Settings**
2. Look for **"Build & Deploy"** section
3. Check for **"Python Version"** or **"Runtime"** option
4. If found, change to **Python 3.12**

## Method 3: Use Environment Variables (May Not Work)

1. Go to **Settings** → **Environment Variables**
2. Add:
   - Key: `PYTHON_VERSION`
   - Value: `3.12.8`
3. Save and redeploy

## Current Status

I've updated the packages to use latest versions that *might* work with Python 3.13, but **the best solution is to use Python 3.12**.

The build script (`build.sh`) will install packages in the correct order, but if Python 3.13 is used, scipy/scikit-learn will try to build from source and fail.

## After Setting Python 3.12

1. Commit and push:
   ```bash
   git add .
   git commit -m "Add build script and update for Python 3.12"
   git push origin main
   ```

2. The build should succeed!

