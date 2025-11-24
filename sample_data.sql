-- CSCI 341 Assignment 3 - Part 1: Sample Data
-- Insert at least 10 instances per table
-- Data designed to ensure all Part 2 queries return non-empty results

-- Insert USERS (at least 20: 10+ caregivers, 10+ members)
INSERT INTO "USER" (user_id, email, given_name, surname, city, phone_number, profile_description, password) VALUES
-- Caregivers (user_id 1-15)
(1, 'maria.garcia@email.com', 'Maria', 'Garcia', 'Astana', '+77011234567', 'Experienced babysitter with 5 years of experience', 'pass123'),
(2, 'john.smith@email.com', 'John', 'Smith', 'Almaty', '+77012345678', 'Professional caregiver for elderly, certified nurse', 'pass123'),
(3, 'anna.kim@email.com', 'Anna', 'Kim', 'Astana', '+77013456789', 'Creative playmate, loves arts and crafts', 'pass123'),
(4, 'david.lee@email.com', 'David', 'Lee', 'Shymkent', '+77014567890', 'Babysitter specializing in toddlers', 'pass123'),
(5, 'sarah.johnson@email.com', 'Sarah', 'Johnson', 'Astana', '+77015678901', 'Elderly care specialist with medical background', 'pass123'),
(6, 'michael.brown@email.com', 'Michael', 'Brown', 'Almaty', '+77016789012', 'Fun and energetic playmate for children', 'pass123'),
(7, 'lisa.wang@email.com', 'Lisa', 'Wang', 'Astana', '+77017890123', 'Experienced babysitter, CPR certified', 'pass123'),
(8, 'robert.taylor@email.com', 'Robert', 'Taylor', 'Karaganda', '+77018901234', 'Compassionate elderly caregiver', 'pass123'),
(9, 'emily.davis@email.com', 'Emily', 'Davis', 'Astana', '+77019012345', 'Creative playmate, music and dance enthusiast', 'pass123'),
(10, 'james.wilson@email.com', 'James', 'Wilson', 'Almaty', '+77010123456', 'Professional babysitter, early childhood education', 'pass123'),
(11, 'olivia.martinez@email.com', 'Olivia', 'Martinez', 'Astana', '+77011234560', 'Elderly care with physical therapy experience', 'pass123'),
(12, 'william.anderson@email.com', 'William', 'Anderson', 'Shymkent', '+77012345601', 'Babysitter, multilingual (English, Russian, Kazakh)', 'pass123'),
(13, 'sophia.thomas@email.com', 'Sophia', 'Thomas', 'Astana', '+77013456702', 'Playmate specializing in outdoor activities', 'pass123'),
(14, 'benjamin.jackson@email.com', 'Benjamin', 'Jackson', 'Almaty', '+77014567803', 'Elderly caregiver, patient and understanding', 'pass123'),
(15, 'charlotte.white@email.com', 'Charlotte', 'White', 'Astana', '+77015678904', 'Experienced babysitter, first aid certified', 'pass123'),

-- Members (user_id 16-30)
(16, 'amina.aminova@email.com', 'Amina', 'Aminova', 'Astana', '+77016789015', 'Looking for reliable caregiver', 'pass123'),
(17, 'arman.armanov@email.com', 'Arman', 'Armanov', 'Almaty', '+77017890126', 'Seeking professional caregiver', 'pass123'),
(18, 'nurlybek.nurlybekov@email.com', 'Nurlybek', 'Nurlybekov', 'Astana', '+77018901237', 'Family with elderly parent', 'pass123'),
(19, 'ayzhan.ayzhanova@email.com', 'Ayzhan', 'Ayzhanova', 'Shymkent', '+77019012348', 'Working parent needs babysitter', 'pass123'),
(20, 'daniyar.daniyarov@email.com', 'Daniyar', 'Daniyarov', 'Astana', '+77010123459', 'Looking for playmate for children', 'pass123'),
(21, 'madina.madinova@email.com', 'Madina', 'Madinova', 'Almaty', '+77011234570', 'Elderly care needed', 'pass123'),
(22, 'askar.askarov@email.com', 'Askar', 'Askarov', 'Astana', '+77012345681', 'Babysitter for two children', 'pass123'),
(23, 'aigerim.aigerimova@email.com', 'Aigerim', 'Aigerimova', 'Karaganda', '+77013456792', 'Professional caregiver required', 'pass123'),
(24, 'bekzhan.bekzhanov@email.com', 'Bekzhan', 'Bekzhanov', 'Astana', '+77014567803', 'Playmate for active child', 'pass123'),
(25, 'gulnara.gulnarova@email.com', 'Gulnara', 'Gulnarova', 'Almaty', '+77015678914', 'Elderly parent needs assistance', 'pass123'),
(26, 'kairat.kairatov@email.com', 'Kairat', 'Kairatov', 'Astana', '+77016789025', 'Babysitter for weekend care', 'pass123'),
(27, 'zhuldyz.zhuldyzova@email.com', 'Zhuldyz', 'Zhuldyzova', 'Shymkent', '+77017890136', 'Looking for experienced caregiver', 'pass123'),
(28, 'nurlan.nurlanov@email.com', 'Nurlan', 'Nurlanov', 'Astana', '+77018901247', 'Elderly care with medical needs', 'pass123'),
(29, 'saltanat.saltanova@email.com', 'Saltanat', 'Saltanova', 'Almaty', '+77019012358', 'Babysitter for after-school care', 'pass123'),
(30, 'talgat.talgatov@email.com', 'Talgat', 'Talgatov', 'Astana', '+77010123469', 'Playmate for creative activities', 'pass123');

-- Insert CAREGIVERS (at least 10)
INSERT INTO CAREGIVER (caregiver_user_id, photo, gender, caregiving_type, hourly_rate) VALUES
(1, 'maria_photo.jpg', 'Female', 'babysitter', 8.50),
(2, 'john_photo.jpg', 'Male', 'elderly care', 12.00),
(3, 'anna_photo.jpg', 'Female', 'playmate for children', 7.00),
(4, 'david_photo.jpg', 'Male', 'babysitter', 9.00),
(5, 'sarah_photo.jpg', 'Female', 'elderly care', 15.00),
(6, 'michael_photo.jpg', 'Male', 'playmate for children', 6.50),
(7, 'lisa_photo.jpg', 'Female', 'babysitter', 10.00),
(8, 'robert_photo.jpg', 'Male', 'elderly care', 11.50),
(9, 'emily_photo.jpg', 'Female', 'playmate for children', 8.00),
(10, 'james_photo.jpg', 'Male', 'babysitter', 9.50),
(11, 'olivia_photo.jpg', 'Female', 'elderly care', 13.00),
(12, 'william_photo.jpg', 'Male', 'babysitter', 8.75),
(13, 'sophia_photo.jpg', 'Female', 'playmate for children', 7.50),
(14, 'benjamin_photo.jpg', 'Male', 'elderly care', 12.50),
(15, 'charlotte_photo.jpg', 'Female', 'babysitter', 10.50);

-- Insert MEMBERS (at least 10)
INSERT INTO MEMBER (member_user_id, house_rules, dependent_description) VALUES
(16, 'No smoking. Please remove shoes at entrance.', 'I have a 5-year old son who likes painting and needs supervision during playtime.'),
(17, 'No pets. Quiet environment required.', 'Elderly father, 78 years old, needs assistance with daily activities and medication.'),
(18, 'No pets. Clean and organized space.', 'Elderly mother, 82 years old, requires help with mobility and companionship.'),
(19, 'No pets. Child-friendly environment.', 'Two children: 4-year-old daughter and 7-year-old son, need after-school care.'),
(20, 'Creative activities encouraged. Outdoor play preferred.', '6-year-old daughter who loves music and dance, needs an active playmate.'),
(21, 'No pets. Medical equipment present.', 'Elderly grandmother, 85 years old, needs specialized care and monitoring.'),
(22, 'Strict bedtime routine. Healthy snacks only.', 'Two children: 3-year-old and 5-year-old, need consistent care and routine.'),
(23, 'No pets. Professional demeanor required.', 'Elderly father, 75 years old, needs assistance with physical therapy exercises.'),
(24, 'Active play encouraged. Safety first.', '8-year-old son who loves sports and outdoor activities, needs energetic playmate.'),
(25, 'No pets. Quiet and peaceful environment.', 'Elderly mother, 80 years old, needs help with daily tasks and companionship.'),
(26, 'Flexible schedule. Fun activities welcome.', '5-year-old daughter, needs weekend babysitting for occasional outings.'),
(27, 'No pets. Cleanliness important.', 'Elderly aunt, 77 years old, needs assistance with household tasks and social interaction.'),
(28, 'No pets. Medical supervision required.', 'Elderly father, 88 years old, with chronic conditions requiring careful monitoring.'),
(29, 'Homework help needed. Educational activities preferred.', '9-year-old son, needs after-school care and homework assistance.'),
(30, 'Art supplies available. Creative environment.', '7-year-old daughter who loves drawing and crafts, needs creative playmate.');

-- Insert ADDRESSES (at least 10, one per member)
INSERT INTO ADDRESS (member_user_id, house_number, street, town) VALUES
(16, '15', 'Abay Avenue', 'Astana'),
(17, '23', 'Dostyk Street', 'Almaty'),
(18, '42', 'Kabanbay Batyr Avenue', 'Astana'),
(19, '7', 'Turan Avenue', 'Shymkent'),
(20, '31', 'Kabanbay Batyr Avenue', 'Astana'),
(21, '56', 'Al-Farabi Avenue', 'Almaty'),
(22, '12', 'Kabanbay Batyr Avenue', 'Astana'),
(23, '89', 'Bukhar Zhyrau Boulevard', 'Karaganda'),
(24, '4', 'Kabanbay Batyr Avenue', 'Astana'),
(25, '67', 'Raiymbek Avenue', 'Almaty'),
(26, '19', 'Kabanbay Batyr Avenue', 'Astana'),
(27, '33', 'Tauelsizdik Avenue', 'Shymkent'),
(28, '8', 'Kabanbay Batyr Avenue', 'Astana'),
(29, '91', 'Abay Avenue', 'Almaty'),
(30, '25', 'Kabanbay Batyr Avenue', 'Astana');

-- Insert JOBS (at least 10)
INSERT INTO JOB (job_id, member_user_id, required_caregiving_type, other_requirements, date_posted) VALUES
(1, 16, 'babysitter', 'Must be patient and soft-spoken with children. Experience with arts and crafts preferred.', '2025-01-15'),
(2, 17, 'elderly care', 'No pets. Caregiver must be soft-spoken and gentle. Medical background preferred.', '2025-01-20'),
(3, 18, 'elderly care', 'No pets. Quiet environment. Soft-spoken caregiver required for elderly care.', '2025-02-01'),
(4, 19, 'babysitter', 'Must handle multiple children. CPR certification preferred.', '2025-02-05'),
(5, 20, 'playmate for children', 'Energetic and creative. Music and dance skills preferred.', '2025-02-10'),
(6, 21, 'elderly care', 'No pets. Medical equipment knowledge required. Soft-spoken and professional.', '2025-02-15'),
(7, 22, 'babysitter', 'Experience with toddlers. Must follow strict routines.', '2025-02-20'),
(8, 16, 'playmate for children', 'Creative activities. Soft-spoken approach to children preferred.', '2025-03-01'),
(9, 23, 'elderly care', 'Physical therapy experience. Professional and soft-spoken demeanor required.', '2025-03-05'),
(10, 24, 'playmate for children', 'Active and energetic. Sports activities preferred.', '2025-03-10'),
(11, 25, 'elderly care', 'No pets. Quiet and peaceful environment. Soft-spoken caregiver needed.', '2025-03-15'),
(12, 26, 'babysitter', 'Weekend availability. Fun and engaging activities.', '2025-03-20'),
(13, 27, 'elderly care', 'No pets. Household assistance and social interaction.', '2025-04-01'),
(14, 28, 'elderly care', 'No pets. Medical supervision. Soft-spoken and careful approach.', '2025-04-05'),
(15, 29, 'babysitter', 'Homework help. Educational activities preferred.', '2025-04-10'),
(16, 30, 'playmate for children', 'Art and crafts. Creative and soft-spoken playmate preferred.', '2025-04-15');

-- Insert JOB_APPLICATIONS (at least 10)
INSERT INTO JOB_APPLICATION (caregiver_user_id, job_id, date_applied) VALUES
(1, 1, '2025-01-16'),
(1, 4, '2025-02-06'),
(1, 7, '2025-02-21'),
(2, 2, '2025-01-21'),
(2, 3, '2025-02-02'),
(2, 6, '2025-02-16'),
(3, 5, '2025-02-11'),
(3, 8, '2025-03-02'),
(3, 10, '2025-03-11'),
(4, 1, '2025-01-17'),
(4, 4, '2025-02-07'),
(4, 12, '2025-03-21'),
(5, 2, '2025-01-22'),
(5, 3, '2025-02-03'),
(5, 11, '2025-03-16'),
(6, 5, '2025-02-12'),
(6, 8, '2025-03-03'),
(6, 10, '2025-03-12'),
(7, 1, '2025-01-18'),
(7, 7, '2025-02-22'),
(7, 12, '2025-03-22'),
(7, 15, '2025-04-11'),
(8, 2, '2025-01-23'),
(8, 6, '2025-02-17'),
(8, 9, '2025-03-06'),
(9, 5, '2025-02-13'),
(9, 8, '2025-03-04'),
(9, 16, '2025-04-16'),
(10, 4, '2025-02-08'),
(10, 7, '2025-02-23'),
(10, 15, '2025-04-12'),
(11, 3, '2025-02-04'),
(11, 6, '2025-02-18'),
(11, 11, '2025-03-17'),
(12, 1, '2025-01-19'),
(12, 4, '2025-02-09'),
(12, 12, '2025-03-23'),
(13, 5, '2025-02-14'),
(13, 10, '2025-03-13'),
(13, 16, '2025-04-17'),
(14, 2, '2025-01-24'),
(14, 3, '2025-02-05'),
(14, 9, '2025-03-07'),
(15, 1, '2025-01-20'),
(15, 7, '2025-02-24'),
(15, 15, '2025-04-13');

-- Insert APPOINTMENTS (at least 10, with various statuses including 'confirmed' for accepted appointments)
INSERT INTO APPOINTMENT (appointment_id, caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status) VALUES
(1, 1, 16, '2025-05-01', '09:00:00', 3.0, 'confirmed'),
(2, 2, 17, '2025-05-02', '10:00:00', 4.0, 'confirmed'),
(3, 3, 20, '2025-05-03', '14:00:00', 2.5, 'confirmed'),
(4, 4, 19, '2025-05-04', '08:00:00', 5.0, 'confirmed'),
(5, 5, 18, '2025-05-05', '11:00:00', 3.5, 'confirmed'),
(6, 6, 20, '2025-05-06', '15:00:00', 2.0, 'confirmed'),
(7, 7, 22, '2025-05-07', '09:30:00', 4.5, 'confirmed'),
(8, 8, 21, '2025-05-08', '10:30:00', 3.0, 'confirmed'),
(9, 9, 24, '2025-05-09', '13:00:00', 3.0, 'confirmed'),
(10, 10, 19, '2025-05-10', '08:30:00', 4.0, 'confirmed'),
(11, 11, 25, '2025-05-11', '12:00:00', 3.5, 'confirmed'),
(12, 12, 26, '2025-05-12', '16:00:00', 2.5, 'confirmed'),
(13, 13, 30, '2025-05-13', '14:30:00', 2.0, 'confirmed'),
(14, 14, 28, '2025-05-14', '11:00:00', 4.0, 'confirmed'),
(15, 15, 29, '2025-05-15', '15:30:00', 3.0, 'confirmed'),
(16, 1, 16, '2025-05-16', '09:00:00', 3.0, 'pending'),
(17, 2, 17, '2025-05-17', '10:00:00', 4.0, 'pending'),
(18, 3, 20, '2025-05-18', '14:00:00', 2.5, 'declined'),
(19, 4, 19, '2025-05-19', '08:00:00', 5.0, 'pending'),
(20, 5, 18, '2025-05-20', '11:00:00', 3.5, 'completed'),
(21, 6, 20, '2025-05-21', '15:00:00', 2.0, 'completed'),
(22, 7, 22, '2025-05-22', '09:30:00', 4.5, 'completed'),
(23, 8, 21, '2025-05-23', '10:30:00', 3.0, 'declined'),
(24, 9, 24, '2025-05-24', '13:00:00', 3.0, 'pending'),
(25, 10, 19, '2025-05-25', '08:30:00', 4.0, 'completed');

-- Reset sequences to continue from the highest ID
-- Note: Sequence name must be quoted because table is "USER"
SELECT setval('"USER_user_id_seq"', (SELECT MAX(user_id) FROM "USER"));
SELECT setval('job_job_id_seq', (SELECT MAX(job_id) FROM JOB));
SELECT setval('appointment_appointment_id_seq', (SELECT MAX(appointment_id) FROM APPOINTMENT));

