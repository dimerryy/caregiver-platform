# Part 3: Flask Web Application with CRUD Operations

## Overview
This part implements a Flask web application that provides CRUD (Create, Read, Update, Delete) operations for all tables in the caregiver platform database.

## Files
- `app.py` - Main Flask application with all routes
- `templates/` - HTML templates for all pages
  - `base.html` - Base template with navigation
  - `index.html` - Home page
  - `users/` - User CRUD templates
  - `caregivers/` - Caregiver CRUD templates
  - `members/` - Member CRUD templates
  - `addresses/` - Address CRUD templates
  - `jobs/` - Job CRUD templates
  - `job_applications/` - Job Application CRUD templates
  - `appointments/` - Appointment CRUD templates

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

The application uses environment variables for database configuration. You can either:

**Option A: Set environment variables**
```bash
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=caregiver_platform
export SECRET_KEY=your-secret-key-here
```

**Option B: Edit app.py directly**
Modify the connection variables at the top of `app.py`:
```python
DB_USER = 'postgres'
DB_PASSWORD = 'your_password'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'caregiver_platform'
```

### 3. Run the Application

**Development mode:**
```bash
python app.py
```

Or using Flask CLI:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

The application will be available at `http://localhost:5000`

## Features

### CRUD Operations for All Tables

1. **USER**
   - List all users
   - Create new user
   - View user details
   - Edit user
   - Delete user

2. **CAREGIVER**
   - List all caregivers (with user info)
   - Create new caregiver (requires existing user)
   - Edit caregiver
   - Delete caregiver

3. **MEMBER**
   - List all members (with user info)
   - Create new member (requires existing user)
   - Edit member
   - Delete member

4. **ADDRESS**
   - List all addresses (with member info)
   - Create new address (requires existing member)
   - Edit address
   - Delete address

5. **JOB**
   - List all jobs (with member info)
   - Create new job
   - Edit job
   - Delete job

6. **JOB_APPLICATION**
   - List all job applications (with caregiver and member info)
   - Create new job application
   - Delete job application

7. **APPOINTMENT**
   - List all appointments (with caregiver and member info)
   - Create new appointment
   - Edit appointment
   - Delete appointment

## UI Features

- **Simple, clear interface** - Focus on functionality over styling
- **Navigation bar** - Easy access to all tables
- **Flash messages** - Success and error notifications
- **Form validation** - Required fields and data types
- **Confirmation dialogs** - For delete operations
- **Responsive tables** - Easy to read and navigate

## Design Decisions

1. **Foreign Key Handling:**
   - When creating CAREGIVER or MEMBER, users can only select from users who aren't already caregivers/members
   - When creating ADDRESS, users can only select from members who don't have addresses yet
   - Dropdowns show user/member names for better UX

2. **Data Display:**
   - Lists show key information in tables
   - Long text fields are truncated in list views
   - Full details available in view/edit pages

3. **Error Handling:**
   - Database errors are caught and displayed as flash messages
   - Transactions are rolled back on errors
   - User-friendly error messages

## Deployment

### PythonAnywhere

1. Create a free account at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your files via the Files tab
3. Create a new web app
4. Configure:
   - Source code: `/home/yourusername/mysite/app.py`
   - Working directory: `/home/yourusername/mysite`
5. Set environment variables in the web app configuration
6. Install dependencies in the Bash console:
   ```bash
   pip3.10 install --user flask sqlalchemy psycopg2-binary
   ```
7. Reload the web app

### Render

1. Create a new Web Service on [render.com](https://render.com)
2. Connect your GitHub repository
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. Add environment variables in the dashboard
5. Deploy

### Heroku

1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```
3. Create `runtime.txt`:
   ```
   python-3.11.0
   ```
4. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set DB_USER=... DB_PASSWORD=... DB_HOST=... DB_PORT=... DB_NAME=...
   git push heroku main
   ```

## Notes

- The application uses SQLAlchemy's Textual SQL for database operations
- All database operations are wrapped in try-except blocks for error handling
- Sessions are properly closed after each operation
- The UI is simple and functional, suitable for database management
- All table and column names match the assignment requirements exactly

## Troubleshooting

### Connection Errors
- Verify PostgreSQL is running and accessible
- Check database credentials
- Ensure the database exists

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version: `python --version` (should be 3.7+)

### Template Errors
- Ensure all template files are in the correct directories
- Check that template inheritance is correct
- Verify Jinja2 syntax

### Foreign Key Errors
- When creating CAREGIVER/MEMBER, ensure the user exists first
- When creating ADDRESS, ensure the member exists first
- Check that foreign key constraints are satisfied

