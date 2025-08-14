from backend.database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'clinical_users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(32), nullable=False)  # consultant, senior_registrar, registrar, house_officer, admin
    name = db.Column(db.String(120), nullable=False)
    rotation_end = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    # Relationships
    patients = db.relationship('Patient', backref='assigned_consultant', lazy=True, foreign_keys='Patient.consultant_id')

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(16), nullable=True)
    inpatient = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    consultant_id = db.Column(db.Integer, db.ForeignKey('clinical_users.id'), nullable=True)
    # Note: removed senior_registrar_id, registrar_id, house_officer_id as they don't exist in DB
    # Add more fields as needed

class ClinicalEvaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Diagnosis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    diagnosis = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class TreatmentPlan(db.Model):
    __tablename__ = 'treatment'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    treatment = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class LabInvestigation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    investigation = db.Column(db.String(256), nullable=False)
    result = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class ImagingInvestigation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    investigation = db.Column(db.String(256), nullable=False)
    finding = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class WoundCarePlan(db.Model):
    __tablename__ = 'wound_care'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    care_given = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class SurgeryBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    surgery_type = db.Column(db.String(256), nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    purpose = db.Column(db.String(256), nullable=True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    scheduled_by = db.Column(db.Integer, db.ForeignKey('clinical_users.id'), nullable=True)
    appointment_date = db.Column(db.DateTime, nullable=False)
    appointment_type = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('clinical_users.id'), nullable=False)
    message = db.Column(db.String(256), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AcademicEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text, nullable=True)
    event_date = db.Column(db.DateTime, nullable=False)
    moderator_id = db.Column(db.Integer, db.ForeignKey('clinical_users.id'), nullable=True)
    presenter_id = db.Column(db.Integer, db.ForeignKey('clinical_users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('clinical_users.id'), nullable=False)
    assessment_type = db.Column(db.String(100), nullable=True)
    score = db.Column(db.Integer, nullable=True)
    responses = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CBTQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diagnosis = db.Column(db.String(256), nullable=False)
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(256), nullable=False)
    option_b = db.Column(db.String(256), nullable=False)
    option_c = db.Column(db.String(256), nullable=False)
    option_d = db.Column(db.String(256), nullable=False)
    option_e = db.Column(db.String(256), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)


class Discharge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    discharge_date = db.Column(db.DateTime, nullable=True)
    follow_up_date = db.Column(db.DateTime, nullable=True)
    discharge_summary = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DischargeSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    summary_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('clinical_users.id'), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=True)
    recommendation = db.Column(db.String(256), nullable=True)
    advice = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
