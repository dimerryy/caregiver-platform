# Render Deployment - Quick Start

## 5-Minute Setup

### 1. Push to GitHub
```bash
git add .
git commit -m "Ready for Render deployment"
git remote add origin https://github.com/yourusername/caregiver-platform.git
git push -u origin main
```

### 2. Create PostgreSQL on Render
1. Go to [render.com](https://render.com) → **New +** → **PostgreSQL**
2. Name: `caregiver-platform-db`
3. Plan: **Free**
4. Click **Create Database**
5. **Save connection details!**

### 3. Load Database
- Go to database dashboard → **Connect** → **psql**
- Or use **Data** tab → Run SQL
- Paste contents of `database.sql` and execute

### 4. Create Web Service
1. **New +** → **Web Service**
2. Connect GitHub repo
3. Configure:
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `gunicorn app:app`
4. **Add Environment Variables**:
   ```
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=5432
   DB_NAME=your_db_name
   SECRET_KEY=e7e76228685d8a2f207c1ca59a84109bbc27e2e6b9e0f66aa3e202f971d031ef
   ```
5. Click **Create Web Service**

### 5. Wait & Test
- Wait 5-10 minutes for first deployment
- Visit your URL: `https://caregiver-platform.onrender.com`
- Test CRUD operations

## Environment Variables Template

Copy these from your Render PostgreSQL dashboard:

```
DB_USER=caregiver_user
DB_PASSWORD=your_password_here
DB_HOST=dpg-xxxxx-a.oregon-postgres.render.com
DB_PORT=5432
DB_NAME=caregiver_platform_xxxxx
SECRET_KEY=e7e76228685d8a2f207c1ca59a84109bbc27e2e6b9e0f66aa3e202f971d031ef
```

## Your Deployed URL

After deployment: `https://caregiver-platform.onrender.com`

**This is what you'll submit!**

See `RENDER_DEPLOYMENT.md` for detailed instructions.

