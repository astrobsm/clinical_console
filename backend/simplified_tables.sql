-- Simplified table creation for DigitalOcean Console
-- Copy and paste this into the DigitalOcean database console

-- Users table
CREATE TABLE IF NOT EXISTS clinical_users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(256) NOT NULL,
    role VARCHAR(32) NOT NULL,
    name VARCHAR(120) NOT NULL,
    rotation_end TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Patients table
CREATE TABLE IF NOT EXISTS patient (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    dob DATE,
    gender VARCHAR(16),
    inpatient BOOLEAN DEFAULT false,
    consultant_id INTEGER REFERENCES clinical_users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Appointments table
CREATE TABLE IF NOT EXISTS appointment (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patient(id),
    scheduled_by INTEGER REFERENCES clinical_users(id),
    appointment_date TIMESTAMP NOT NULL,
    appointment_type VARCHAR(50),
    status VARCHAR(20) DEFAULT 'scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grant permissions to your user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO clinical_console;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO clinical_console;

-- Insert admin user (password is 'admin123')
INSERT INTO clinical_users (email, password, role, name, is_active) 
VALUES (
    'admin@plasticsurg.com', 
    'scrypt:32768:8:1$1mEuuEJYlJNIm8KC$94c8c6e3a91e68b7e59d69e2c6a3b2f1e8d4c7a6b9f2e1d0a4b7c8e9f1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7',
    'admin', 
    'System Administrator', 
    true
) ON CONFLICT (email) DO NOTHING;
