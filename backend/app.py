
import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():

    app = Flask(__name__, static_folder='frontend_build')
    # Start the CBT notification scheduler
    from backend.cbt_scheduler import start_scheduler
    start_scheduler(app)
    from backend.cbt_api import bp as cbt_api_bp
    app.register_blueprint(cbt_api_bp)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:natiss_natiss@localhost:5432/clinical_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    db.init_app(app)
    # Import all models so Alembic can detect them for migrations
    from backend.models import User, Patient, ClinicalEvaluation, Diagnosis, TreatmentPlan, LabInvestigation, ImagingInvestigation, WoundCarePlan, SurgeryBooking, Appointment, Notification, AcademicEvent, Assessment, CBTQuestion, Discharge, DischargeSummary, Score
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    # Register blueprints

    from backend.discharge import bp as discharge_bp
    app.register_blueprint(discharge_bp)
    from backend.swagger import bp as swagger_bp
    app.register_blueprint(swagger_bp)
    from backend.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    from backend.protected_example import bp as protected_bp
    app.register_blueprint(protected_bp)
    from backend.api.patients import bp as patients_bp
    app.register_blueprint(patients_bp)
    from backend.api.clinical import bp as clinical_bp
    app.register_blueprint(clinical_bp)
    from backend.api.notifications import bp as notifications_bp
    app.register_blueprint(notifications_bp)
    from backend.api.assessments import bp as assessments_bp
    app.register_blueprint(assessments_bp)
    from backend.api.diagnosis import bp as diagnosis_bp
    app.register_blueprint(diagnosis_bp)
    from backend.api.treatment import bp as treatment_bp
    app.register_blueprint(treatment_bp)
    from backend.api.lab_investigation import bp as lab_investigation_bp
    app.register_blueprint(lab_investigation_bp)
    from backend.api.imaging_investigation import bp as imaging_investigation_bp
    app.register_blueprint(imaging_investigation_bp)
    from backend.api.wound_care import bp as wound_care_bp
    app.register_blueprint(wound_care_bp)
    from backend.api.surgery_booking import bp as surgery_booking_bp
    app.register_blueprint(surgery_booking_bp)
    from backend.api.appointment import bp as appointment_bp
    app.register_blueprint(appointment_bp)
    # Removed notification_api blueprint to resolve /api/notifications conflict
    from backend.api.academic_event import bp as academic_event_bp
    app.register_blueprint(academic_event_bp)
    from backend.api.assessment_api import bp as assessment_api_bp
    app.register_blueprint(assessment_api_bp)
    from backend.api.cbt_question import bp as cbt_question_bp
    app.register_blueprint(cbt_question_bp)
    from backend.discharge_api import bp as discharge_api_bp
    app.register_blueprint(discharge_api_bp)
    from backend.discharge_summary import bp as discharge_summary_bp
    app.register_blueprint(discharge_summary_bp)

    from backend.score_api import bp as score_api_bp
    app.register_blueprint(score_api_bp)

    from backend.dashboard_api import bp as dashboard_api_bp
    app.register_blueprint(dashboard_api_bp)

    # Serve React static files
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    # Health check endpoint
    @app.route('/healthz')
    def healthz():
        return {"status": "ok"}, 200

    return app


# Expose app for import by tests and other modules
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
