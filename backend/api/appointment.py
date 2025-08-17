from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from backend.models import db, Appointment, User

bp = Blueprint('appointment', __name__, url_prefix='/api/appointments')

def role_required(roles):
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user or user.role not in roles:
                return jsonify({'msg': 'Forbidden'}), 403
            return fn(*args, **kwargs)
        decorator.__name__ = fn.__name__
        return decorator
    return wrapper

@bp.route('/', methods=['GET'])
@jwt_required()
def get_appointments():
    """Get all appointments - available to all authenticated users"""
    try:
        appointments = Appointment.query.all()
        return jsonify([{
            'id': a.id,
            'patient_id': a.patient_id,
            'date': a.appointment_date.isoformat() if a.appointment_date else None,
            'appointment_date': a.appointment_date.isoformat() if a.appointment_date else None,  # For API compatibility
            'purpose': a.appointment_type,  # Map appointment_type to purpose for frontend compatibility
            'appointment_type': a.appointment_type,
            'status': a.status,
            'notes': a.notes,
            'scheduled_by': a.scheduled_by,
            'created_at': a.created_at.isoformat() if a.created_at else None
        } for a in appointments])
    except Exception as e:
        return jsonify({'msg': f'Error fetching appointments: {str(e)}'}), 500

@bp.route('/', methods=['POST'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def create_appointment():
    """Create a new appointment - restricted to senior staff"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'msg': 'No data provided'}), 400
            
        if not data.get('patient_id'):
            return jsonify({'msg': 'Patient ID is required'}), 400
            
        # Accept both 'date' and 'appointment_date' for flexibility
        appointment_date = data.get('appointment_date') or data.get('date')
        if not appointment_date:
            return jsonify({'msg': 'Appointment date is required'}), 400
        
        # Parse date if it's a string
        if isinstance(appointment_date, str):
            try:
                appointment_date = datetime.fromisoformat(appointment_date.replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'msg': 'Invalid date format'}), 400
        
        # Map purpose to appointment_type for backward compatibility
        appointment_type = data.get('appointment_type') or data.get('purpose', 'General')
        
        appointment = Appointment(
            patient_id=data.get('patient_id'),
            appointment_date=appointment_date,
            appointment_type=appointment_type,
            status=data.get('status', 'Scheduled'),
            notes=data.get('notes'),
            scheduled_by=get_jwt_identity()
        )
        db.session.add(appointment)
        db.session.commit()
        return jsonify({'msg': 'Appointment created', 'id': appointment.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': f'Error creating appointment: {str(e)}'}), 500

@bp.route('/<int:appointment_id>', methods=['GET'])
@jwt_required()
def get_appointment(appointment_id):
    """Get a specific appointment"""
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        return jsonify({
            'id': appointment.id,
            'patient_id': appointment.patient_id,
            'date': appointment.appointment_date.isoformat() if appointment.appointment_date else None,
            'appointment_date': appointment.appointment_date.isoformat() if appointment.appointment_date else None,
            'purpose': appointment.appointment_type,  # Map appointment_type to purpose for frontend compatibility
            'appointment_type': appointment.appointment_type,
            'status': appointment.status,
            'notes': appointment.notes,
            'scheduled_by': appointment.scheduled_by,
            'created_at': appointment.created_at.isoformat() if appointment.created_at else None
        })
    except Exception as e:
        return jsonify({'msg': f'Error fetching appointment: {str(e)}'}), 500

@bp.route('/<int:appointment_id>', methods=['PUT'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def update_appointment(appointment_id):
    """Update an appointment - restricted to senior staff"""
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        data = request.get_json()
        
        if 'patient_id' in data:
            appointment.patient_id = data['patient_id']
        
        # Accept both 'date' and 'appointment_date' for flexibility
        if 'appointment_date' in data or 'date' in data:
            appointment_date = data.get('appointment_date') or data.get('date')
            if isinstance(appointment_date, str):
                try:
                    appointment_date = datetime.fromisoformat(appointment_date.replace('Z', '+00:00'))
                except ValueError:
                    return jsonify({'msg': 'Invalid date format'}), 400
            appointment.appointment_date = appointment_date
            
        # Accept both 'appointment_type' and 'purpose' for flexibility  
        if 'appointment_type' in data or 'purpose' in data:
            appointment.appointment_type = data.get('appointment_type') or data.get('purpose')
            
        if 'status' in data:
            appointment.status = data['status']
        if 'notes' in data:
            appointment.notes = data['notes']
            
        db.session.commit()
        return jsonify({'msg': 'Appointment updated'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': f'Error updating appointment: {str(e)}'}), 500

@bp.route('/<int:appointment_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_appointment(appointment_id):
    """Delete an appointment - admin only"""
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({'msg': 'Appointment deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': f'Error deleting appointment: {str(e)}'}), 500

# Health check endpoint
@bp.route('/health', methods=['GET'])
def health_check():
    """Health check for appointments API"""
    try:
        count = Appointment.query.count()
        return jsonify({
            'status': 'healthy',
            'total_appointments': count,
            'service': 'appointments'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'service': 'appointments'
        }), 500
