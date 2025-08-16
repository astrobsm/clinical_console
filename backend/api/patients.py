# RESTful Patient API with JWT and role-based access
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from backend.models import db, Patient, User

bp = Blueprint('patients', __name__, url_prefix='/api/patients')

# Helper: role check
def role_required(roles):
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            user_id = str(get_jwt_identity())
            user = User.query.get(user_id)
            if not user or user.role not in roles:
                return jsonify({'msg': 'Forbidden'}), 403
            return fn(*args, **kwargs)
        decorator.__name__ = fn.__name__
        return decorator
    return wrapper

@bp.route('/', methods=['GET'])
@jwt_required()
def get_patients():
    """Get all patients - available to all authenticated users"""
    try:
        patients = Patient.query.all()
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'dob': p.dob.isoformat() if p.dob else None,
            'gender': p.gender,
            'inpatient': p.inpatient,
            'date_registered': p.created_at.isoformat() if p.created_at else None,
            'consultant_id': p.consultant_id
        } for p in patients])
    except Exception as e:
        return jsonify({'msg': f'Error fetching patients: {str(e)}'}), 500

@bp.route('/', methods=['POST'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def create_patient():
    """Create a new patient - restricted to senior staff"""
    try:
        data = request.get_json()
        if not data or not data.get('name'):
            return jsonify({'msg': 'Name is required'}), 400
            
        patient = Patient(
            name=data.get('name'),
            dob=data.get('dob'),
            gender=data.get('gender'),
            inpatient=data.get('inpatient', False),
            consultant_id=data.get('consultant_id')
        )
        db.session.add(patient)
        db.session.commit()
        return jsonify({'msg': 'Patient created', 'id': patient.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': f'Error creating patient: {str(e)}'}), 500

@bp.route('/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient(patient_id):
    """Get a specific patient by ID"""
    try:
        patient = Patient.query.get_or_404(patient_id)
        return jsonify({
            'id': patient.id,
            'name': patient.name,
            'dob': patient.dob.isoformat() if patient.dob else None,
            'gender': patient.gender,
            'inpatient': patient.inpatient,
            'date_registered': patient.created_at.isoformat() if patient.created_at else None,
            'consultant_id': patient.consultant_id
        })
    except Exception as e:
        return jsonify({'msg': f'Error fetching patient: {str(e)}'}), 500

@bp.route('/<int:patient_id>', methods=['PUT'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def update_patient(patient_id):
    """Update a patient - restricted to senior staff"""
    try:
        patient = Patient.query.get_or_404(patient_id)
        data = request.get_json()
        
        if 'name' in data:
            patient.name = data['name']
        if 'dob' in data:
            patient.dob = data['dob']
        if 'gender' in data:
            patient.gender = data['gender']
        if 'inpatient' in data:
            patient.inpatient = data['inpatient']
        if 'consultant_id' in data:
            patient.consultant_id = data['consultant_id']
            
        db.session.commit()
        return jsonify({'msg': 'Patient updated'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': f'Error updating patient: {str(e)}'}), 500

@bp.route('/<int:patient_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_patient(patient_id):
    """Delete a patient - admin only"""
    try:
        patient = Patient.query.get_or_404(patient_id)
        db.session.delete(patient)
        db.session.commit()
        return jsonify({'msg': 'Patient deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': f'Error deleting patient: {str(e)}'}), 500

# Health check endpoint for patients
@bp.route('/health', methods=['GET'])
def health_check():
    """Health check for patients API"""
    try:
        # Simple query to test database connectivity
        count = Patient.query.count()
        return jsonify({
            'status': 'healthy',
            'total_patients': count,
            'service': 'patients'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'service': 'patients'
        }), 500
