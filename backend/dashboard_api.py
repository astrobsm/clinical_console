from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from backend.models import db, Patient, Notification, Assessment

bp = Blueprint('dashboard_api', __name__, url_prefix='/api/dashboard')

@bp.route('/summary', methods=['GET'])
@jwt_required()
def dashboard_summary():
    total_patients = Patient.query.count()
    total_appointments = 0  # Add logic if you have an Appointment model
    total_notifications = Notification.query.count()
    total_assessments = Assessment.query.count()
    return jsonify({
        'patients': total_patients,
        'appointments': total_appointments,
        'notifications': total_notifications,
        'assessments': total_assessments
    })

@bp.route('/patient_trends', methods=['GET'])
@jwt_required()
def patient_trends():
    # Example: return dummy data for now
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    data = [10, 15, 12, 20, 18]
    trends = [{"month": m, "patients": d} for m, d in zip(months, data)]
    return jsonify(trends)

@bp.route('/recent_activity', methods=['GET'])
@jwt_required()
def recent_activity():
    # Example: return dummy data for now
    return jsonify([
        {'type': 'patient', 'message': 'admitted', 'time': '2025-07-25T10:00:00'},
        {'type': 'assessment', 'message': 'completed', 'time': '2025-07-25T09:00:00'},
        {'type': 'notification', 'message': 'sent', 'time': '2025-07-25T08:00:00'}
    ])
