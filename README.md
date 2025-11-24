# CSCI 341 Assignment 3 - Caregiver Platform

A complete database management system for matching caregivers with families, implemented in three parts:
- **Part 1**: PostgreSQL database schema and sample data
- **Part 2**: Python + SQLAlchemy operations script
- **Part 3**: Flask web application with CRUD operations

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create and setup database
createdb caregiver_platform
psql -d caregiver_platform -f database.sql

# 3. Set database credentials in main.py and app.py

# 4. Test Part 2
python3 main.py

# 5. Run Part 3 (web app)
python3 app.py
# Visit http://localhost:5001
```

## Project Structure

```
db/
├── app.py                 # Part 3: Flask web application
├── main.py                # Part 2: Python + SQLAlchemy script
├── schema.sql             # Database schema
├── sample_data.sql        # Sample data
├── database.sql           # Combined schema + data
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates for web app
├── README_Part1.md        # Part 1 documentation
├── README_Part2.md        # Part 2 documentation
├── README_Part3.md        # Part 3 documentation
└── DEPLOYMENT_GUIDE.md    # Deployment instructions
```

## Documentation

- **Setup & Testing**: See `RUN_AND_TEST.md`
- **Deployment**: See `DEPLOYMENT_GUIDE.md` or `PYTHONANYWHERE_SETUP.md`
- **Requirements Verification**: See `REQUIREMENTS_VERIFICATION.md`

## Database

- **System**: PostgreSQL
- **Tables**: 7 tables (USER, CAREGIVER, MEMBER, ADDRESS, JOB, JOB_APPLICATION, APPOINTMENT)
- **Sample Data**: 30+ users, 15+ records per table

## Technologies

- Python 3.12
- PostgreSQL
- SQLAlchemy
- Flask
- HTML/CSS (templates)

## License

Academic project for CSCI 341 Database Management Systems.

