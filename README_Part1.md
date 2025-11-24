# Part 1: Database Schema & Initial Data

## Overview
This directory contains the database schema and sample data for the Caregiver Platform assignment.

## Files
- `schema.sql` - Database schema only (table creation with PKs and FKs)
- `sample_data.sql` - Sample data only (insert statements)
- `database.sql` - Combined file with both schema and data (recommended for submission)

## Database System
**PostgreSQL** (chosen for consistency throughout the project)

## Setup Instructions

### Prerequisites
- PostgreSQL installed and running
- `psql` command-line tool or pgAdmin

### Option 1: Using the combined file (Recommended)
```bash
# Create database
createdb caregiver_platform

# Run the combined SQL file
psql -d caregiver_platform -f database.sql
```

### Option 2: Using separate files
```bash
# Create database
createdb caregiver_platform

# Run schema first
psql -d caregiver_platform -f schema.sql

# Then run sample data
psql -d caregiver_platform -f sample_data.sql
```

### Option 3: Using psql interactively
```bash
psql -d caregiver_platform
\i database.sql
```

## Database Schema

### Tables
1. **USER** - Base table for all users (caregivers and members)
   - Primary Key: `user_id`
   - Unique: `email`

2. **CAREGIVER** - Caregiver-specific information
   - Primary Key: `caregiver_user_id` (FK to USER)
   - Check constraint: `caregiving_type` must be one of: 'babysitter', 'elderly care', 'playmate for children'

3. **MEMBER** - Family member-specific information
   - Primary Key: `member_user_id` (FK to USER)

4. **ADDRESS** - Address information for members
   - Primary Key: `member_user_id` (FK to MEMBER)

5. **JOB** - Job postings by members
   - Primary Key: `job_id`
   - Foreign Key: `member_user_id` → MEMBER

6. **JOB_APPLICATION** - Applications by caregivers to jobs
   - Composite Primary Key: (`caregiver_user_id`, `job_id`)
   - Foreign Keys: `caregiver_user_id` → CAREGIVER, `job_id` → JOB

7. **APPOINTMENT** - Appointments between members and caregivers
   - Primary Key: `appointment_id`
   - Foreign Keys: `caregiver_user_id` → CAREGIVER, `member_user_id` → MEMBER
   - Check constraint: `status` must be one of: 'pending', 'confirmed', 'declined', 'completed'

## Sample Data Summary

- **USER**: 30 instances (15 caregivers, 15 members)
- **CAREGIVER**: 15 instances
- **MEMBER**: 15 instances
- **ADDRESS**: 15 instances
- **JOB**: 16 instances
- **JOB_APPLICATION**: 45 instances
- **APPOINTMENT**: 25 instances (with various statuses)

## Data Design Notes

The sample data is designed to ensure all Part 2 queries return non-empty results:

1. **Accepted appointments**: Multiple appointments with `status = 'confirmed'`
2. **Jobs with 'soft-spoken'**: Several jobs contain 'soft-spoken' in `other_requirements`
3. **Babysitter positions**: Multiple jobs and caregivers with `caregiving_type = 'babysitter'`
4. **Elderly Care in Astana with "No pets"**: Member 18 and 28 meet these criteria
5. **Arman Armanov**: User ID 17 (for phone number update query)
6. **Amina Aminova**: User ID 16 (has jobs 1 and 8 for deletion query)
7. **Kabanbay Batyr street**: Multiple members (18, 20, 22, 24, 26, 28, 30) live on this street

## Verification

After running the SQL files, verify the data:

```sql
-- Count records in each table
SELECT 'USER' as table_name, COUNT(*) as count FROM USER
UNION ALL
SELECT 'CAREGIVER', COUNT(*) FROM CAREGIVER
UNION ALL
SELECT 'MEMBER', COUNT(*) FROM MEMBER
UNION ALL
SELECT 'ADDRESS', COUNT(*) FROM ADDRESS
UNION ALL
SELECT 'JOB', COUNT(*) FROM JOB
UNION ALL
SELECT 'JOB_APPLICATION', COUNT(*) FROM JOB_APPLICATION
UNION ALL
SELECT 'APPOINTMENT', COUNT(*) FROM APPOINTMENT;
```

All tables should have at least 10 instances.

## Export for Submission

To export the database for submission:

```bash
pg_dump -d caregiver_platform > caregiver_platform.sql
```

This creates a `.sql` file that can be submitted as required.

