# How to Run and Test the Complete System

## 🚀 Quick Setup (5 Steps)

### Step 1: Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

### Step 2: Create and Setup Database
```bash
# Create database
createdb caregiver_platform

# Load schema and data
psql -d caregiver_platform -f database.sql
```

### Step 3: Set Database Credentials
```bash
# Set environment variables
export DB_USER=postgres
export DB_PASSWORD=your_postgres_password
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=caregiver_platform
```

**OR** edit `main.py` and `app.py` directly (lines 23-27) with your credentials.

### Step 4: Test Part 2 (Python Script)
```bash
python3 main.py
```

**What to verify:**
- ✅ No error messages
- ✅ "Database connection successful!"
- ✅ "All tables created successfully!"
- ✅ "Sample data inserted successfully!"
- ✅ All queries show results (not empty)
- ✅ Updates and deletes complete successfully

### Step 5: Test Part 3 (Web Application)
```bash
python3 app.py
```

Then open: **http://localhost:5000**

**What to test:**
1. **Home page** loads with navigation
2. **Each table** (Users, Caregivers, Members, etc.):
   - Click "Create New" → Fill form → Submit → Verify appears in list
   - Click "View" → See details
   - Click "Edit" → Modify → Save → Verify changes
   - Click "Delete" → Confirm → Verify removed

## 📋 Complete Verification Checklist

### Part 1: Database Schema ✅
```bash
# Verify tables exist
psql -d caregiver_platform -c "\dt"

# Should show 7 tables:
# - address
# - appointment  
# - caregiver
# - job
# - job_application
# - member
# - user

# Verify data (should have 10+ records each)
psql -d caregiver_platform -c "
SELECT 'USER' as table_name, COUNT(*) as count FROM USER
UNION ALL SELECT 'CAREGIVER', COUNT(*) FROM CAREGIVER
UNION ALL SELECT 'MEMBER', COUNT(*) FROM MEMBER
UNION ALL SELECT 'ADDRESS', COUNT(*) FROM ADDRESS
UNION ALL SELECT 'JOB', COUNT(*) FROM JOB
UNION ALL SELECT 'JOB_APPLICATION', COUNT(*) FROM JOB_APPLICATION
UNION ALL SELECT 'APPOINTMENT', COUNT(*) FROM APPOINTMENT;
"
```

### Part 2: Python Script ✅
```bash
# Run the script
python3 main.py

# Verify output includes:
# ✓ Section 1: CREATING TABLES
# ✓ Section 2: INSERTING SAMPLE DATA
# ✓ Section 3: UPDATE OPERATIONS
#   - Phone number updated for Arman Armanov
#   - Commission added to hourly rates
# ✓ Section 4: DELETE OPERATIONS
#   - Jobs by Amina Aminova deleted
#   - Members on Kabanbay Batyr deleted
# ✓ Section 5: SIMPLE QUERIES (4 queries with results)
# ✓ Section 6: COMPLEX QUERIES (4 queries with results)
# ✓ Section 7: DERIVED ATTRIBUTE QUERY (total cost)
# ✓ Section 8: VIEW OPERATION (job applications view)
```

### Part 3: Web Application ✅

**Test CRUD for each table:**

1. **USER Table**
   - ✅ List users
   - ✅ Create user
   - ✅ View user details
   - ✅ Edit user
   - ✅ Delete user

2. **CAREGIVER Table**
   - ✅ List caregivers
   - ✅ Create caregiver (select from available users)
   - ✅ Edit caregiver
   - ✅ Delete caregiver

3. **MEMBER Table**
   - ✅ List members
   - ✅ Create member (select from available users)
   - ✅ Edit member
   - ✅ Delete member

4. **ADDRESS Table**
   - ✅ List addresses
   - ✅ Create address (select from available members)
   - ✅ Edit address
   - ✅ Delete address

5. **JOB Table**
   - ✅ List jobs
   - ✅ Create job (select member)
   - ✅ Edit job
   - ✅ Delete job

6. **JOB_APPLICATION Table**
   - ✅ List job applications
   - ✅ Create job application (select caregiver and job)
   - ✅ Delete job application

7. **APPOINTMENT Table**
   - ✅ List appointments
   - ✅ Create appointment (select caregiver and member)
   - ✅ Edit appointment
   - ✅ Delete appointment

## 🔍 Automated Testing

Run the test script:
```bash
./test_system.sh
```

This checks:
- Database exists
- Tables are created
- Python dependencies installed
- Scripts can be imported
- Required files exist
- Templates exist

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'sqlalchemy'"
**Solution:**
```bash
pip3 install -r requirements.txt
```

### Problem: "could not connect to server"
**Solution:**
```bash
# Check PostgreSQL is running
pg_isready

# If not running, start it:
# macOS: brew services start postgresql
# Linux: sudo systemctl start postgresql
```

### Problem: "database 'caregiver_platform' does not exist"
**Solution:**
```bash
createdb caregiver_platform
psql -d caregiver_platform -f database.sql
```

### Problem: "relation does not exist"
**Solution:**
```bash
# Reload schema and data
psql -d caregiver_platform -f database.sql
```

### Problem: "port 5000 already in use"
**Solution:**
Edit `app.py` last line:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Problem: Foreign key constraint errors
**Solution:**
- Create parent records first (USER before CAREGIVER/MEMBER)
- Create MEMBER before ADDRESS
- Ensure IDs match between tables

## ✅ Final Verification

Before submitting, verify:

### Part 1 ✅
- [ ] Database created with PostgreSQL
- [ ] All 7 tables with correct names
- [ ] Primary keys defined
- [ ] Foreign keys defined
- [ ] At least 10 records per table
- [ ] Data allows Part 2 queries to return results

### Part 2 ✅
- [ ] Single script `main.py` runs successfully
- [ ] Uses SQLAlchemy
- [ ] Creates all tables
- [ ] Inserts sample data
- [ ] Updates work (phone, commission)
- [ ] Deletes work (jobs, members)
- [ ] 4 simple queries return results
- [ ] 4 complex queries return results
- [ ] Derived attribute query works
- [ ] View operation works

### Part 3 ✅
- [ ] Flask app runs on http://localhost:5000
- [ ] Navigation works
- [ ] CRUD works for all 7 tables
- [ ] Forms validate input
- [ ] Flash messages appear
- [ ] Delete confirmations work
- [ ] No errors in browser console

## 📝 For Demo Video

Record these in order:

1. **Part 1 (2 min)**
   - Show database creation
   - Show tables in psql
   - Show data counts

2. **Part 2 (3 min)**
   - Run `python3 main.py`
   - Show each section output
   - Highlight query results

3. **Part 3 (5 min)**
   - Show web app home page
   - Demonstrate CRUD for 2-3 tables
   - Show create, read, update, delete operations

**Total: ~10 minutes**

## 🎯 Success Criteria

The system is working correctly if:

1. ✅ `python3 main.py` runs without errors
2. ✅ All queries return non-empty results
3. ✅ Web app loads at http://localhost:5000
4. ✅ Can create, view, edit, delete records in all tables
5. ✅ No database constraint errors
6. ✅ All tables accessible via web interface

If all above are ✅, your system meets all requirements!

