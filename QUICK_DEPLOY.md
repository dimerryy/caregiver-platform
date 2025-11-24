# Quick Deployment Guide

## Fastest Option: PythonAnywhere (Free)

### 5-Minute Setup

1. **Sign up**: [pythonanywhere.com](https://www.pythonanywhere.com) - Free account

2. **Upload files** (Files tab):
   - Upload `app.py`
   - Upload `requirements.txt`
   - Upload entire `templates/` folder
   - Upload `database.sql` (for reference)

3. **Set up database**:
   - **Option 1: Supabase** (Recommended): [supabase.com](https://supabase.com)
     - Sign up → New Project → Copy connection string
   - **Option 2: Neon**: [neon.tech](https://neon.tech)
     - Sign up → Create Project → Copy connection string
   - **Option 3: Render**: [render.com](https://render.com)
     - Sign up → New PostgreSQL → Copy connection string

4. **Edit app.py** (in PythonAnywhere):
   
   **For Supabase:**
   ```python
   DB_USER = 'postgres'
   DB_PASSWORD = 'your_supabase_password'
   DB_HOST = 'db.xxxxx.supabase.co'
   DB_PORT = '5432'
   DB_NAME = 'postgres'
   ```

5. **Load database**:
   - **Option 1**: Use web SQL editor (Supabase/Neon dashboard)
   - **Option 2**: Use `load_db.py` script
   - **Option 3**: Use psql command line

6. **Install dependencies** (Bash console):
   ```bash
   pip3.10 install --user -r requirements.txt
   ```

7. **Create web app** (Web tab):
   - Source code: `/home/yourusername/app.py`
   - Working directory: `/home/yourusername/`
   - WSGI file: Edit and add:
     ```python
     import sys
     path = '/home/yourusername'
     if path not in sys.path:
         sys.path.append(path)
     from app import app as application
     ```

8. **Reload** and visit: `https://yourusername.pythonanywhere.com`

---

## Alternative: Render (Free, GitHub Required)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Deploy"
   git remote add origin <your_repo_url>
   git push -u origin main
   ```

2. **Create PostgreSQL** (Render dashboard):
   - New → PostgreSQL
   - Free plan
   - Copy connection details

3. **Create Web Service** (Render dashboard):
   - New → Web Service
   - Connect GitHub repo
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
   - Add environment variables (DB credentials)

4. **Deploy** - Automatic!

---

## Database Setup (External - Recommended)

### Supabase (Free - Recommended)
1. Sign up: supabase.com
2. Create new project (free)
3. Get connection string from Settings → Database
4. Use in your app

### Neon (Free - Alternative)
1. Sign up: neon.tech
2. Create project (free)
3. Copy connection string
4. Use in your app

### Render (Free - Alternative)
1. Sign up: render.com
2. Create PostgreSQL database (free)
3. Copy connection string
4. Use in your app

### Supabase (Free)
1. Sign up: supabase.com
2. Create project
3. Get PostgreSQL connection string
4. Use in your app

---

## Quick Checklist

- [ ] Hosting account created
- [ ] Files uploaded
- [ ] Database created (external or platform)
- [ ] Database schema loaded
- [ ] Environment variables set
- [ ] Dependencies installed
- [ ] Web app configured
- [ ] App deployed and tested
- [ ] URL ready for submission

---

## Need Help?

See `DEPLOYMENT_GUIDE.md` for detailed instructions for all platforms.

