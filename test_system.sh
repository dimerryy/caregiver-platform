#!/bin/bash

echo "=== Testing Caregiver Platform System ==="
echo ""

# Test 1: Database exists
echo "1. Checking database..."
if psql -l 2>/dev/null | grep -q caregiver_platform; then
    echo "   ✓ Database 'caregiver_platform' exists"
else
    echo "   ✗ Database 'caregiver_platform' not found"
    echo "      Run: createdb caregiver_platform"
fi
echo ""

# Test 2: Tables exist
echo "2. Checking tables..."
if psql -d caregiver_platform -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';" 2>/dev/null | grep -q '[0-9]'; then
    TABLE_COUNT=$(psql -d caregiver_platform -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';" 2>/dev/null | tr -d ' ')
    if [ "$TABLE_COUNT" -ge 7 ]; then
        echo "   ✓ Found $TABLE_COUNT tables (expected 7+)"
    else
        echo "   ✗ Only found $TABLE_COUNT tables (expected 7+)"
    fi
else
    echo "   ✗ Could not connect to database or tables not found"
fi
echo ""

# Test 3: Python dependencies
echo "3. Checking Python dependencies..."
if python3 -c "import sqlalchemy; import flask; import psycopg2" 2>/dev/null; then
    echo "   ✓ All dependencies installed"
    python3 -c "import sqlalchemy; print('      SQLAlchemy:', sqlalchemy.__version__)" 2>/dev/null
    python3 -c "import flask; print('      Flask:', flask.__version__)" 2>/dev/null
else
    echo "   ✗ Missing dependencies"
    echo "      Run: pip3 install -r requirements.txt"
fi
echo ""

# Test 4: Part 2 script
echo "4. Testing Part 2 script (main.py)..."
if python3 -c "import main" 2>/dev/null; then
    echo "   ✓ main.py imports successfully"
else
    echo "   ✗ main.py has import errors"
    python3 -c "import main" 2>&1 | head -3
fi
echo ""

# Test 5: Part 3 app
echo "5. Testing Part 3 app (app.py)..."
if python3 -c "import app" 2>/dev/null; then
    echo "   ✓ app.py imports successfully"
else
    echo "   ✗ app.py has import errors"
    python3 -c "import app" 2>&1 | head -3
fi
echo ""

# Test 6: Check required files
echo "6. Checking required files..."
REQUIRED_FILES=("schema.sql" "sample_data.sql" "database.sql" "main.py" "app.py" "requirements.txt")
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file exists"
    else
        echo "   ✗ $file missing"
    fi
done
echo ""

# Test 7: Check templates directory
echo "7. Checking templates..."
if [ -d "templates" ] && [ "$(ls -A templates 2>/dev/null)" ]; then
    TEMPLATE_COUNT=$(find templates -name "*.html" | wc -l | tr -d ' ')
    echo "   ✓ Found $TEMPLATE_COUNT HTML templates"
else
    echo "   ✗ Templates directory missing or empty"
fi
echo ""

echo "=== Test Complete ==="
echo ""
echo "Next steps:"
echo "1. Ensure database is set up: psql -d caregiver_platform -f database.sql"
echo "2. Set environment variables for database connection"
echo "3. Test Part 2: python3 main.py"
echo "4. Test Part 3: python3 app.py (then visit http://localhost:5000)"

