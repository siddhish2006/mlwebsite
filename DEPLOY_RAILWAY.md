# Deploy to Railway.app (EASIEST!)

Railway is much simpler than Render and lets you easily choose Python version.

## Quick Setup (5 minutes)

### Step 1: Sign Up
1. Go to https://railway.app
2. Sign up with GitHub (free)

### Step 2: Deploy
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your `Aimlproject` repository
4. Railway will auto-detect it's a Python app

### Step 3: Set Python Version (IMPORTANT!)
1. Go to your project → **Settings**
2. Find **"Python Version"** or **"Runtime"**
3. Select **Python 3.12** (NOT 3.13!)
4. Save

### Step 4: Set Start Command
1. Go to **Settings** → **Deploy**
2. **Start Command:** `gunicorn app:app`
3. Save

### Step 5: Add Environment Variable (if needed)
1. Go to **Variables** tab
2. Add: `PORT` = `5000` (Railway sets this automatically, but just in case)

### Done! 🎉

Railway will automatically:
- Build your app
- Deploy it
- Give you a URL like: `https://your-app.railway.app`

## Free Tier
- $5 free credit per month
- More than enough for this app
- Auto-deploys on git push

## That's It!

Much easier than Render! No build script issues, easy Python version selection.

