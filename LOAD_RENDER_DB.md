# How to Load Database into Render PostgreSQL

## Your Database Info
- **Host**: `dpg-d4i7cfbe5dus73ch3m3g-a.frankfurt-postgres.render.com`
- **Full connection string format**: `postgresql://user:password@dpg-d4i7cfbe5dus73ch3m3g-a.frankfurt-postgres.render.com:5432/database_name`

## Method 1: Using Render's Web Interface (Easiest)

1. Go to your Render dashboard
2. Click on your PostgreSQL database
3. Go to **Connect** tab
4. Click **psql** (opens web-based SQL editor)
5. Or go to **Data** tab → **SQL Editor**
6. Copy the entire contents of `database.sql`
7. Paste into the SQL editor
8. Click **Run** or **Execute**
9. Wait for completion
10. Verify tables were created in **Data** tab

**This is the easiest method - no SSL issues!**

## Method 2: Using Python Script (with venv)

```bash
# Activate your venv first
source venv/bin/activate

# Set environment variables
export DB_USER=your_user
export DB_PASSWORD=your_password
export DB_HOST=dpg-d4i7cfbe5dus73ch3m3g-a.frankfurt-postgres.render.com
export DB_PORT=5432
export DB_NAME=your_database_name

# Run the script
python3 load_render_db.py
```

Or with connection string:
```bash
source venv/bin/activate
python3 load_render_db.py "postgresql://user:password@dpg-d4i7cfbe5dus73ch3m3g-a.frankfurt-postgres.render.com:5432/dbname?sslmode=require"
```

## Method 3: Using psql with SSL

```bash
# Set password as environment variable (avoids exposing in command)
export PGPASSWORD='your_password'

# Connect with SSL
psql "postgresql://user@dpg-d4i7cfbe5dus73ch3m3g-a.frankfurt-postgres.render.com:5432/dbname?sslmode=require" -f database.sql
```

Or with explicit SSL flags:
```bash
psql "host=dpg-d4i7cfbe5dus73ch3m3g-a.frankfurt-postgres.render.com port=5432 dbname=your_db user=your_user sslmode=require" -f database.sql
```

## Get Your Full Connection Details

1. Go to Render dashboard
2. Click on your PostgreSQL database
3. Go to **Connections** tab
4. You'll see:
   - **Internal Database URL**: For services on Render
   - **External Database URL**: For connecting from outside
   - Copy the **External Database URL**

The URL format is:
```
postgresql://user:password@dpg-d4i7cfbe5dus73ch3m3g-a.frankfurt-postgres.render.com:5432/database_name
```

## Recommended: Use Render's Web Interface

**This is the easiest and most reliable method:**

1. Render Dashboard → Your Database → **Connect** → **psql**
2. Paste `database.sql` contents
3. Execute
4. Done!

No SSL configuration needed, no command line issues.

