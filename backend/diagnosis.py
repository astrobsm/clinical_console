from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, Diagnosis, User

bp = Blueprint('diagnosis', __name__, url_prefix='/api/diagnosis')

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
def get_diagnoses():
    diagnoses = Diagnosis.query.all()
    return jsonify([{
        'id': d.id,
        'patient_id': d.patient_id,
        'diagnosis': d.diagnosis,
        'date': d.date.isoformat() if d.date else None
    } for d in diagnoses])

@bp.route('/', methods=['POST'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def create_diagnosis():
    data = request.get_json()
    diagnosis = Diagnosis(
        patient_id=data.get('patient_id'),
        diagnosis=data.get('diagnosis'),
        date=data.get('date')
    )
    db.session.add(diagnosis)
    db.session.commit()
    return jsonify({'msg': 'Diagnosis created', 'id': diagnosis.id}), 201

@bp.route('/<int:diagnosis_id>', methods=['GET'])
@jwt_required()
def get_diagnosis(diagnosis_id):
    diagnosis = Diagnosis.query.get_or_404(diagnosis_id)
    return jsonify({
        'id': diagnosis.id,
        'patient_id': diagnosis.patient_id,
        'diagnosis': diagnosis.diagnosis,
        'date': diagnosis.date.isoformat() if diagnosis.date else None
    })

@bp.route('/<int:diagnosis_id>', methods=['PUT'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def update_diagnosis(diagnosis_id):
    diagnosis = Diagnosis.query.get_or_404(diagnosis_id)
    data = request.get_json()
    diagnosis.diagnosis = data.get('diagnosis', diagnosis.diagnosis)
    diagnosis.date = data.get('date', diagnosis.date)
    db.session.commit()
    return jsonify({'msg': 'Diagnosis updated'})

@bp.route('/<int:diagnosis_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_diagnosis(diagnosis_id):
    diagnosis = Diagnosis.query.get_or_404(diagnosis_id)
    db.session.delete(diagnosis)
    db.session.commit()
    return jsonify({'msg': 'Diagnosis deleted'})
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, Diagnosis, User

bp = Blueprint('diagnosis', __name__, url_prefix='/api/diagnosis')

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
def get_diagnoses():
    diagnoses = Diagnosis.query.all()
    return jsonify([{
        'id': d.id,
        'patient_id': d.patient_id,
        'diagnosis': d.diagnosis,
        'date': d.date.isoformat() if d.date else None
    } for d in diagnoses])

@bp.route('/', methods=['POST'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def create_diagnosis():
    data = request.get_json()
    diagnosis = Diagnosis(
        patient_id=data.get('patient_id'),
        diagnosis=data.get('diagnosis'),
        date=data.get('date')
    )
    db.session.add(diagnosis)
    db.session.commit()
    return jsonify({'msg': 'Diagnosis created', 'id': diagnosis.id}), 201

@bp.route('/<int:diagnosis_id>', methods=['GET'])
@jwt_required()
def get_diagnosis(diagnosis_id):
    diagnosis = Diagnosis.query.get_or_404(diagnosis_id)
    return jsonify({
        'id': diagnosis.id,
        'patient_id': diagnosis.patient_id,
        'diagnosis': diagnosis.diagnosis,
        'date': diagnosis.date.isoformat() if diagnosis.date else None
    })

@bp.route('/<int:diagnosis_id>', methods=['PUT'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def update_diagnosis(diagnosis_id):
    diagnosis = Diagnosis.query.get_or_404(diagnosis_id)
    data = request.get_json()
    diagnosis.diagnosis = data.get('diagnosis', diagnosis.diagnosis)
    diagnosis.date = data.get('date', diagnosis.date)
    db.session.commit()
    return jsonify({'msg': 'Diagnosis updated'})

@bp.route('/<int:diagnosis_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_diagnosis(diagnosis_id):
    diagnosis = Diagnosis.query.get_or_404(diagnosis_id)
    db.session.delete(diagnosis)
    db.session.commit()
    return jsonify({'msg': 'Diagnosis deleted'})
