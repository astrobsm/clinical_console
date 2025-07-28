from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, Discharge, User

bp = Blueprint('discharge_api', __name__, url_prefix='/api/discharges')

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
def get_discharges():
    discharges = Discharge.query.all()
    return jsonify([{
        'id': d.id,
        'patient_id': d.patient_id,
        'date': d.date.isoformat() if d.date else None,
        'discharged_by': d.discharged_by,
        'summary_id': d.summary_id
    } for d in discharges])

@bp.route('/', methods=['POST'])
@role_required(['admin'])
def create_discharge():
    data = request.get_json()
    discharge = Discharge(
        patient_id=data.get('patient_id'),
        date=data.get('date'),
        discharged_by=data.get('discharged_by'),
        summary_id=data.get('summary_id')
    )
    db.session.add(discharge)
    db.session.commit()
    return jsonify({'msg': 'Discharge created', 'id': discharge.id}), 201

@bp.route('/<int:discharge_id>', methods=['GET'])
@jwt_required()
def get_discharge(discharge_id):
    discharge = Discharge.query.get_or_404(discharge_id)
    return jsonify({
        'id': discharge.id,
        'patient_id': discharge.patient_id,
        'date': discharge.date.isoformat() if discharge.date else None,
        'discharged_by': discharge.discharged_by,
        'summary_id': discharge.summary_id
    })

@bp.route('/<int:discharge_id>', methods=['PUT'])
@role_required(['admin'])
def update_discharge(discharge_id):
    discharge = Discharge.query.get_or_404(discharge_id)
    data = request.get_json()
    discharge.date = data.get('date', discharge.date)
    discharge.discharged_by = data.get('discharged_by', discharge.discharged_by)
    discharge.summary_id = data.get('summary_id', discharge.summary_id)
    db.session.commit()
    return jsonify({'msg': 'Discharge updated'})

@bp.route('/<int:discharge_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_discharge(discharge_id):
    discharge = Discharge.query.get_or_404(discharge_id)
    db.session.delete(discharge)
    db.session.commit()
    return jsonify({'msg': 'Discharge deleted'})
