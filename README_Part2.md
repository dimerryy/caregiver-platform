# Part 2: Python + SQLAlchemy Operations

## Overview
This part implements all database operations using Python 3 and SQLAlchemy. All operations are executed from a single script (`main.py`).

## Files
- `main.py` - Main Python script with all database operations
- `requirements.txt` - Python dependencies

## Prerequisites
- Python 3.7 or higher
- PostgreSQL database (created in Part 1)
- Database connection credentials

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database Connection

The script uses environment variables for database configuration. You can either:

**Option A: Set environment variables**
```bash
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=caregiver_platform
```

**Option B: Edit main.py directly**
Modify the connection variables at the top of `main.py`:
```python
DB_USER = 'postgres'
DB_PASSWORD = 'your_password'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'caregiver_platform'
```

### 3. Ensure Database Exists
Make sure your PostgreSQL database is running and accessible. If you haven't created it yet:
```bash
createdb caregiver_platform
psql -d caregiver_platform -f database.sql
```

## Running the Script

```bash
python3 main.py
```

## Operations Implemented

The script executes all operations in the following order:

### 1. Create Tables
- Creates all 7 tables with primary keys and foreign keys
- Includes check constraints and indexes
- Drops existing tables first (if they exist)

### 2. Insert Sample Data
- Inserts 30 users (15 caregivers, 15 members)
- Inserts 15 caregivers
- Inserts 15 members
- Inserts 15 addresses
- Inserts 16 jobs
- Inserts 45 job applications
- Inserts 25 appointments (with various statuses)

### 3. Update Operations
- **3.1**: Updates phone number of "Arman Armanov" to +77773414141
- **3.2**: Adds commission to caregiver hourly rates:
  - If hourly_rate < $10: add $0.3
  - If hourly_rate >= $10: add 10%

### 4. Delete Operations
- **4.1**: Deletes all jobs posted by "Amina Aminova"
- **4.2**: Deletes all members who live on "Kabanbay Batyr Avenue"

### 5. Simple Queries
- **5.1**: Select caregiver and member names for accepted appointments
- **5.2**: List job IDs containing 'soft-spoken' in other requirements
- **5.3**: List work hours of all babysitter positions
- **5.4**: List members looking for Elderly Care in Astana with "No pets" rule

### 6. Complex Queries
- **6.1**: Count number of applicants for each job (multiple joins with aggregation)
- **6.2**: Total hours spent by caregivers for all accepted appointments (multiple joins with aggregation)
- **6.3**: Average pay of caregivers based on accepted appointments (join with aggregation)
- **6.4**: Caregivers who earn above average based on accepted appointments (nested query with aggregation)

### 7. Derived Attribute Query
- Calculates total cost to pay for caregivers for all accepted appointments
- Formula: SUM(hourly_rate * work_hours) for all confirmed appointments

### 8. View Operation
- Creates a view `job_applications_view` showing all job applications with applicant details
- Queries the view to display results

## Output

The script prints:
- Section headers for each operation
- Query results in a formatted table
- Row counts for updates and deletes
- Verification queries after updates/deletes
- Error messages if any operation fails

## Notes

- The script uses SQLAlchemy's Textual SQL approach for clarity and direct SQL execution
- All operations are executed in a single transaction per section
- The script includes error handling with rollback on failures
- Results are formatted for easy reading in the console
- The view is created with `CREATE OR REPLACE` so it can be re-run safely

## Troubleshooting

### Connection Errors
- Verify PostgreSQL is running: `pg_isready`
- Check database credentials are correct
- Ensure the database exists: `psql -l | grep caregiver_platform`

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version: `python3 --version` (should be 3.7+)

### Data Errors
- If tables already exist with data, the script will drop and recreate them
- Make sure you have sufficient permissions to create/drop tables

## For Demo Video

When recording your demo:
1. Show the database connection setup
2. Execute the script step by step (or all at once)
3. Highlight each section's output
4. Show the view creation and query results
5. Verify that all queries return non-empty results

