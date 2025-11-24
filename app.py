"""
CSCI 341 Assignment 3 - Part 3
Flask Web Application with CRUD Operations
Caregiver Platform Database

This application provides CRUD (Create, Read, Update, Delete) operations
for all tables in the caregiver platform database.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database connection configuration
DB_USER = os.getenv('DB_USER', 'dimerryy')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'caregiver_platform')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine and session factory
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)


def get_db_session():
    """Get a database session"""
    return Session()


# ============================================================================
# HOME PAGE
# ============================================================================

@app.route('/')
def index():
    """Home page with links to all tables"""
    return render_template('index.html')


# ============================================================================
# USER CRUD OPERATIONS
# ============================================================================

@app.route('/users')
def list_users():
    """List all users"""
    session = get_db_session()
    try:
        result = session.execute(text('SELECT * FROM "USER" ORDER BY user_id'))
        users = [dict(row._mapping) for row in result]
        return render_template('users/list.html', users=users)
    except Exception as e:
        flash(f'Error loading users: {str(e)}', 'error')
        return render_template('users/list.html', users=[])
    finally:
        session.close()


@app.route('/users/create', methods=['GET', 'POST'])
def create_user():
    """Create a new user"""
    if request.method == 'POST':
        session = get_db_session()
        try:
            query = text("""
                INSERT INTO "USER" (email, given_name, surname, city, phone_number, profile_description, password)
                VALUES (:email, :given_name, :surname, :city, :phone_number, :profile_description, :password)
            """)
            session.execute(query, {
                'email': request.form['email'],
                'given_name': request.form['given_name'],
                'surname': request.form['surname'],
                'city': request.form['city'],
                'phone_number': request.form['phone_number'],
                'profile_description': request.form.get('profile_description', ''),
                'password': request.form['password']
            })
            session.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('list_users'))
        except Exception as e:
            session.rollback()
            flash(f'Error creating user: {str(e)}', 'error')
        finally:
            session.close()
    
    return render_template('users/create.html')


@app.route('/users/<int:user_id>')
def view_user(user_id):
    """View a specific user"""
    session = get_db_session()
    try:
        result = session.execute(
            text('SELECT * FROM "USER" WHERE user_id = :user_id'),
            {'user_id': user_id}
        )
        user = result.fetchone()
        if user:
            return render_template('users/view.html', user=dict(user._mapping))
        else:
            flash('User not found', 'error')
            return redirect(url_for('list_users'))
    finally:
        session.close()


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Edit a user"""
    session = get_db_session()
    try:
        if request.method == 'POST':
            query = text("""
                UPDATE "USER"
                SET email = :email, given_name = :given_name, surname = :surname,
                    city = :city, phone_number = :phone_number,
                    profile_description = :profile_description, password = :password
                WHERE user_id = :user_id
            """)
            session.execute(query, {
                'user_id': user_id,
                'email': request.form['email'],
                'given_name': request.form['given_name'],
                'surname': request.form['surname'],
                'city': request.form['city'],
                'phone_number': request.form['phone_number'],
                'profile_description': request.form.get('profile_description', ''),
                'password': request.form['password']
            })
            session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('view_user', user_id=user_id))
        
        result = session.execute(
            text('SELECT * FROM "USER" WHERE user_id = :user_id'),
            {'user_id': user_id}
        )
        user = result.fetchone()
        if user:
            return render_template('users/edit.html', user=dict(user._mapping))
        else:
            flash('User not found', 'error')
            return redirect(url_for('list_users'))
    except Exception as e:
        session.rollback()
        flash(f'Error updating user: {str(e)}', 'error')
    finally:
        session.close()


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a user"""
    session = get_db_session()
    try:
        session.execute(
            text('DELETE FROM "USER" WHERE user_id = :user_id'),
            {'user_id': user_id}
        )
        session.commit()
        flash('User deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_users'))


# ============================================================================
# CAREGIVER CRUD OPERATIONS
# ============================================================================

@app.route('/caregivers')
def list_caregivers():
    """List all caregivers with user information"""
    session = get_db_session()
    try:
        query = text("""
            SELECT c.*, u.given_name, u.surname, u.email, u.city, u.phone_number
            FROM CAREGIVER c
            JOIN "USER" u ON c.caregiver_user_id = u.user_id
            ORDER BY c.caregiver_user_id
        """)
        result = session.execute(query)
        caregivers = [dict(row._mapping) for row in result]
        return render_template('caregivers/list.html', caregivers=caregivers)
    finally:
        session.close()


@app.route('/caregivers/create', methods=['GET', 'POST'])
def create_caregiver():
    """Create a new caregiver (user must exist first)"""
    session = get_db_session()
    try:
        if request.method == 'POST':
            query = text("""
                INSERT INTO CAREGIVER (caregiver_user_id, photo, gender, caregiving_type, hourly_rate)
                VALUES (:caregiver_user_id, :photo, :gender, :caregiving_type, :hourly_rate)
            """)
            session.execute(query, {
                'caregiver_user_id': int(request.form['caregiver_user_id']),
                'photo': request.form.get('photo', ''),
                'gender': request.form['gender'],
                'caregiving_type': request.form['caregiving_type'],
                'hourly_rate': float(request.form['hourly_rate'])
            })
            session.commit()
            flash('Caregiver created successfully!', 'success')
            return redirect(url_for('list_caregivers'))
        
        # Get list of users who are not already caregivers
        users_query = text("""
            SELECT u.user_id, u.given_name || ' ' || u.surname AS name
            FROM "USER" u
            LEFT JOIN CAREGIVER c ON u.user_id = c.caregiver_user_id
            WHERE c.caregiver_user_id IS NULL
            ORDER BY u.user_id
        """)
        users_result = session.execute(users_query)
        available_users = [dict(row._mapping) for row in users_result]
        return render_template('caregivers/create.html', available_users=available_users)
    except Exception as e:
        session.rollback()
        flash(f'Error: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_caregivers'))


@app.route('/caregivers/<int:caregiver_id>/edit', methods=['GET', 'POST'])
def edit_caregiver(caregiver_id):
    """Edit a caregiver"""
    session = get_db_session()
    try:
        if request.method == 'POST':
            query = text("""
                UPDATE CAREGIVER
                SET photo = :photo, gender = :gender, caregiving_type = :caregiving_type,
                    hourly_rate = :hourly_rate
                WHERE caregiver_user_id = :caregiver_user_id
            """)
            session.execute(query, {
                'caregiver_user_id': caregiver_id,
                'photo': request.form.get('photo', ''),
                'gender': request.form['gender'],
                'caregiving_type': request.form['caregiving_type'],
                'hourly_rate': float(request.form['hourly_rate'])
            })
            session.commit()
            flash('Caregiver updated successfully!', 'success')
            return redirect(url_for('list_caregivers'))
        
        query = text("""
            SELECT c.*, u.given_name, u.surname
            FROM CAREGIVER c
            JOIN "USER" u ON c.caregiver_user_id = u.user_id
            WHERE c.caregiver_user_id = :caregiver_id
        """)
        result = session.execute(query, {'caregiver_id': caregiver_id})
        caregiver = result.fetchone()
        if caregiver:
            return render_template('caregivers/edit.html', caregiver=dict(caregiver._mapping))
        else:
            flash('Caregiver not found', 'error')
            return redirect(url_for('list_caregivers'))
    except Exception as e:
        session.rollback()
        flash(f'Error: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_caregivers'))


@app.route('/caregivers/<int:caregiver_id>/delete', methods=['POST'])
def delete_caregiver(caregiver_id):
    """Delete a caregiver"""
    session = get_db_session()
    try:
        session.execute(
            text("DELETE FROM CAREGIVER WHERE caregiver_user_id = :caregiver_id"),
            {'caregiver_id': caregiver_id}
        )
        session.commit()
        flash('Caregiver deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting caregiver: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_caregivers'))


# ============================================================================
# MEMBER CRUD OPERATIONS
# ============================================================================

@app.route('/members')
def list_members():
    """List all members with user information"""
    session = get_db_session()
    try:
        query = text("""
            SELECT m.*, u.given_name, u.surname, u.email, u.city, u.phone_number
            FROM MEMBER m
            JOIN "USER" u ON m.member_user_id = u.user_id
            ORDER BY m.member_user_id
        """)
        result = session.execute(query)
        members = [dict(row._mapping) for row in result]
        return render_template('members/list.html', members=members)
    finally:
        session.close()


@app.route('/members/create', methods=['GET', 'POST'])
def create_member():
    """Create a new member (user must exist first)"""
    session = get_db_session()
    try:
        if request.method == 'POST':
            query = text("""
                INSERT INTO MEMBER (member_user_id, house_rules, dependent_description)
                VALUES (:member_user_id, :house_rules, :dependent_description)
            """)
            session.execute(query, {
                'member_user_id': int(request.form['member_user_id']),
                'house_rules': request.form.get('house_rules', ''),
                'dependent_description': request.form.get('dependent_description', '')
            })
            session.commit()
            flash('Member created successfully!', 'success')
            return redirect(url_for('list_members'))
        
        # Get list of users who are not already members
        users_query = text("""
            SELECT u.user_id, u.given_name || ' ' || u.surname AS name
            FROM "USER" u
            LEFT JOIN MEMBER m ON u.user_id = m.member_user_id
            WHERE m.member_user_id IS NULL
            ORDER BY u.user_id
        """)
        users_result = session.execute(users_query)
        available_users = [dict(row._mapping) for row in users_result]
        return render_template('members/create.html', available_users=available_users)
    except Exception as e:
        session.rollback()
        flash(f'Error: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_members'))


@app.route('/members/<int:member_id>/edit', methods=['GET', 'POST'])
def edit_member(member_id):
    """Edit a member"""
    session = get_db_session()
    try:
        if request.method == 'POST':
            query = text("""
                UPDATE MEMBER
                SET house_rules = :house_rules, dependent_description = :dependent_description
                WHERE member_user_id = :member_user_id
            """)
            session.execute(query, {
                'member_user_id': member_id,
                'house_rules': request.form.get('house_rules', ''),
                'dependent_description': request.form.get('dependent_description', '')
            })
            session.commit()
            flash('Member updated successfully!', 'success')
            return redirect(url_for('list_members'))
        
        query = text("""
            SELECT m.*, u.given_name, u.surname
            FROM MEMBER m
            JOIN "USER" u ON m.member_user_id = u.user_id
            WHERE m.member_user_id = :member_id
        """)
        result = session.execute(query, {'member_id': member_id})
        member = result.fetchone()
        if member:
            return render_template('members/edit.html', member=dict(member._mapping))
        else:
            flash('Member not found', 'error')
            return redirect(url_for('list_members'))
    except Exception as e:
        session.rollback()
        flash(f'Error: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_members'))


@app.route('/members/<int:member_id>/delete', methods=['POST'])
def delete_member(member_id):
    """Delete a member"""
    session = get_db_session()
    try:
        session.execute(
            text("DELETE FROM MEMBER WHERE member_user_id = :member_id"),
            {'member_id': member_id}
        )
        session.commit()
        flash('Member deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting member: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_members'))


# ============================================================================
# ADDRESS CRUD OPERATIONS
# ============================================================================

@app.route('/addresses')
def list_addresses():
    """List all addresses with member information"""
    session = get_db_session()
    try:
        query = text("""
            SELECT a.*, u.given_name, u.surname
            FROM ADDRESS a
            JOIN MEMBER m ON a.member_user_id = m.member_user_id
            JOIN "USER" u ON m.member_user_id = u.user_id
            ORDER BY a.member_user_id
        """)
        result = session.execute(query)
        addresses = [dict(row._mapping) for row in result]
        return render_template('addresses/list.html', addresses=addresses)
    finally:
        session.close()


@app.route('/addresses/create', methods=['GET', 'POST'])
def create_address():
    """Create a new address"""
    session = get_db_session()
    try:
        if request.method == 'POST':
            query = text("""
                INSERT INTO ADDRESS (member_user_id, house_number, street, town)
                VALUES (:member_user_id, :house_number, :street, :town)
            """)
            session.execute(query, {
                'member_user_id': int(request.form['member_user_id']),
                'house_number': request.form['house_number'],
                'street': request.form['street'],
                'town': request.form['town']
            })
            session.commit()
            flash('Address created successfully!', 'success')
            return redirect(url_for('list_addresses'))
        
        # Get list of members who don't have addresses yet
        members_query = text("""
            SELECT m.member_user_id, u.given_name || ' ' || u.surname AS name
            FROM MEMBER m
            JOIN "USER" u ON m.member_user_id = u.user_id
            LEFT JOIN ADDRESS a ON m.member_user_id = a.member_user_id
            WHERE a.member_user_id IS NULL
            ORDER BY m.member_user_id
        """)
        members_result = session.execute(members_query)
        available_members = [dict(row._mapping) for row in members_result]
        return render_template('addresses/create.html', available_members=available_members)
    except Exception as e:
        session.rollback()
        flash(f'Error: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_addresses'))


@app.route('/addresses/<int:member_id>/edit', methods=['GET', 'POST'])
def edit_address(member_id):
    """Edit an address"""
    session = get_db_session()
    try:
        if request.method == 'POST':
            query = text("""
                UPDATE ADDRESS
                SET house_number = :house_number, street = :street, town = :town
                WHERE member_user_id = :member_user_id
            """)
            session.execute(query, {
                'member_user_id': member_id,
                'house_number': request.form['house_number'],
                'street': request.form['street'],
                'town': request.form['town']
            })
            session.commit()
            flash('Address updated successfully!', 'success')
            return redirect(url_for('list_addresses'))
        
        query = text("""
            SELECT a.*, u.given_name, u.surname
            FROM ADDRESS a
            JOIN MEMBER m ON a.member_user_id = m.member_user_id
            JOIN "USER" u ON m.member_user_id = u.user_id
            WHERE a.member_user_id = :member_id
        """)
        result = session.execute(query, {'member_id': member_id})
        address = result.fetchone()
        if address:
            return render_template('addresses/edit.html', address=dict(address._mapping))
        else:
            flash('Address not found', 'error')
            return redirect(url_for('list_addresses'))
    except Exception as e:
        session.rollback()
        flash(f'Error: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_addresses'))


@app.route('/addresses/<int:member_id>/delete', methods=['POST'])
def delete_address(member_id):
    """Delete an address"""
    session = get_db_session()
    try:
        session.execute(
            text("DELETE FROM ADDRESS WHERE member_user_id = :member_id"),
            {'member_id': member_id}
        )
        session.commit()
        flash('Address deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting address: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_addresses'))


# ============================================================================
# JOB CRUD OPERATIONS
# ============================================================================

@app.route('/jobs')
def list_jobs():
    """List all jobs with member information"""
    session = get_db_session()
    try:
        query = text("""
            SELECT j.*, u.given_name, u.surname
            FROM JOB j
            JOIN MEMBER m ON j.member_user_id = m.member_user_id
            JOIN "USER" u ON m.member_user_id = u.user_id
            ORDER BY j.job_id
        """)
        result = session.execute(query)
        jobs = [dict(row._mapping) for row in result]
        return render_template('jobs/list.html', jobs=jobs)
    finally:
        session.close()


@app.route('/jobs/create', methods=['GET', 'POST'])
def create_job():
    """Create a new job"""
    session = get_db_session()
    try:
        if request.method == 'POST':
            query = text("""
                INSERT INTO JOB (member_user_id, required_caregiving_type, other_requirements, date_posted)
                VALUES (:member_user_id, :required_caregiving_type, :other_requirements, :date_posted)
            """)
            session.execute(query, {
                'member_user_id': int(request.form['member_user_id']),
                'required_caregiving_type': request.form['required_caregiving_type'],
                'other_requirements': request.form.get('other_requirements', ''),
                'date_posted': request.form.get('date_posted', datetime.now().date())
            })
            session.commit()
            flash('Job created successfully!', 'success')
            return redirect(url_for('list_jobs'))
        
        # Get list of members
        members_query = text("""
            SELECT m.member_user_id, u.given_name || ' ' || u.surname AS name
            FROM MEMBER m
            JOIN "USER" u ON m.member_user_id = u.user_id
            ORDER BY m.member_user_id
        """)
        members_result = session.execute(members_query)
        members = [dict(row._mapping) for row in members_result]
        return render_template('jobs/create.html', members=members)
    except Exception as e:
        session.rollback()
        flash(f'Error: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_jobs'))


@app.route('/jobs/<int:job_id>/edit', methods=['GET', 'POST'])
def edit_job(job_id):
    """Edit a job"""
    session = get_db_session()
    try:
        if request.method == 'POST':
            query = text("""
                UPDATE JOB
                SET required_caregiving_type = :required_caregiving_type,
                    other_requirements = :other_requirements,
                    date_posted = :date_posted
                WHERE job_id = :job_id
            """)
            session.execute(query, {
                'job_id': job_id,
                'required_caregiving_type': request.form['required_caregiving_type'],
                'other_requirements': request.form.get('other_requirements', ''),
                'date_posted': request.form.get('date_posted')
            })
            session.commit()
            flash('Job updated successfully!', 'success')
            return redirect(url_for('list_jobs'))
        
        query = text("""
            SELECT j.*, u.given_name, u.surname
            FROM JOB j
            JOIN MEMBER m ON j.member_user_id = m.member_user_id
            JOIN "USER" u ON m.member_user_id = u.user_id
            WHERE j.job_id = :job_id
        """)
        result = session.execute(query, {'job_id': job_id})
        job = result.fetchone()
        if job:
            job_dict = dict(job._mapping)
            # Convert date to string for form
            if job_dict.get('date_posted'):
                job_dict['date_posted'] = str(job_dict['date_posted'])
            return render_template('jobs/edit.html', job=job_dict)
        else:
            flash('Job not found', 'error')
            return redirect(url_for('list_jobs'))
    except Exception as e:
        session.rollback()
        flash(f'Error: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_jobs'))


@app.route('/jobs/<int:job_id>/delete', methods=['POST'])
def delete_job(job_id):
    """Delete a job"""
    session = get_db_session()
    try:
        session.execute(
            text("DELETE FROM JOB WHERE job_id = :job_id"),
            {'job_id': job_id}
        )
        session.commit()
        flash('Job deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting job: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_jobs'))


# ============================================================================
# JOB_APPLICATION CRUD OPERATIONS
# ============================================================================

@app.route('/job_applications')
def list_job_applications():
    """List all job applications"""
    session = get_db_session()
    try:
        query = text("""
            SELECT ja.*, 
                   u_caregiver.given_name || ' ' || u_caregiver.surname AS caregiver_name,
                   u_member.given_name || ' ' || u_member.surname AS member_name,
                   j.required_caregiving_type
            FROM JOB_APPLICATION ja
            JOIN CAREGIVER c ON ja.caregiver_user_id = c.caregiver_user_id
            JOIN "USER" u_caregiver ON c.caregiver_user_id = u_caregiver.user_id
            JOIN JOB j ON ja.job_id = j.job_id
            JOIN MEMBER m ON j.member_user_id = m.member_user_id
            JOIN "USER" u_member ON m.member_user_id = u_member.user_id
            ORDER BY ja.job_id, ja.date_applied
        """)
        result = session.execute(query)
        applications = [dict(row._mapping) for row in result]
        return render_template('job_applications/list.html', applications=applications)
    finally:
        session.close()


@app.route('/job_applications/create', methods=['GET', 'POST'])
def create_job_application():
    """Create a new job application"""
    session = get_db_session()
    try:
        if request.method == 'POST':
            query = text("""
                INSERT INTO JOB_APPLICATION (caregiver_user_id, job_id, date_applied)
                VALUES (:caregiver_user_id, :job_id, :date_applied)
            """)
            session.execute(query, {
                'caregiver_user_id': int(request.form['caregiver_user_id']),
                'job_id': int(request.form['job_id']),
                'date_applied': request.form.get('date_applied', datetime.now().date())
            })
            session.commit()
            flash('Job application created successfully!', 'success')
            return redirect(url_for('list_job_applications'))
        
        # Get caregivers and jobs
        caregivers_query = text("""
            SELECT c.caregiver_user_id, u.given_name || ' ' || u.surname AS name
            FROM CAREGIVER c
            JOIN "USER" u ON c.caregiver_user_id = u.user_id
            ORDER BY c.caregiver_user_id
        """)
        jobs_query = text("SELECT job_id, required_caregiving_type FROM JOB ORDER BY job_id")
        
        caregivers_result = session.execute(caregivers_query)
        jobs_result = session.execute(jobs_query)
        
        caregivers = [dict(row._mapping) for row in caregivers_result]
        jobs = [dict(row._mapping) for row in jobs_result]
        
        return render_template('job_applications/create.html', caregivers=caregivers, jobs=jobs)
    except Exception as e:
        session.rollback()
        flash(f'Error: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_job_applications'))


@app.route('/job_applications/<int:caregiver_id>/<int:job_id>/delete', methods=['POST'])
def delete_job_application(caregiver_id, job_id):
    """Delete a job application"""
    session = get_db_session()
    try:
        query = text("""
            DELETE FROM JOB_APPLICATION 
            WHERE caregiver_user_id = :caregiver_id AND job_id = :job_id
        """)
        session.execute(query, {
            'caregiver_id': caregiver_id,
            'job_id': job_id
        })
        session.commit()
        flash('Job application deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting job application: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_job_applications'))


# ============================================================================
# APPOINTMENT CRUD OPERATIONS
# ============================================================================

@app.route('/appointments')
def list_appointments():
    """List all appointments"""
    session = get_db_session()
    try:
        query = text("""
            SELECT a.*,
                   u_caregiver.given_name || ' ' || u_caregiver.surname AS caregiver_name,
                   u_member.given_name || ' ' || u_member.surname AS member_name
            FROM APPOINTMENT a
            JOIN CAREGIVER c ON a.caregiver_user_id = c.caregiver_user_id
            JOIN "USER" u_caregiver ON c.caregiver_user_id = u_caregiver.user_id
            JOIN MEMBER m ON a.member_user_id = m.member_user_id
            JOIN "USER" u_member ON m.member_user_id = u_member.user_id
            ORDER BY a.appointment_date, a.appointment_time
        """)
        result = session.execute(query)
        appointments = [dict(row._mapping) for row in result]
        return render_template('appointments/list.html', appointments=appointments)
    finally:
        session.close()


@app.route('/appointments/create', methods=['GET', 'POST'])
def create_appointment():
    """Create a new appointment"""
    session = get_db_session()
    try:
        if request.method == 'POST':
            query = text("""
                INSERT INTO APPOINTMENT (caregiver_user_id, member_user_id, appointment_date, 
                                        appointment_time, work_hours, status)
                VALUES (:caregiver_user_id, :member_user_id, :appointment_date,
                        :appointment_time, :work_hours, :status)
            """)
            session.execute(query, {
                'caregiver_user_id': int(request.form['caregiver_user_id']),
                'member_user_id': int(request.form['member_user_id']),
                'appointment_date': request.form['appointment_date'],
                'appointment_time': request.form['appointment_time'],
                'work_hours': float(request.form['work_hours']),
                'status': request.form['status']
            })
            session.commit()
            flash('Appointment created successfully!', 'success')
            return redirect(url_for('list_appointments'))
        
        # Get caregivers and members
        caregivers_query = text("""
            SELECT c.caregiver_user_id, u.given_name || ' ' || u.surname AS name
            FROM CAREGIVER c
            JOIN "USER" u ON c.caregiver_user_id = u.user_id
            ORDER BY c.caregiver_user_id
        """)
        members_query = text("""
            SELECT m.member_user_id, u.given_name || ' ' || u.surname AS name
            FROM MEMBER m
            JOIN "USER" u ON m.member_user_id = u.user_id
            ORDER BY m.member_user_id
        """)
        
        caregivers_result = session.execute(caregivers_query)
        members_result = session.execute(members_query)
        
        caregivers = [dict(row._mapping) for row in caregivers_result]
        members = [dict(row._mapping) for row in members_result]
        
        return render_template('appointments/create.html', caregivers=caregivers, members=members)
    except Exception as e:
        session.rollback()
        flash(f'Error: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_appointments'))


@app.route('/appointments/<int:appointment_id>/edit', methods=['GET', 'POST'])
def edit_appointment(appointment_id):
    """Edit an appointment"""
    session = get_db_session()
    try:
        if request.method == 'POST':
            query = text("""
                UPDATE APPOINTMENT
                SET caregiver_user_id = :caregiver_user_id,
                    member_user_id = :member_user_id,
                    appointment_date = :appointment_date,
                    appointment_time = :appointment_time,
                    work_hours = :work_hours,
                    status = :status
                WHERE appointment_id = :appointment_id
            """)
            session.execute(query, {
                'appointment_id': appointment_id,
                'caregiver_user_id': int(request.form['caregiver_user_id']),
                'member_user_id': int(request.form['member_user_id']),
                'appointment_date': request.form['appointment_date'],
                'appointment_time': request.form['appointment_time'],
                'work_hours': float(request.form['work_hours']),
                'status': request.form['status']
            })
            session.commit()
            flash('Appointment updated successfully!', 'success')
            return redirect(url_for('list_appointments'))
        
        query = text("SELECT * FROM APPOINTMENT WHERE appointment_id = :appointment_id")
        result = session.execute(query, {'appointment_id': appointment_id})
        appointment = result.fetchone()
        
        if appointment:
            appointment_dict = dict(appointment._mapping)
            # Convert date and time to strings for form
            if appointment_dict.get('appointment_date'):
                appointment_dict['appointment_date'] = str(appointment_dict['appointment_date'])
            if appointment_dict.get('appointment_time'):
                appointment_dict['appointment_time'] = str(appointment_dict['appointment_time'])
            
            # Get caregivers and members for dropdowns
            caregivers_query = text("""
                SELECT c.caregiver_user_id, u.given_name || ' ' || u.surname AS name
                FROM CAREGIVER c
                JOIN "USER" u ON c.caregiver_user_id = u.user_id
                ORDER BY c.caregiver_user_id
            """)
            members_query = text("""
                SELECT m.member_user_id, u.given_name || ' ' || u.surname AS name
                FROM MEMBER m
                JOIN "USER" u ON m.member_user_id = u.user_id
                ORDER BY m.member_user_id
            """)
            
            caregivers_result = session.execute(caregivers_query)
            members_result = session.execute(members_query)
            
            caregivers = [dict(row._mapping) for row in caregivers_result]
            members = [dict(row._mapping) for row in members_result]
            
            return render_template('appointments/edit.html', 
                                 appointment=appointment_dict,
                                 caregivers=caregivers,
                                 members=members)
        else:
            flash('Appointment not found', 'error')
            return redirect(url_for('list_appointments'))
    except Exception as e:
        session.rollback()
        flash(f'Error: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_appointments'))


@app.route('/appointments/<int:appointment_id>/delete', methods=['POST'])
def delete_appointment(appointment_id):
    """Delete an appointment"""
    session = get_db_session()
    try:
        session.execute(
            text("DELETE FROM APPOINTMENT WHERE appointment_id = :appointment_id"),
            {'appointment_id': appointment_id}
        )
        session.commit()
        flash('Appointment deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting appointment: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('list_appointments'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

