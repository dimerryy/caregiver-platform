# Complete Setup and Testing Guide

This guide will help you set up and test the entire system to ensure it meets all assignment requirements.

## Prerequisites Check

First, verify you have the required software:

```bash
# Check Python version (should be 3.7+)
python3 --version

# Check PostgreSQL
psql --version

# Check if pip is available
pip3 --version
```

## Step 1: Database Setup (Part 1)

### 1.1 Create PostgreSQL Database

```bash
# Create database
createdb caregiver_platform

# Verify database was created
psql -l | grep caregiver_platform
```

### 1.2 Load Schema and Data

```bash
# Option A: Use the combined file
psql -d caregiver_platform -f database.sql

# Option B: Use separate files
psql -d caregiver_platform -f schema.sql
psql -d caregiver_platform -f sample_data.sql
```

### 1.3 Verify Database Setup

```bash
# Connect to database
psql -d caregiver_platform

# Run these queries to verify:
```

```sql
-- Check all tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- Should show: address, appointment, caregiver, job, job_application, member, user

-- Count records in each table
SELECT 'USER' as table_name, COUNT(*) as count FROM USER
UNION ALL SELECT 'CAREGIVER', COUNT(*) FROM CAREGIVER
UNION ALL SELECT 'MEMBER', COUNT(*) FROM MEMBER
UNION ALL SELECT 'ADDRESS', COUNT(*) FROM ADDRESS
UNION ALL SELECT 'JOB', COUNT(*) FROM JOB
UNION ALL SELECT 'JOB_APPLICATION', COUNT(*) FROM JOB_APPLICATION
UNION ALL SELECT 'APPOINTMENT', COUNT(*) FROM APPOINTMENT;

-- Should show at least 10 records per table

-- Verify foreign keys
SELECT
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
ORDER BY tc.table_name;

-- Exit psql
\q
```

## Step 2: Install Python Dependencies

```bash
# Install all required packages
pip3 install -r requirements.txt

# Verify installation
pip3 list | grep -E "(sqlalchemy|psycopg2|flask)"
```

## Step 3: Configure Database Connection

### Option A: Environment Variables (Recommended)

```bash
# Set environment variables
export DB_USER=postgres
export DB_PASSWORD=your_password_here
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=caregiver_platform
export SECRET_KEY=dev-secret-key-change-in-production
```

### Option B: Edit Files Directly

Edit `main.py` and `app.py` to set database credentials directly.

## Step 4: Test Part 2 (Python + SQLAlchemy)

### 4.1 Run the Main Script

```bash
# Run main.py (this will create tables, insert data, and run all queries)
python3 main.py
```

### 4.2 Verify Output

The script should:
- ✅ Create all tables successfully
- ✅ Insert sample data successfully
- ✅ Update phone number for Arman Armanov
- ✅ Update caregiver hourly rates with commission
- ✅ Delete jobs by Amina Aminova
- ✅ Delete members on Kabanbay Batyr street
- ✅ Execute 4 simple queries (with results)
- ✅ Execute 4 complex queries (with results)
- ✅ Calculate total cost (derived attribute)
- ✅ Create and query view

### 4.3 Check for Errors

Look for:
- ✗ Error messages (should be none)
- ✓ Success messages for each operation
- Non-empty results for all queries

## Step 5: Test Part 3 (Flask Web Application)

### 5.1 Start the Flask Application

```bash
# Run the Flask app
python3 app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

### 5.2 Access the Web Application

Open your browser and go to: `http://localhost:5000`

### 5.3 Test CRUD Operations

Test each table systematically:

#### Users
1. Click "Users" in navigation
2. Click "Create New User"
3. Fill in form and submit
4. Verify user appears in list
5. Click "View" to see details
6. Click "Edit" to modify
7. Click "Delete" to remove (confirm deletion)

#### Caregivers
1. Create a user first (if needed)
2. Click "Caregivers" → "Create New Caregiver"
3. Select a user from dropdown
4. Fill in caregiver details
5. Verify in list
6. Test Edit and Delete

#### Members
1. Create a user first (if needed)
2. Click "Members" → "Create New Member"
3. Select a user from dropdown
4. Fill in member details
5. Verify in list
6. Test Edit and Delete

#### Addresses
1. Create a member first
2. Click "Addresses" → "Create New Address"
3. Select a member from dropdown
4. Fill in address details
5. Verify in list
6. Test Edit and Delete

#### Jobs
1. Click "Jobs" → "Create New Job"
2. Select a member
3. Fill in job details
4. Verify in list
5. Test Edit and Delete

#### Job Applications
1. Click "Job Applications" → "Create New Job Application"
2. Select caregiver and job
3. Verify in list
4. Test Delete

#### Appointments
1. Click "Appointments" → "Create New Appointment"
2. Select caregiver and member
3. Fill in appointment details
4. Verify in list
5. Test Edit and Delete

## Step 6: Verify All Requirements

### Part 1 Requirements ✅
- [ ] Database created (PostgreSQL)
- [ ] All 7 tables exist with correct names
- [ ] Primary keys defined
- [ ] Foreign keys defined
- [ ] At least 10 records per table
- [ ] Data sufficient for Part 2 queries

### Part 2 Requirements ✅
- [ ] Single Python script (main.py)
- [ ] Uses SQLAlchemy
- [ ] Creates all tables
- [ ] Inserts sample data
- [ ] Updates: phone number and commission
- [ ] Deletes: jobs and members
- [ ] 4 simple queries work
- [ ] 4 complex queries work
- [ ] Derived attribute query works
- [ ] View operation works

### Part 3 Requirements ✅
- [ ] Flask application runs
- [ ] CRUD for USER table
- [ ] CRUD for CAREGIVER table
- [ ] CRUD for MEMBER table
- [ ] CRUD for ADDRESS table
- [ ] CRUD for JOB table
- [ ] CRUD for JOB_APPLICATION table
- [ ] CRUD for APPOINTMENT table
- [ ] Simple, clear UI
- [ ] All operations functional

## Troubleshooting

### Database Connection Issues

```bash
# Test PostgreSQL connection
psql -h localhost -U postgres -d caregiver_platform

# If connection fails, check:
# 1. PostgreSQL is running: pg_isready
# 2. Database exists: psql -l
# 3. User has permissions
```

### Python Import Errors

```bash
# Reinstall dependencies
pip3 install --upgrade -r requirements.txt

# Check Python path
python3 -c "import sys; print(sys.path)"
```

### Flask App Issues

```bash
# Check if port 5000 is in use
lsof -i :5000

# Use different port
python3 app.py  # Edit app.py to change port
```

### Foreign Key Constraint Errors

- Ensure parent records exist before creating child records
- Check that IDs match between tables
- Verify foreign key relationships in database

## Quick Test Script

Save this as `test_system.sh`:

```bash
#!/bin/bash

echo "=== Testing Caregiver Platform System ==="

# Test 1: Database exists
echo "1. Checking database..."
psql -l | grep -q caregiver_platform && echo "   ✓ Database exists" || echo "   ✗ Database not found"

# Test 2: Tables exist
echo "2. Checking tables..."
TABLE_COUNT=$(psql -d caregiver_platform -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';")
if [ "$TABLE_COUNT" -ge 7 ]; then
    echo "   ✓ Found $TABLE_COUNT tables"
else
    echo "   ✗ Only found $TABLE_COUNT tables (expected 7+)"
fi

# Test 3: Python dependencies
echo "3. Checking Python dependencies..."
python3 -c "import sqlalchemy; import flask; import psycopg2" 2>/dev/null && echo "   ✓ All dependencies installed" || echo "   ✗ Missing dependencies"

# Test 4: Part 2 script
echo "4. Testing Part 2 script..."
python3 -c "import main" 2>/dev/null && echo "   ✓ main.py imports successfully" || echo "   ✗ main.py has errors"

# Test 5: Part 3 app
echo "5. Testing Part 3 app..."
python3 -c "import app" 2>/dev/null && echo "   ✓ app.py imports successfully" || echo "   ✗ app.py has errors"

echo "=== Test Complete ==="
```

Make it executable and run:
```bash
chmod +x test_system.sh
./test_system.sh
```

## Next Steps for Demo Video

1. **Part 1**: Show database creation and data insertion
2. **Part 2**: Run main.py and show query results
3. **Part 3**: Demonstrate CRUD operations in the web app

Record your screen showing:
- Database setup
- Running main.py with all operations
- Web app CRUD operations for each table

