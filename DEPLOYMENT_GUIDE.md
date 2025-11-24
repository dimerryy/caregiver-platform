# Deployment Guide for Caregiver Platform Web Application

This guide covers deploying the Flask application to free hosting platforms.

## Prerequisites

Before deploying, ensure you have:
- ✅ All code working locally
- ✅ Database credentials ready
- ✅ Git repository (optional but recommended)

---

## Option 1: PythonAnywhere (Recommended - Free Tier Available)

PythonAnywhere offers a free tier perfect for this assignment.

### Step 1: Create Account
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for a free "Beginner" account
3. Verify your email

### Step 2: Upload Files
1. Go to **Files** tab
2. Navigate to `/home/yourusername/`
3. Create a folder: `caregiver_platform`
4. Upload all files:
   - `app.py`
   - `requirements.txt`
   - `templates/` folder (upload entire folder)
   - `static/` folder (if you have one)

### Step 3: Set Up Database
**Option A: Use PythonAnywhere's PostgreSQL (if available)**
1. Go to **Databases** tab
2. Create a PostgreSQL database
3. Note the connection details

**Option B: Use External PostgreSQL (Recommended - Free)**
1. **Supabase** (Recommended): [supabase.com](https://supabase.com)
   - Sign up → New Project → Free tier
   - Get connection string from Settings → Database
2. **Neon** (Alternative): [neon.tech](https://neon.tech)
   - Sign up → Create Project → Free tier
   - Copy connection string
3. **Render** (Alternative): [render.com](https://render.com)
   - Sign up → New PostgreSQL → Free tier
   - Copy connection string

### Step 4: Configure Database Connection
1. Go to **Files** tab
2. Edit `app.py`
3. Update database credentials:
   ```python
   DB_USER = 'your_db_user'
   DB_PASSWORD = 'your_db_password'
   DB_HOST = 'your_host'
   DB_PORT = '5432'
   DB_NAME = 'your_db_name'
   ```

### Step 5: Install Dependencies
1. Go to **Consoles** tab
2. Open a **Bash** console
3. Run:
   ```bash
   cd caregiver_platform
   pip3.10 install --user -r requirements.txt
   ```

### Step 6: Load Database Schema
1. In the Bash console:
   ```bash
   psql -h your_host -U your_user -d your_db -f database.sql
   ```
   Or use PythonAnywhere's database interface to run the SQL.

### Step 7: Create Web App
1. Go to **Web** tab
2. Click **Add a new web app**
3. Choose **Manual configuration**
4. Select **Python 3.10** (or latest available)
5. Click **Next**

### Step 8: Configure Web App
1. **Source code**: `/home/yourusername/caregiver_platform/app.py`
2. **Working directory**: `/home/yourusername/caregiver_platform`
3. **WSGI configuration file**: Click the link to edit
4. Replace the content with:
   ```python
   import sys
   path = '/home/yourusername/caregiver_platform'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```
5. Save the file

### Step 9: Reload Web App
1. Go back to **Web** tab
2. Click **Reload** button
3. Your app will be available at: `https://yourusername.pythonanywhere.com`

### Step 10: Test
1. Visit your URL
2. Test CRUD operations
3. Check for any errors in the **Error log** tab

---

## Option 2: Render (Free Tier Available)

Render offers free PostgreSQL and web services.

### Step 1: Create Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended) or email

### Step 2: Prepare Repository
1. Create a GitHub repository
2. Push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/caregiver-platform.git
   git push -u origin main
   ```

### Step 3: Create PostgreSQL Database
1. In Render dashboard, click **New +**
2. Select **PostgreSQL**
3. Name: `caregiver-platform-db`
4. Plan: **Free**
5. Click **Create Database**
6. Note the connection details

### Step 4: Load Database Schema
1. Copy the **Internal Database URL**
2. Use `psql` or a database client to connect
3. Run: `psql <your_database_url> -f database.sql`
   Or use Render's database interface

### Step 5: Create Web Service
1. In Render dashboard, click **New +**
2. Select **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `caregiver-platform`
   - **Environment**: **Python 3**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

### Step 6: Set Environment Variables
In the Web Service settings, add:
```
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432
DB_NAME=your_db_name
SECRET_KEY=your-secret-key-here
```

### Step 7: Deploy
1. Click **Create Web Service**
2. Render will build and deploy automatically
3. Your app will be available at: `https://caregiver-platform.onrender.com`

---

## Option 3: Railway (Free Tier Available)

Railway offers easy deployment with PostgreSQL.

### Step 1: Create Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub

### Step 2: Create New Project
1. Click **New Project**
2. Select **Deploy from GitHub repo**
3. Connect your repository

### Step 3: Add PostgreSQL
1. Click **+ New**
2. Select **Database** → **Add PostgreSQL**
3. Railway will create a database automatically

### Step 4: Configure Environment Variables
1. Go to **Variables** tab
2. Railway automatically provides `DATABASE_URL`
3. Update `app.py` to use `DATABASE_URL`:
   ```python
   import os
   from urllib.parse import urlparse
   
   # For Railway
   if 'DATABASE_URL' in os.environ:
       DATABASE_URL = os.environ['DATABASE_URL']
       # Parse the URL if needed
   else:
       # Your existing code
       DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
   ```

### Step 5: Deploy
1. Railway will auto-deploy on push
2. Your app will be available at: `https://your-app.railway.app`

---

## Option 4: Heroku (No Free Tier, but Easy)

Heroku no longer has a free tier, but it's still easy to use.

### Step 1: Install Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Or download from heroku.com
```

### Step 2: Create Files
Create `Procfile`:
```
web: gunicorn app:app
```

Create `runtime.txt`:
```
python-3.11.0
```

### Step 3: Login and Create App
```bash
heroku login
heroku create caregiver-platform
```

### Step 4: Add PostgreSQL
```bash
heroku addons:create heroku-postgresql:mini
```

### Step 5: Set Environment Variables
```bash
heroku config:set DB_USER=your_user
heroku config:set DB_PASSWORD=your_password
heroku config:set DB_HOST=your_host
heroku config:set DB_PORT=5432
heroku config:set DB_NAME=your_db
heroku config:set SECRET_KEY=your-secret-key
```

### Step 6: Deploy
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Step 7: Load Database
```bash
heroku pg:psql < database.sql
```

---

## Quick Setup Script for Deployment

Create this script to help with deployment:

```bash
#!/bin/bash
# deploy_setup.sh

echo "=== Deployment Setup ==="
echo "1. Exporting database..."
pg_dump -d caregiver_platform > caregiver_platform.sql
echo "✓ Database exported"

echo "2. Checking files..."
echo "Required files:"
ls -1 app.py main.py requirements.txt database.sql 2>/dev/null
echo ""

echo "3. Checking templates..."
find templates -name "*.html" | wc -l | xargs echo "HTML templates found:"
echo ""

echo "4. Ready for deployment!"
echo ""
echo "Next steps:"
echo "- Upload files to your hosting platform"
echo "- Set environment variables"
echo "- Load database schema"
echo "- Deploy!"
```

---

## Database Setup for Deployment

### Using External PostgreSQL (Recommended)

**ElephantSQL (Free Tier):**
1. Sign up at [elephantsql.com](https://www.elephantsql.com)
2. Create "Tiny Turtle" plan (free)
3. Copy connection details
4. Use in your deployment

**Supabase (Free Tier):**
1. Sign up at [supabase.com](https://supabase.com)
2. Create new project
3. Get PostgreSQL connection string
4. Use in your deployment

### Loading Database Schema

Once you have database access:
```bash
# Option 1: Using psql
psql <connection_string> -f database.sql

# Option 2: Using Python
python3 -c "
from sqlalchemy import create_engine, text
engine = create_engine('your_connection_string')
with engine.connect() as conn:
    with open('database.sql', 'r') as f:
        conn.execute(text(f.read()))
    conn.commit()
"
```

---

## Environment Variables Template

Create a `.env` file (don't commit this!):
```
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432
DB_NAME=caregiver_platform
SECRET_KEY=your-secret-key-change-in-production
```

Update `app.py` to use `.env`:
```python
from dotenv import load_dotenv
load_dotenv()  # Load .env file
```

Add to `requirements.txt`:
```
python-dotenv>=1.0.0
```

---

## Testing After Deployment

1. **Home Page**: Visit your deployed URL
2. **Database Connection**: Try accessing any table
3. **CRUD Operations**: Test create, read, update, delete
4. **Error Handling**: Check logs for any errors

---

## Troubleshooting

### Database Connection Errors
- Verify database credentials
- Check if database is accessible from hosting platform
- Ensure firewall allows connections

### Import Errors
- Verify all dependencies in `requirements.txt`
- Check Python version compatibility
- Review deployment logs

### Static Files Not Loading
- Ensure `static/` folder is uploaded
- Check file permissions
- Verify paths in templates

### Template Not Found
- Verify `templates/` folder structure
- Check file permissions
- Ensure templates are uploaded

---

## Recommended: PythonAnywhere (Free)

For this assignment, **PythonAnywhere** is the best choice because:
- ✅ Free tier available
- ✅ Easy to use
- ✅ Supports PostgreSQL
- ✅ Good for Flask apps
- ✅ Mentioned in assignment

## Quick Deployment Checklist

- [ ] Account created on hosting platform
- [ ] Files uploaded (app.py, templates/, requirements.txt)
- [ ] Database created and configured
- [ ] Database schema loaded (database.sql)
- [ ] Environment variables set
- [ ] Dependencies installed
- [ ] Web app configured
- [ ] App deployed and accessible
- [ ] CRUD operations tested
- [ ] URL ready for submission

---

## Submission Note

For the assignment, you need to provide:
- The deployed URL in your submission
- Make sure the app is publicly accessible
- Test all CRUD operations before submission

Good luck with your deployment! 🚀

