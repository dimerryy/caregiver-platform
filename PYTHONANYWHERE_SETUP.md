# PythonAnywhere Deployment with External PostgreSQL

Since PythonAnywhere's free tier doesn't include PostgreSQL, we'll use an external database service.

## Step 1: Get Free PostgreSQL Database

### Option A: Supabase (Recommended - Free & Reliable)

1. Go to [supabase.com](https://supabase.com)
2. Sign up with GitHub (recommended) or email
3. Click **New Project**
4. Fill in:
   - **Name**: `caregiver-platform`
   - **Database Password**: (create a strong password - save it!)
   - **Region**: Choose closest to you
5. Click **Create new project**
6. Wait 2-3 minutes for setup

7. **Get connection details:**
   - Go to **Settings** → **Database**
   - Scroll to **Connection string**
   - Copy **URI** (or use individual settings):
     - **Host**: `db.xxxxx.supabase.co`
     - **Port**: `5432`
     - **Database**: `postgres`
     - **User**: `postgres`
     - **Password**: (the one you created)
     - **Connection string**: `postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres`

### Option B: Neon (Free Tier - Modern & Fast)

1. Go to [neon.tech](https://neon.tech)
2. Sign up with GitHub
3. Click **Create a project**
4. Name: `caregiver-platform`
5. Click **Create project**
6. **Get connection string:**
   - Click on your project
   - Copy the connection string (starts with `postgresql://`)

### Option C: Render (Free PostgreSQL)

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click **New +** → **PostgreSQL**
4. Name: `caregiver-platform-db`
5. Plan: **Free**
6. Click **Create Database**
7. **Get connection details:**
   - Internal Database URL (for Render services)
   - External Database URL (for PythonAnywhere)

1. Go to [supabase.com](https://supabase.com)
2. Sign up with GitHub
3. Create new project
4. Go to **Settings** → **Database**
5. Copy connection string

---

## Step 2: Load Database Schema

### Using Supabase Web Interface

1. Go to your Supabase dashboard
2. Click **SQL Editor** in left sidebar
3. Click **New query**
4. Copy the contents of `database.sql`
5. Paste into SQL Editor
6. Click **Run** (or press Ctrl+Enter)
7. Verify tables were created in **Table Editor**

### Using Neon Web Interface

1. Go to your Neon dashboard
2. Click on your project
3. Click **SQL Editor**
4. Copy contents of `database.sql`
5. Paste and click **Run**
6. Verify tables in **Tables** section

### Using psql (Command Line)

```bash
# Get your connection URL from Supabase/Neon/Render
# Format: postgresql://user:password@host:5432/dbname

# Load schema
psql "postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres" -f database.sql
```

### Using Python Script

Use the provided `load_db.py`:
```python
# Update with your Supabase/Neon/Render credentials
DATABASE_URL = "postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres"

engine = create_engine(DATABASE_URL)

with open('database.sql', 'r') as f:
    sql_content = f.read()
    
    # Split by semicolon and execute each statement
    statements = [s.strip() for s in sql_content.split(';') if s.strip()]
    
    with engine.connect() as conn:
        for statement in statements:
            if statement:
                try:
                    conn.execute(text(statement))
                except Exception as e:
                    print(f"Error: {e}")
        conn.commit()

print("Database loaded successfully!")
```

Run: `python3 load_db.py`

---

## Step 3: Upload Files to PythonAnywhere

1. **Go to PythonAnywhere Files tab**
2. **Navigate to `/home/yourusername/`**
3. **Upload these files:**
   - `app.py`
   - `requirements.txt`
   - `database.sql` (for reference)
   - Entire `templates/` folder (create folder first, then upload all HTML files)

### Upload Templates Folder:
1. Click **New directory** → Name it `templates`
2. Click into `templates/`
3. Create subdirectories: `users`, `caregivers`, `members`, `addresses`, `jobs`, `job_applications`, `appointments`
4. Upload HTML files to respective folders

---

## Step 4: Update app.py with Database Credentials

1. **In PythonAnywhere Files tab, open `app.py`**
2. **Find lines 20-24** and update:

**For Supabase:**
```python
# Database connection configuration
DB_USER = 'postgres'  # Usually 'postgres' for Supabase
DB_PASSWORD = 'your_supabase_password'  # The password you created
DB_HOST = 'db.xxxxx.supabase.co'  # From Supabase Settings → Database
DB_PORT = '5432'
DB_NAME = 'postgres'  # Usually 'postgres' for Supabase
```

**For Neon:**
```python
DB_USER = 'your_neon_user'  # From Neon dashboard
DB_PASSWORD = 'your_neon_password'  # From Neon dashboard
DB_HOST = 'ep-xxxxx.us-east-2.aws.neon.tech'  # From Neon
DB_PORT = '5432'
DB_NAME = 'neondb'  # Usually 'neondb' for Neon
```

**For Render:**
```python
DB_USER = 'your_render_user'  # From Render dashboard
DB_PASSWORD = 'your_render_password'  # From Render dashboard
DB_HOST = 'dpg-xxxxx-a.oregon-postgres.render.com'  # From Render
DB_PORT = '5432'
DB_NAME = 'caregiver_platform_db'  # Your database name
```

---

## Step 5: Install Dependencies

1. **Go to Consoles tab**
2. **Click "Bash"**
3. **Run:**
   ```bash
   pip3.10 install --user sqlalchemy psycopg2-binary flask gunicorn
   ```

Or if you have requirements.txt uploaded:
```bash
pip3.10 install --user -r requirements.txt
```

---

## Step 6: Create Web App

1. **Go to Web tab**
2. **Click "Add a new web app"**
3. **Select "Manual configuration"**
4. **Select "Python 3.10"** (or latest available)
5. **Click "Next"**

---

## Step 7: Configure Web App

1. **Source code**: `/home/yourusername/app.py`
2. **Working directory**: `/home/yourusername/`

3. **WSGI configuration file**: Click the link (usually `/var/www/yourusername_pythonanywhere_com_wsgi.py`)

4. **Replace all content with:**
   ```python
   import sys

   # Add your home directory to the path
   path = '/home/yourusername'
   if path not in sys.path:
       sys.path.insert(0, path)

   # Import your Flask app
   from app import app as application

   if __name__ == "__main__":
       application.run()
   ```

5. **Save the file**

---

## Step 8: Reload Web App

1. **Go back to Web tab**
2. **Click the green "Reload" button**
3. **Wait for it to reload**
4. **Visit your URL**: `https://yourusername.pythonanywhere.com`

---

## Step 9: Test Your App

1. Visit your URL
2. You should see the home page
3. Test CRUD operations:
   - Click "Users" → Create a user
   - Click "Caregivers" → Create a caregiver
   - Test other tables

---

## Troubleshooting

### Error: "could not connect to server"
- Check database credentials in `app.py`
- Verify Supabase/Neon/Render database is running
- For Supabase: Make sure you're using the correct host (db.xxxxx.supabase.co)
- Check firewall/network settings
- Some services require IP whitelisting (check dashboard settings)

### Error: "relation does not exist"
- Database schema not loaded
- Go back to Step 2 and load `database.sql`

### Error: "Module not found"
- Dependencies not installed
- Go to Step 5 and install requirements

### Error: "Template not found"
- Templates folder not uploaded correctly
- Check file structure in PythonAnywhere Files tab

### Check Error Logs
1. Go to **Web tab**
2. Click **Error log** link
3. Read error messages for debugging

---

## Quick Checklist

- [ ] Supabase/Neon/Render account created
- [ ] Database instance created
- [ ] Database schema loaded (database.sql)
- [ ] Files uploaded to PythonAnywhere
- [ ] app.py updated with database credentials
- [ ] Dependencies installed
- [ ] Web app created and configured
- [ ] WSGI file updated
- [ ] Web app reloaded
- [ ] App tested and working

---

## Your Deployed URL

Once everything is set up, your app will be available at:
**https://yourusername.pythonanywhere.com**

This is the URL you'll submit with your assignment!

---

## Alternative: Use SQLite (Not Recommended)

If you absolutely cannot use external PostgreSQL, you could modify the app to use SQLite, but this is **NOT recommended** because:
- Assignment requires PostgreSQL or MySQL
- SQLite has different syntax
- Would require significant code changes

**Recommended: Supabase + PythonAnywhere** - Free, reliable, and works perfectly!

**Alternative options:**
- **Neon** - Modern, fast, free tier
- **Render** - Free PostgreSQL with easy setup

