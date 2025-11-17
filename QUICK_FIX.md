# QUICK FIX - Set Python 3.12 in Railway

Railway is using Python 3.13.9 which breaks pandas. Here's the **EASIEST FIX**:

## In Railway Dashboard:

1. **Go to your service** → **Settings** tab
2. **Scroll to "Variables"** section  
3. **Click "New Variable"**
4. Add:
   - **Key:** `PYTHON_VERSION`
   - **Value:** `3.12.8`
5. **Save**

## Then:

1. Go to **Deployments** tab
2. Click **"Redeploy"** (or just push a new commit)

That's it! Railway will use Python 3.12 and the build will succeed.

---

**Alternative:** If you can't find Variables section:
- Go to **Settings** → Look for **"Python Version"** dropdown
- Select **3.12**
- Save and redeploy

The files I created (`nixpacks.toml`, `.python-version`) should also help, but setting it in the dashboard is the most reliable way.

