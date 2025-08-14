-- Database schema for plastic surgery unit EMR system
-- Send this to your DigitalOcean database administrator

-- Users table for authentication and authorization
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(256) NOT NULL,
    role VARCHAR(32) NOT NULL,
    name VARCHAR(120) NOT NULL,
    rotation_end TIMESTAMP WITHOUT TIME ZONE,
    is_active BOOLEAN DEFAULT true
);

-- Patients table
CREATE TABLE IF NOT EXISTS patient (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(120),
    address TEXT,
    emergency_contact_name VARCHAR(120),
    emergency_contact_phone VARCHAR(20),
    medical_record_number VARCHAR(50) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Clinical encounters
CREATE TABLE IF NOT EXISTS clinical_encounter (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patient(id),
    encounter_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    encounter_type VARCHAR(50),
    chief_complaint TEXT,
    present_illness TEXT,
    examination_findings TEXT,
    diagnosis TEXT,
    treatment_plan TEXT,
    created_by INTEGER REFERENCES "user"(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Assessments
CREATE TABLE IF NOT EXISTS assessment (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patient(id),
    encounter_id INTEGER REFERENCES clinical_encounter(id),
    assessment_type VARCHAR(50),
    score INTEGER,
    total_score INTEGER,
    assessment_data JSON,
    notes TEXT,
    assessed_by INTEGER REFERENCES "user"(id),
    assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Appointments
CREATE TABLE IF NOT EXISTS appointment (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patient(id),
    scheduled_by INTEGER REFERENCES "user"(id),
    appointment_date TIMESTAMP NOT NULL,
    appointment_type VARCHAR(50),
    status VARCHAR(20) DEFAULT 'scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Surgery bookings
CREATE TABLE IF NOT EXISTS surgery_booking (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patient(id),
    surgeon_id INTEGER REFERENCES "user"(id),
    surgery_date TIMESTAMP NOT NULL,
    surgery_type VARCHAR(100),
    procedure_name VARCHAR(200),
    theatre_number VARCHAR(20),
    estimated_duration INTEGER,
    status VARCHAR(20) DEFAULT 'scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Wound care
CREATE TABLE IF NOT EXISTS wound_care (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patient(id),
    encounter_id INTEGER REFERENCES clinical_encounter(id),
    wound_description TEXT,
    wound_size VARCHAR(50),
    wound_location VARCHAR(100),
    care_provided TEXT,
    next_care_date DATE,
    performed_by INTEGER REFERENCES "user"(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notifications
CREATE TABLE IF NOT EXISTS notification (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id),
    title VARCHAR(200),
    message TEXT,
    notification_type VARCHAR(50),
    read_status BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Academic events
CREATE TABLE IF NOT EXISTS academic_event (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    event_date TIMESTAMP NOT NULL,
    location VARCHAR(100),
    event_type VARCHAR(50),
    created_by INTEGER REFERENCES "user"(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Treatment records
CREATE TABLE IF NOT EXISTS treatment (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patient(id),
    encounter_id INTEGER REFERENCES clinical_encounter(id),
    treatment_type VARCHAR(100),
    treatment_description TEXT,
    medications TEXT,
    dosage VARCHAR(100),
    frequency VARCHAR(50),
    duration VARCHAR(50),
    prescribed_by INTEGER REFERENCES "user"(id),
    prescribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Lab investigations
CREATE TABLE IF NOT EXISTS lab_investigation (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patient(id),
    encounter_id INTEGER REFERENCES clinical_encounter(id),
    investigation_type VARCHAR(100),
    test_name VARCHAR(200),
    results TEXT,
    reference_values VARCHAR(200),
    status VARCHAR(50) DEFAULT 'pending',
    ordered_by INTEGER REFERENCES "user"(id),
    ordered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    result_date TIMESTAMP
);

-- Imaging investigations
CREATE TABLE IF NOT EXISTS imaging_investigation (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patient(id),
    encounter_id INTEGER REFERENCES clinical_encounter(id),
    imaging_type VARCHAR(100),
    study_description VARCHAR(200),
    findings TEXT,
    impression TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    ordered_by INTEGER REFERENCES "user"(id),
    ordered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    study_date TIMESTAMP
);

-- Diagnosis records
CREATE TABLE IF NOT EXISTS diagnosis (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patient(id),
    encounter_id INTEGER REFERENCES clinical_encounter(id),
    diagnosis_code VARCHAR(20),
    diagnosis_description TEXT,
    diagnosis_type VARCHAR(50),
    severity VARCHAR(20),
    status VARCHAR(20) DEFAULT 'active',
    diagnosed_by INTEGER REFERENCES "user"(id),
    diagnosed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Discharge summaries
CREATE TABLE IF NOT EXISTS discharge_summary (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patient(id),
    encounter_id INTEGER REFERENCES clinical_encounter(id),
    admission_date DATE,
    discharge_date DATE,
    length_of_stay INTEGER,
    discharge_condition VARCHAR(100),
    discharge_medications TEXT,
    follow_up_instructions TEXT,
    created_by INTEGER REFERENCES "user"(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CBT questions for assessments
CREATE TABLE IF NOT EXISTS cbt_question (
    id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50),
    options JSON,
    scoring_criteria JSON,
    category VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default admin user (password: admin123)
INSERT INTO "user" (email, password, role, name, is_active) 
VALUES (
    'admin@plasticsurg.com', 
    'scrypt:32768:8:1$1mEuuEJYlJNIm8KC$94c8c6e3a91e68b7e59d69e2c6a3b2f1e8d4c7a6b9f2e1d0a4b7c8e9f1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7', 
    'admin', 
    'System Administrator', 
    true
) ON CONFLICT (email) DO NOTHING;

-- Grant necessary permissions to the user
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO clinical_console;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO clinical_console;
