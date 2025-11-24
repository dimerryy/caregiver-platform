"""
Load database schema into Render PostgreSQL database
This script handles SSL requirements automatically
"""

from sqlalchemy import create_engine, text
import sys
import os

# Get database URL from command line or environment
if len(sys.argv) > 1:
    DATABASE_URL = sys.argv[1]
    # Add SSL if not present and it's a Render URL
    if 'render.com' in DATABASE_URL and 'sslmode' not in DATABASE_URL:
        if '?' in DATABASE_URL:
            DATABASE_URL += '&sslmode=require'
        else:
            DATABASE_URL += '?sslmode=require'
else:
    # Get from environment variables
    DB_USER = os.getenv('DB_USER', '')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_HOST = os.getenv('DB_HOST', '')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', '')
    
    if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
        print("Error: Database credentials not provided")
        print("Usage: python3 load_render_db.py 'postgresql://user:pass@host:port/db'")
        print("Or set environment variables: DB_USER, DB_PASSWORD, DB_HOST, DB_NAME")
        sys.exit(1)
    
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    # Render requires SSL
    if 'render.com' in DB_HOST:
        DATABASE_URL += '?sslmode=require'

print("Connecting to database...")
print(f"Host: {DB_HOST if 'DB_HOST' in locals() else 'from URL'}")

# Create engine with SSL for Render
connect_args = {}
if 'render.com' in DATABASE_URL:
    connect_args = {'sslmode': 'require'}

try:
    engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)
    
    # Test connection
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("✓ Database connection successful!")
    
    # Read database.sql file
    print("Reading database.sql...")
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
    
    with engine.begin() as conn:  # Use begin() for transaction
        for i, statement in enumerate(statements, 1):
            if statement:
                try:
                    conn.execute(text(statement))
                    if i % 10 == 0:
                        print(f"  Processed {i}/{len(statements)} statements...")
                except Exception as e:
                    # Some errors are expected (like DROP TABLE IF EXISTS)
                    if 'does not exist' not in str(e).lower():
                        print(f"  Warning on statement {i}: {e}")
    
    print("✓ Database schema loaded successfully!")
    
    # Verify tables were created
    print("\nVerifying tables...")
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """))
        tables = [row[0] for row in result]
        print(f"✓ Created {len(tables)} tables:")
        for table in tables:
            print(f"  - {table}")
        
        # Count records
        print("\nRecord counts:")
        for table in tables:
            try:
                result = conn.execute(text(f'SELECT COUNT(*) FROM "{table}"'))
                count = result.scalar()
                print(f"  {table}: {count} records")
            except:
                pass
    
except FileNotFoundError:
    print("Error: database.sql file not found!")
    print("Make sure database.sql is in the same directory.")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ Database setup complete!")

