# Render Deployment Guide - Step by Step

This guide will help you deploy the Caregiver Platform to Render.

## Prerequisites

- GitHub account
- Code pushed to GitHub repository
- Render account (free)

---

## Step 1: Push Code to GitHub

### 1.1 Create GitHub Repository

1. Go to [github.com](https://github.com)
2. Click **New repository** (or **+** → **New repository**)
3. Repository name: `caregiver-platform` (or your choice)
4. Description: "CSCI 341 Assignment 3 - Caregiver Platform Database Management System"
5. **Don't** initialize with README, .gitignore, or license
6. Click **Create repository**

### 1.2 Push Your Code

In your terminal (already in the project directory):

```bash
# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: CSCI 341 Assignment 3 - Caregiver Platform"

# Add GitHub remote (replace with your repository URL)
git remote add origin https://github.com/yourusername/caregiver-platform.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note**: Replace `yourusername` with your GitHub username.

---

## Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Click **Get Started for Free**
3. Sign up with **GitHub** (recommended - easiest)
4. Authorize Render to access your repositories

---

## Step 3: Create PostgreSQL Database

### 3.1 Create Database

1. In Render dashboard, click **New +**
2. Select **PostgreSQL**
3. Configure:
   - **Name**: `caregiver-platform-db`
   - **Database**: `caregiver_platform` (or leave default)
   - **User**: `caregiver_user` (or leave default)
   - **Region**: Choose closest to you
   - **PostgreSQL Version**: Latest (15 or 16)
   - **Plan**: **Free**
4. Click **Create Database**
5. Wait 2-3 minutes for database to be created

### 3.2 Get Connection Details

1. Click on your database
2. Go to **Connections** tab
3. You'll see:
   - **Internal Database URL**: For services on Render
   - **External Database URL**: For connecting from outside Render
   - **Host**: `dpg-xxxxx-a.oregon-postgres.render.com`
   - **Port**: `5432`
   - **Database name**: `caregiver_platform_xxxxx`
   - **User**: `caregiver_user`
   - **Password**: (shown, save this!)

**Save these credentials - you'll need them!**

### 3.3 Load Database Schema

**⭐ RECOMMENDED: Using Render's Web Interface (Easiest)**

1. In your database dashboard, click **Connect** → **psql**
   - OR go to **Data** tab → **SQL Editor**
2. Open `database.sql` file on your computer
3. Copy **ALL** contents (Ctrl+A, Ctrl+C)
4. Paste into Render's SQL editor
5. Click **Run** or **Execute**
6. Wait for completion (may take 1-2 minutes)
7. Verify tables in **Data** tab

**This method avoids SSL issues and is the most reliable!**

**Alternative: Using psql Command Line**

```bash
# Set password as environment variable
export PGPASSWORD='your_password'

# Connect with SSL (Render requires SSL)
psql "host=dpg-xxxxx-a.frankfurt-postgres.render.com port=5432 dbname=your_db user=your_user sslmode=require" -f database.sql
```

**Alternative: Using Python Script (with venv activated)**

```bash
# Activate venv first
source venv/bin/activate

# Run with connection string
python3 load_render_db.py "postgresql://user:password@dpg-xxxxx-a.frankfurt-postgres.render.com:5432/dbname?sslmode=require"
```

---

## Step 4: Create Web Service

### 4.1 Create New Web Service

1. In Render dashboard, click **New +**
2. Select **Web Service**
3. Connect your GitHub account if not already connected
4. Select your repository: `caregiver-platform`
5. Click **Connect**

### 4.2 Configure Web Service

Fill in the configuration:

- **Name**: `caregiver-platform` (or your choice)
- **Region**: Same as database (for better performance)
- **Branch**: `main` (or `master`)
- **Root Directory**: (leave empty - root is fine)
- **Environment**: **Python 3**
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```
  gunicorn app:app
  ```

### 4.3 Set Environment Variables

Click **Advanced** → **Add Environment Variable**

Add these variables (use values from your PostgreSQL database):

```
DB_USER=caregiver_user
DB_PASSWORD=your_database_password_from_render
DB_HOST=dpg-xxxxx-a.oregon-postgres.render.com
DB_PORT=5432
DB_NAME=caregiver_platform_xxxxx
SECRET_KEY=your-random-secret-key-here-make-it-long-and-random
```

**Important**: 
- Get these values from your PostgreSQL database dashboard
- Use the **Internal Database URL** values (for services on Render)
- `SECRET_KEY` can be any random string (e.g., generate with: `python3 -c "import secrets; print(secrets.token_hex(32))"`)

### 4.4 Create Web Service

1. Scroll down
2. Click **Create Web Service**
3. Render will start building and deploying

---

## Step 5: Wait for Deployment

1. Watch the build logs
2. First deployment takes 5-10 minutes
3. You'll see:
   - Installing dependencies
   - Building application
   - Starting service

### 5.1 Check Build Logs

If there are errors:
- Check the build logs
- Verify environment variables are set correctly
- Ensure `requirements.txt` includes all dependencies
- Check that `gunicorn` is in requirements.txt

---

## Step 6: Test Your Deployed App

1. Once deployed, you'll get a URL like:
   ```
   https://caregiver-platform.onrender.com
   ```

2. Visit the URL in your browser

3. Test CRUD operations:
   - Home page loads
   - Can view users
   - Can create/edit/delete records
   - All tables accessible

---

## Step 7: Update app.py for Render (if needed)

Render automatically provides environment variables. You can optionally update `app.py` to use Render's `DATABASE_URL`:

```python
import os
from urllib.parse import urlparse

# Check if DATABASE_URL is provided by Render
if 'DATABASE_URL' in os.environ:
    # Render provides DATABASE_URL in format: postgresql://user:pass@host:port/db
    DATABASE_URL = os.environ['DATABASE_URL']
    # Parse if needed, or use directly
    engine = create_engine(DATABASE_URL, echo=False)
else:
    # Your existing code for local development
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'caregiver_platform')
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(DATABASE_URL, echo=False)
```

**Note**: The current `app.py` should work fine with individual environment variables. This is optional.

---

## Troubleshooting

### Build Fails

**Error: "Module not found"**
- Check `requirements.txt` includes all dependencies
- Verify `gunicorn` is in requirements.txt
- Check build logs for specific missing module

**Error: "Command not found: gunicorn"**
- Add `gunicorn>=21.2.0` to `requirements.txt`
- Redeploy

### App Crashes

**Error: "could not connect to server"**
- Verify environment variables are set correctly
- Check database is running (Render dashboard)
- Use Internal Database URL (not External)
- Verify database credentials match

**Error: "relation does not exist"**
- Database schema not loaded
- Go back to Step 3.3 and load `database.sql`

### App is Slow

- Free tier spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- This is normal for free tier
- Consider upgrading for production use

### Check Logs

1. Go to your Web Service dashboard
2. Click **Logs** tab
3. Check for error messages
4. Common issues show up here

---

## Render Free Tier Limitations

- **Web Service**: Spins down after 15 min inactivity (wakes on request)
- **PostgreSQL**: 90 days free, then requires credit card (but still free)
- **Bandwidth**: 100 GB/month
- **Build time**: 750 hours/month

**For assignment submission**: Free tier is sufficient!

---

## Quick Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] PostgreSQL database created on Render
- [ ] Database schema loaded (`database.sql`)
- [ ] Web service created
- [ ] Environment variables set
- [ ] Build successful
- [ ] App accessible at Render URL
- [ ] CRUD operations tested
- [ ] URL ready for submission

---

## Your Deployed URL

Once everything is set up, your app will be available at:
```
https://caregiver-platform.onrender.com
```
(Or whatever name you chose)

**This is the URL you'll submit with your assignment!**

---

## Updating Your App

After making changes:

1. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update description"
   git push origin main
   ```

2. Render automatically detects changes and redeploys
3. Check **Events** tab in Render dashboard to see deployment progress

---

## Need Help?

- Check Render logs for errors
- Verify environment variables
- Ensure database is running
- Test locally first before deploying

Good luck with your deployment! 🚀

