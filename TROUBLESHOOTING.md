# Troubleshooting 403 Forbidden Error

## Quick Fix

The 403 error is likely due to database connection issues. Check your database credentials:

### Option 1: Set Environment Variables
```bash
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=caregiver_platform
```

Then restart Flask:
```bash
python3 app.py
```

### Option 2: Edit app.py Directly

Edit lines 20-24 in `app.py`:
```python
DB_USER = os.getenv('DB_USER', 'postgres')  # Change from 'dimerryy'
DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_password')  # Add your password
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'caregiver_platform')
```

## Debug Steps

1. **Check which URL gives 403:**
   - Home page (/) should work
   - Try /users, /caregivers, etc.
   - Note which specific route fails

2. **Check Flask terminal output:**
   - Look for error messages when you access the failing route
   - Database connection errors will show there

3. **Check browser console (F12):**
   - Open Developer Tools
   - Check Console tab for JavaScript errors
   - Check Network tab to see the exact request/response

4. **Test database connection:**
   ```bash
   psql -d caregiver_platform -U postgres -c "SELECT COUNT(*) FROM \"USER\";"
   ```

## Common Issues

- **Wrong database user/password** → Update credentials
- **Database not running** → Start PostgreSQL
- **Database doesn't exist** → Run `createdb caregiver_platform`
- **Tables don't exist** → Run `psql -d caregiver_platform -f database.sql`

