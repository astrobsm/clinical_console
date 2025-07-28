from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
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
    appointments = Appointment.query.all()
    return jsonify([{
        'id': a.id,
        'patient_id': a.patient_id,
        'date': a.date.isoformat() if a.date else None,
        'purpose': a.purpose
    } for a in appointments])

@bp.route('/', methods=['POST'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def create_appointment():
    data = request.get_json()
    appointment = Appointment(
        patient_id=data.get('patient_id'),
        date=data.get('date'),
        purpose=data.get('purpose')
    )
    db.session.add(appointment)
    db.session.commit()
    return jsonify({'msg': 'Appointment created', 'id': appointment.id}), 201

@bp.route('/<int:appointment_id>', methods=['GET'])
@jwt_required()
def get_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    return jsonify({
        'id': appointment.id,
        'patient_id': appointment.patient_id,
        'date': appointment.date.isoformat() if appointment.date else None,
        'purpose': appointment.purpose
    })

@bp.route('/<int:appointment_id>', methods=['PUT'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def update_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    data = request.get_json()
    appointment.date = data.get('date', appointment.date)
    appointment.purpose = data.get('purpose', appointment.purpose)
    db.session.commit()
    return jsonify({'msg': 'Appointment updated'})

@bp.route('/<int:appointment_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({'msg': 'Appointment deleted'})
