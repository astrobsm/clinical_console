
import os
import sys
from datetime import datetime
from flask import Flask, send_from_directory, request, jsonify
from flask_migrate import upgrade
from flask_cors import CORS
from flask_cors import CORS
from dotenv import load_dotenv

# Add the parent directory to Python path so we can import backend modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from backend.database import db, migrate, jwt

load_dotenv()

def create_app():

    app = Flask(__name__, static_folder='frontend_build')
    # Automatically run migrations on startup
    try:
        with app.app_context():
            upgrade()
        print("Database migrations applied successfully.")
    except Exception as e:
        print(f"Migration error: {e}")
    CORS(app, supports_credentials=True, origins=["https://clinicalguru-36y53.ondigitalocean.app"])
    
    # Critical API routes FIRST - before everything else
    @app.route('/api/healthz', methods=['GET'])
    def healthz():
        return jsonify({"status": "ok"}), 200

    @app.route('/api/test', methods=['GET', 'POST'])
    def api_test():
        """Simple test endpoint"""
        return jsonify({
            'message': 'API is working!',
            'method': request.method,
            'timestamp': str(datetime.now())
        }), 200

    @app.route('/api/routes', methods=['GET'])
    def list_routes():
        """Debug endpoint to show all registered routes"""
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods),
                'rule': str(rule)
            })
        return jsonify(routes), 200
    
    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:natiss_natiss@localhost:5432/clinical_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    db.init_app(app)
    # Import all models so Alembic can detect them for migrations
    from backend.models import User, Patient, ClinicalEvaluation, Diagnosis, TreatmentPlan, LabInvestigation, ImagingInvestigation, WoundCarePlan, SurgeryBooking, Appointment, Notification, AcademicEvent, Assessment, CBTQuestion, Discharge, DischargeSummary, Score
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Configure CORS to allow your DigitalOcean domain and network access
    CORS(app, origins=[
        "http://localhost:3000",  # Local development
        "http://localhost:5000",  # Local Flask
        "http://192.168.0.199:3000",  # Network development
        "http://192.168.0.199:5000",  # Network Flask
        "https://clinicalguru-36y53.ondigitalocean.app",  # Your DigitalOcean frontend
        "http://clinicalguru-36y53.ondigitalocean.app",   # HTTP version
        "https://clinical-console-backend-cqk2r.ondigitalocean.app",  # Backend domain
        "http://clinical-console-backend-cqk2r.ondigitalocean.app",   # Backend HTTP
        "*"  # Allow all origins for development (remove in production)
    ], supports_credentials=True)

    # Start the CBT notification scheduler after app is configured
    from backend.cbt_scheduler import start_scheduler
    start_scheduler(app)
    from backend.cbt_api import bp as cbt_api_bp
    app.register_blueprint(cbt_api_bp)

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
    from backend.notification_api import bp as notification_api_bp
    app.register_blueprint(notification_api_bp)
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

    # Serve React static files - LAST, after all API routes
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react(path):
        # Explicitly block API paths - they should already be handled above
        if path.startswith('api/'):
            return jsonify({'error': 'API route not found'}), 404
        
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    return app


# Expose app for import by tests and other modules
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host="0.0.0.0", port=port, debug=debug)
