-- CSCI 341 Assignment 3 - Part 1: Database Schema
-- Caregiver Platform Database
-- Database: PostgreSQL

-- Drop existing tables if they exist (in reverse order of dependencies)
DROP TABLE IF EXISTS APPOINTMENT CASCADE;
DROP TABLE IF EXISTS JOB_APPLICATION CASCADE;
DROP TABLE IF EXISTS JOB CASCADE;
DROP TABLE IF EXISTS ADDRESS CASCADE;
DROP TABLE IF EXISTS MEMBER CASCADE;
DROP TABLE IF EXISTS CAREGIVER CASCADE;
DROP TABLE IF EXISTS "USER" CASCADE;

-- Create USER table (base table for all users)
CREATE TABLE "USER" (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    given_name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    profile_description TEXT,
    password VARCHAR(255) NOT NULL
);

-- Create CAREGIVER table (inherits from USER)
CREATE TABLE CAREGIVER (
    caregiver_user_id INTEGER PRIMARY KEY,
    photo VARCHAR(255),
    gender VARCHAR(20) NOT NULL,
    caregiving_type VARCHAR(50) NOT NULL CHECK (caregiving_type IN ('babysitter', 'elderly care', 'playmate for children')),
    hourly_rate DECIMAL(10, 2) NOT NULL CHECK (hourly_rate >= 0),
    FOREIGN KEY (caregiver_user_id) REFERENCES "USER"(user_id) ON DELETE CASCADE
);

-- Create MEMBER table (inherits from USER)
CREATE TABLE MEMBER (
    member_user_id INTEGER PRIMARY KEY,
    house_rules TEXT,
    dependent_description TEXT,
    FOREIGN KEY (member_user_id) REFERENCES "USER"(user_id) ON DELETE CASCADE
);

-- Create ADDRESS table (for MEMBER addresses)
CREATE TABLE ADDRESS (
    member_user_id INTEGER PRIMARY KEY,
    house_number VARCHAR(20) NOT NULL,
    street VARCHAR(255) NOT NULL,
    town VARCHAR(100) NOT NULL,
    FOREIGN KEY (member_user_id) REFERENCES MEMBER(member_user_id) ON DELETE CASCADE
);

-- Create JOB table (job postings by members)
CREATE TABLE JOB (
    job_id SERIAL PRIMARY KEY,
    member_user_id INTEGER NOT NULL,
    required_caregiving_type VARCHAR(50) NOT NULL CHECK (required_caregiving_type IN ('babysitter', 'elderly care', 'playmate for children')),
    other_requirements TEXT,
    date_posted DATE NOT NULL,
    FOREIGN KEY (member_user_id) REFERENCES MEMBER(member_user_id) ON DELETE CASCADE
);

-- Create JOB_APPLICATION table (caregivers applying to jobs)
CREATE TABLE JOB_APPLICATION (
    caregiver_user_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    date_applied DATE NOT NULL,
    PRIMARY KEY (caregiver_user_id, job_id),
    FOREIGN KEY (caregiver_user_id) REFERENCES CAREGIVER(caregiver_user_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES JOB(job_id) ON DELETE CASCADE
);

-- Create APPOINTMENT table (appointments between members and caregivers)
CREATE TABLE APPOINTMENT (
    appointment_id SERIAL PRIMARY KEY,
    caregiver_user_id INTEGER NOT NULL,
    member_user_id INTEGER NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    work_hours DECIMAL(4, 2) NOT NULL CHECK (work_hours > 0),
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'confirmed', 'declined', 'completed')),
    FOREIGN KEY (caregiver_user_id) REFERENCES CAREGIVER(caregiver_user_id) ON DELETE CASCADE,
    FOREIGN KEY (member_user_id) REFERENCES MEMBER(member_user_id) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX idx_caregiver_type ON CAREGIVER(caregiving_type);
CREATE INDEX idx_job_type ON JOB(required_caregiving_type);
CREATE INDEX idx_appointment_status ON APPOINTMENT(status);
CREATE INDEX idx_appointment_date ON APPOINTMENT(appointment_date);
CREATE INDEX idx_user_city ON "USER"(city);

