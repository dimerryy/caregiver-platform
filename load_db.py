"""
Script to load database schema into external PostgreSQL database
Use this if you're deploying to PythonAnywhere with ElephantSQL or similar
"""

from sqlalchemy import create_engine, text
import sys

# Get database URL from command line or update here
if len(sys.argv) > 1:
    DATABASE_URL = sys.argv[1]
else:
    # Update these with your database credentials
    # For Supabase: user='postgres', host='db.xxxxx.supabase.co', db='postgres'
    # For Neon: check your Neon dashboard for credentials
    # For Render: check your Render dashboard for credentials
    DB_USER = os.getenv('DB_USER', 'dimerryy')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'caregiver_platform')
    
    # Render requires SSL, so add sslmode=require
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"

print("Connecting to database...")
engine = create_engine(DATABASE_URL)

try:
    # Read database.sql file
    with open('database.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Remove comments and split by semicolon
    lines = []
    for line in sql_content.split('\n'):
        stripped = line.strip()
        if stripped and not stripped.startswith('--'):
            lines.append(line)
    
    cleaned_sql = '\n'.join(lines)
    statements = [stmt.strip() for stmt in cleaned_sql.split(';') if stmt.strip()]
    
    print(f"Executing {len(statements)} SQL statements...")
    
    with engine.connect() as conn:
        for i, statement in enumerate(statements, 1):
            if statement:
                try:
                    conn.execute(text(statement))
                    if i % 10 == 0:
                        print(f"  Processed {i}/{len(statements)} statements...")
                except Exception as e:
                    print(f"  Warning on statement {i}: {e}")
        conn.commit()
    
    print("✓ Database schema loaded successfully!")
    
    # Verify tables were created
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """))
        tables = [row[0] for row in result]
        print(f"\n✓ Created {len(tables)} tables:")
        for table in tables:
            print(f"  - {table}")
    
except FileNotFoundError:
    print("Error: database.sql file not found!")
    print("Make sure database.sql is in the same directory.")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

