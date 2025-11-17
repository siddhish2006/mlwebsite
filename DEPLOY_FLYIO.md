# Deploy to Fly.io (Alternative)

## Setup

1. **Install Fly CLI:**
   ```bash
   # Windows (PowerShell)
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Sign up:**
   ```bash
   fly auth signup
   ```

3. **Create app:**
   ```bash
   fly launch
   ```
   - It will ask for Python version → Choose **3.12**
   - It will auto-detect your app

4. **Deploy:**
   ```bash
   fly deploy
   ```

Done! Your app will be at: `https://your-app.fly.dev`

## Free Tier
- 3 shared VMs
- 160GB outbound data
- Perfect for this app

