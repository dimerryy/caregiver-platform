"""
CSCI 341 Assignment 3 - Part 2
Python + SQLAlchemy Database Operations
Caregiver Platform Database

This script executes all required database operations:
- Create tables with PKs and FKs
- Insert sample data
- Update operations
- Delete operations
- Simple queries (4)
- Complex queries (4)
- Derived attribute query
- View operation
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path

# Database connection configuration
# Update these values according to your PostgreSQL setup
DB_USER = os.getenv('DB_USER', 'dimerryy')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'caregiver_platform')

# Create database connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine and session
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def read_sql_file(file_path):
    """Read SQL file and return its contents"""
    sql_file = Path(file_path)
    if not sql_file.exists():
        raise FileNotFoundError(f"SQL file not found: {file_path}")
    return sql_file.read_text(encoding='utf-8')


def execute_sql_file(file_path, description=""):
    """Execute SQL statements from a file"""
    if description:
        print(f"{description}")
    sql_content = read_sql_file(file_path)
    
    # Remove comments (lines starting with --) and empty lines
    lines = []
    for line in sql_content.split('\n'):
        stripped = line.strip()
        # Skip comment-only lines and empty lines
        if stripped and not stripped.startswith('--'):
            lines.append(line)
    
    # Rejoin and split by semicolon to get individual statements
    cleaned_sql = '\n'.join(lines)
    statements = [stmt.strip() for stmt in cleaned_sql.split(';') if stmt.strip()]
    
    try:
        for statement in statements:
            if statement:  # Skip empty statements
                # Execute each statement
                session.execute(text(statement))
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise Exception(f"Error executing SQL file {file_path}: {e}")


def print_section(title):
    """Helper function to print section headers"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def execute_and_print(query, description):
    """Helper function to execute query and print results"""
    print(f"\n{description}")
    print("-" * 80)
    try:
        result = session.execute(text(query))
        rows = result.fetchall()
        
        if rows:
            # Print column names
            if result.description:
                columns = [desc[0] for desc in result.description]
                print(" | ".join(str(col).ljust(20) for col in columns))
                print("-" * 80)
            
            # Print rows
            for row in rows:
                print(" | ".join(str(val).ljust(20) for val in row))
            print(f"\nTotal rows: {len(rows)}")
        else:
            print("No results found.")
    except Exception as e:
        print(f"Error: {e}")
    print()


# ============================================================================
# 1. CREATE TABLES
# ============================================================================

def create_tables():
    """Create all tables with primary keys and foreign keys"""
    print_section("1. CREATING TABLES")
    
    try:
        # Read and execute schema.sql file
        schema_file = Path(__file__).parent / "schema.sql"
        execute_sql_file(schema_file, "Loading schema from schema.sql...")
        print("✓ All tables created successfully!")
    except Exception as e:
        session.rollback()
        print(f"✗ Error creating tables: {e}")
        raise


# ============================================================================
# 2. INSERT SAMPLE DATA
# ============================================================================

def insert_sample_data():
    """Insert sample data into all tables"""
    print_section("2. INSERTING SAMPLE DATA")
    
    try:
        # Read and execute sample_data.sql file
        sample_data_file = Path(__file__).parent / "sample_data.sql"
        execute_sql_file(sample_data_file, "Loading sample data from sample_data.sql...")
        print("✓ Sample data inserted successfully!")
    except Exception as e:
        session.rollback()
        print(f"✗ Error inserting data: {e}")
        raise


# ============================================================================
# 3. UPDATE OPERATIONS
# ============================================================================

def update_operations():
    """Execute update operations"""
    print_section("3. UPDATE OPERATIONS")
    
    # 3.1 Update phone number of Arman Armanov
    print("\n3.1 Updating phone number of Arman Armanov to +77773414141")
    update_phone_query = """
    UPDATE "USER"
    SET phone_number = '+77773414141'
    WHERE given_name = 'Arman' AND surname = 'Armanov';
    """
    try:
        result = session.execute(text(update_phone_query))
        session.commit()
        print(f"✓ Updated {result.rowcount} row(s)")
        
        # Verify the update
        verify_query = """
        SELECT user_id, given_name, surname, phone_number
        FROM "USER"
        WHERE given_name = 'Arman' AND surname = 'Armanov';
        """
        execute_and_print(verify_query, "Verification - Arman Armanov's phone number:")
    except Exception as e:
        session.rollback()
        print(f"✗ Error updating phone number: {e}")
    
    # 3.2 Add commission to hourly rates
    print("\n3.2 Adding commission fee to Caregivers' hourly rates")
    print("    - If hourly_rate < $10: add $0.3")
    print("    - If hourly_rate >= $10: add 10%")
    update_commission_query = """
    UPDATE CAREGIVER
    SET hourly_rate = CASE
        WHEN hourly_rate < 10 THEN hourly_rate + 0.3
        ELSE hourly_rate * 1.10
    END;
    """
    try:
        result = session.execute(text(update_commission_query))
        session.commit()
        print(f"✓ Updated {result.rowcount} caregiver(s)")
        
        # Show updated rates
        verify_query = """
        SELECT caregiver_user_id, 
               u.given_name || ' ' || u.surname AS caregiver_name,
               caregiving_type,
               hourly_rate
        FROM CAREGIVER c
        JOIN "USER" u ON c.caregiver_user_id = u.user_id
        ORDER BY caregiver_user_id;
        """
        execute_and_print(verify_query, "Verification - Updated hourly rates:")
    except Exception as e:
        session.rollback()
        print(f"✗ Error updating commission: {e}")


# ============================================================================
# 4. DELETE OPERATIONS
# ============================================================================

def delete_operations():
    """Execute delete operations"""
    print_section("4. DELETE OPERATIONS")
    
    # 4.1 Delete jobs posted by Amina Aminova
    print("\n4.1 Deleting jobs posted by Amina Aminova")
    delete_jobs_query = """
    DELETE FROM JOB
    WHERE member_user_id IN (
        SELECT member_user_id
        FROM MEMBER m
        JOIN "USER" u ON m.member_user_id = u.user_id
        WHERE u.given_name = 'Amina' AND u.surname = 'Aminova'
    );
    """
    try:
        result = session.execute(text(delete_jobs_query))
        session.commit()
        print(f"✓ Deleted {result.rowcount} job(s)")
        
        # Verify deletion
        verify_query = """
        SELECT j.job_id, u.given_name, u.surname, j.required_caregiving_type
        FROM JOB j
        JOIN MEMBER m ON j.member_user_id = m.member_user_id
        JOIN "USER" u ON m.member_user_id = u.user_id
        WHERE u.given_name = 'Amina' AND u.surname = 'Aminova';
        """
        execute_and_print(verify_query, "Verification - Remaining jobs by Amina Aminova:")
    except Exception as e:
        session.rollback()
        print(f"✗ Error deleting jobs: {e}")
    
    # 4.2 Delete members who live on Kabanbay Batyr street
    print("\n4.2 Deleting members who live on Kabanbay Batyr street")
    delete_members_query = """
    DELETE FROM MEMBER
    WHERE member_user_id IN (
        SELECT a.member_user_id
        FROM ADDRESS a
        WHERE a.street = 'Kabanbay Batyr Avenue'
    );
    """
    try:
        result = session.execute(text(delete_members_query))
        session.commit()
        print(f"✓ Deleted {result.rowcount} member(s)")
        
        # Verify deletion
        verify_query = """
        SELECT m.member_user_id, u.given_name, u.surname, a.street
        FROM MEMBER m
        JOIN "USER" u ON m.member_user_id = u.user_id
        LEFT JOIN ADDRESS a ON m.member_user_id = a.member_user_id
        WHERE a.street = 'Kabanbay Batyr Avenue';
        """
        execute_and_print(verify_query, "Verification - Remaining members on Kabanbay Batyr Avenue:")
    except Exception as e:
        session.rollback()
        print(f"✗ Error deleting members: {e}")


# ============================================================================
# 5. SIMPLE QUERIES
# ============================================================================

def simple_queries():
    """Execute simple queries"""
    print_section("5. SIMPLE QUERIES")
    
    # 5.1 Select caregiver and member names for accepted appointments
    query_5_1 = """
    SELECT 
        u1.given_name || ' ' || u1.surname AS caregiver_name,
        u2.given_name || ' ' || u2.surname AS member_name,
        a.appointment_date,
        a.appointment_time,
        a.work_hours
    FROM APPOINTMENT a
    JOIN CAREGIVER c ON a.caregiver_user_id = c.caregiver_user_id
    JOIN "USER" u1 ON c.caregiver_user_id = u1.user_id
    JOIN MEMBER m ON a.member_user_id = m.member_user_id
    JOIN "USER" u2 ON m.member_user_id = u2.user_id
    WHERE a.status = 'confirmed'
    ORDER BY a.appointment_date, a.appointment_time;
    """
    execute_and_print(query_5_1, "5.1 Caregiver and member names for accepted appointments:")
    
    # 5.2 List job ids that contain 'soft-spoken' in their other requirements
    query_5_2 = """
    SELECT job_id, required_caregiving_type, other_requirements
    FROM JOB
    WHERE other_requirements ILIKE '%soft-spoken%'
    ORDER BY job_id;
    """
    execute_and_print(query_5_2, "5.2 Job IDs containing 'soft-spoken' in other requirements:")
    
    # 5.3 List the work hours of all babysitter positions
    # Note: "babysitter positions" likely refers to appointments with babysitter caregivers
    query_5_3 = """
    SELECT 
        a.appointment_id,
        u.given_name || ' ' || u.surname AS caregiver_name,
        a.appointment_date,
        a.work_hours,
        a.status
    FROM APPOINTMENT a
    JOIN CAREGIVER c ON a.caregiver_user_id = c.caregiver_user_id
    JOIN "USER" u ON c.caregiver_user_id = u.user_id
    WHERE c.caregiving_type = 'babysitter'
    ORDER BY a.appointment_date;
    """
    execute_and_print(query_5_3, "5.3 Work hours of all babysitter positions:")
    
    # 5.4 List members looking for Elderly Care in Astana with "No pets." rule
    query_5_4 = """
    SELECT 
        u.user_id,
        u.given_name || ' ' || u.surname AS member_name,
        u.city,
        m.house_rules,
        j.job_id,
        j.required_caregiving_type
    FROM MEMBER m
    JOIN "USER" u ON m.member_user_id = u.user_id
    JOIN JOB j ON m.member_user_id = j.member_user_id
    WHERE u.city = 'Astana'
      AND j.required_caregiving_type = 'elderly care'
      AND m.house_rules ILIKE '%No pets%'
    ORDER BY u.surname, u.given_name;
    """
    execute_and_print(query_5_4, "5.4 Members looking for Elderly Care in Astana with 'No pets' rule:")


# ============================================================================
# 6. COMPLEX QUERIES
# ============================================================================

def complex_queries():
    """Execute complex queries with joins and aggregations"""
    print_section("6. COMPLEX QUERIES")
    
    # 6.1 Count the number of applicants for each job posted by a member
    query_6_1 = """
    SELECT 
        j.job_id,
        u.given_name || ' ' || u.surname AS member_name,
        j.required_caregiving_type,
        COUNT(ja.caregiver_user_id) AS number_of_applicants
    FROM JOB j
    JOIN MEMBER m ON j.member_user_id = m.member_user_id
    JOIN "USER" u ON m.member_user_id = u.user_id
    LEFT JOIN JOB_APPLICATION ja ON j.job_id = ja.job_id
    GROUP BY j.job_id, u.given_name, u.surname, j.required_caregiving_type
    ORDER BY number_of_applicants DESC, j.job_id;
    """
    execute_and_print(query_6_1, "6.1 Number of applicants for each job:")
    
    # 6.2 Total hours spent by caregivers for all accepted appointments
    query_6_2 = """
    SELECT 
        c.caregiver_user_id,
        u.given_name || ' ' || u.surname AS caregiver_name,
        c.caregiving_type,
        SUM(a.work_hours) AS total_hours
    FROM APPOINTMENT a
    JOIN CAREGIVER c ON a.caregiver_user_id = c.caregiver_user_id
    JOIN "USER" u ON c.caregiver_user_id = u.user_id
    WHERE a.status = 'confirmed'
    GROUP BY c.caregiver_user_id, u.given_name, u.surname, c.caregiving_type
    ORDER BY total_hours DESC;
    """
    execute_and_print(query_6_2, "6.2 Total hours spent by caregivers for accepted appointments:")
    
    # 6.3 Average pay of caregivers based on accepted appointments
    # Average pay = average of (hourly_rate * work_hours) for each appointment
    query_6_3 = """
    SELECT 
        c.caregiver_user_id,
        u.given_name || ' ' || u.surname AS caregiver_name,
        c.caregiving_type,
        ROUND(AVG(c.hourly_rate * a.work_hours), 2) AS average_pay_per_appointment
    FROM APPOINTMENT a
    JOIN CAREGIVER c ON a.caregiver_user_id = c.caregiver_user_id
    JOIN "USER" u ON c.caregiver_user_id = u.user_id
    WHERE a.status = 'confirmed'
    GROUP BY c.caregiver_user_id, u.given_name, u.surname, c.caregiving_type
    ORDER BY average_pay_per_appointment DESC;
    """
    execute_and_print(query_6_3, "6.3 Average pay of caregivers based on accepted appointments:")
    
    # 6.4 Caregivers who earn above average based on accepted appointments
    # This requires a nested query to calculate the overall average first
    query_6_4 = """
    WITH caregiver_earnings AS (
        SELECT 
            c.caregiver_user_id,
            u.given_name || ' ' || u.surname AS caregiver_name,
            c.caregiving_type,
            AVG(c.hourly_rate * a.work_hours) AS avg_earnings
        FROM APPOINTMENT a
        JOIN CAREGIVER c ON a.caregiver_user_id = c.caregiver_user_id
        JOIN "USER" u ON c.caregiver_user_id = u.user_id
        WHERE a.status = 'confirmed'
        GROUP BY c.caregiver_user_id, u.given_name, u.surname, c.caregiving_type
    ),
    overall_avg AS (
        SELECT AVG(avg_earnings) AS overall_average
        FROM caregiver_earnings
    )
    SELECT 
        ce.caregiver_user_id,
        ce.caregiver_name,
        ce.caregiving_type,
        ROUND(ce.avg_earnings, 2) AS average_earnings,
        ROUND(oa.overall_average, 2) AS overall_average
    FROM caregiver_earnings ce
    CROSS JOIN overall_avg oa
    WHERE ce.avg_earnings > oa.overall_average
    ORDER BY ce.avg_earnings DESC;
    """
    execute_and_print(query_6_4, "6.4 Caregivers earning above average based on accepted appointments:")


# ============================================================================
# 7. DERIVED ATTRIBUTE QUERY
# ============================================================================

def derived_attribute_query():
    """Calculate total cost for all accepted appointments"""
    print_section("7. DERIVED ATTRIBUTE QUERY")
    
    query = """
    SELECT 
        SUM(c.hourly_rate * a.work_hours) AS total_cost
    FROM APPOINTMENT a
    JOIN CAREGIVER c ON a.caregiver_user_id = c.caregiver_user_id
    WHERE a.status = 'confirmed';
    """
    execute_and_print(query, "7. Total cost to pay for caregivers for all accepted appointments:")


# ============================================================================
# 8. VIEW OPERATION
# ============================================================================

def view_operation():
    """Create and query a view for job applications"""
    print_section("8. VIEW OPERATION")
    
    # Create view
    create_view_query = """
    CREATE OR REPLACE VIEW job_applications_view AS
    SELECT 
        ja.job_id,
        j.required_caregiving_type,
        j.other_requirements,
        j.date_posted,
        u_member.given_name || ' ' || u_member.surname AS member_name,
        ja.caregiver_user_id,
        u_caregiver.given_name || ' ' || u_caregiver.surname AS applicant_name,
        c.caregiving_type AS applicant_caregiving_type,
        c.hourly_rate,
        ja.date_applied
    FROM JOB_APPLICATION ja
    JOIN JOB j ON ja.job_id = j.job_id
    JOIN MEMBER m ON j.member_user_id = m.member_user_id
    JOIN "USER" u_member ON m.member_user_id = u_member.user_id
    JOIN CAREGIVER c ON ja.caregiver_user_id = c.caregiver_user_id
    JOIN "USER" u_caregiver ON c.caregiver_user_id = u_caregiver.user_id
    ORDER BY ja.job_id, ja.date_applied;
    """
    
    try:
        session.execute(text(create_view_query))
        session.commit()
        print("✓ View 'job_applications_view' created successfully!")
    except Exception as e:
        session.rollback()
        print(f"✗ Error creating view: {e}")
        return
    
    # Query the view
    query_view = """
    SELECT * FROM job_applications_view;
    """
    execute_and_print(query_view, "8. View: All job applications and applicants:")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function to execute all operations"""
    print("\n" + "="*80)
    print("  CSCI 341 Assignment 3 - Part 2: Python + SQLAlchemy Operations")
    print("  Caregiver Platform Database")
    print("="*80)
    
    try:
        # Test database connection
        session.execute(text("SELECT 1"))
        print("\n✓ Database connection successful!\n")
        
        # Execute all operations in order
        create_tables()
        insert_sample_data()
        update_operations()
        delete_operations()
        simple_queries()
        complex_queries()
        derived_attribute_query()
        view_operation()
        
        print_section("EXECUTION COMPLETE")
        print("✓ All operations executed successfully!")
        
    except Exception as e:
        print(f"\n✗ Error during execution: {e}")
        session.rollback()
        raise
    finally:
        session.close()
        engine.dispose()


if __name__ == "__main__":
    main()

