# Quick Start Guide

Follow these steps to set up and test the entire system.

## Step-by-Step Setup

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

This installs:
- SQLAlchemy (for database operations)
- psycopg2-binary (PostgreSQL driver)
- Flask (web framework)

### 2. Set Up Database

```bash
# Create database
createdb caregiver_platform

# Load schema and data
psql -d caregiver_platform -f database.sql
```

### 3. Configure Database Connection

**Option A: Environment Variables (Recommended)**

```bash
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=caregiver_platform
```

**Option B: Edit Files**

Edit `main.py` and `app.py` lines 23-27 to set your database credentials.

### 4. Test Part 2

```bash
python3 main.py
```

**Expected Output:**
- ✓ Database connection successful!
- ✓ All tables created successfully!
- ✓ Sample data inserted successfully!
- All update, delete, and query operations with results

### 5. Test Part 3

```bash
python3 app.py
```

Then open browser: `http://localhost:5000`

**Test each table:**
1. Click on each table in navigation
2. Create a new record
3. View the record
4. Edit the record
5. Delete the record

## Quick Verification Checklist

Run this to verify everything:

```bash
# Run the test script
./test_system.sh

# Or manually check:
psql -d caregiver_platform -c "SELECT COUNT(*) FROM USER;"
python3 -c "import main; print('Part 2 OK')"
python3 -c "import app; print('Part 3 OK')"
```

## Common Issues & Solutions

### Issue: "ModuleNotFoundError"
**Solution:** `pip3 install -r requirements.txt`

### Issue: "could not connect to server"
**Solution:** 
- Check PostgreSQL is running: `pg_isready`
- Verify database exists: `psql -l | grep caregiver_platform`
- Check credentials in environment variables

### Issue: "relation does not exist"
**Solution:** Run `psql -d caregiver_platform -f database.sql`

### Issue: "port 5000 already in use"
**Solution:** Edit `app.py` last line to use different port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Verification Commands

```bash
# Check database tables
psql -d caregiver_platform -c "\dt"

# Check record counts
psql -d caregiver_platform -c "
SELECT 'USER' as table_name, COUNT(*) FROM USER
UNION ALL SELECT 'CAREGIVER', COUNT(*) FROM CAREGIVER
UNION ALL SELECT 'MEMBER', COUNT(*) FROM MEMBER
UNION ALL SELECT 'ADDRESS', COUNT(*) FROM ADDRESS
UNION ALL SELECT 'JOB', COUNT(*) FROM JOB
UNION ALL SELECT 'JOB_APPLICATION', COUNT(*) FROM JOB_APPLICATION
UNION ALL SELECT 'APPOINTMENT', COUNT(*) FROM APPOINTMENT;
"

# Test Python imports
python3 -c "from sqlalchemy import create_engine; print('SQLAlchemy OK')"
python3 -c "import flask; print('Flask OK')"
```

