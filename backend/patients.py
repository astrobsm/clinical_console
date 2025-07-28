# RESTful Patient API with JWT and role-based access
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
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
    patients = Patient.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'dob': p.dob.isoformat() if p.dob else None,
        'gender': p.gender,
        'inpatient': p.inpatient,
        'date_registered': p.date_registered.isoformat() if p.date_registered else None,
        'consultant_id': p.consultant_id
    } for p in patients])

@bp.route('/', methods=['POST'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def create_patient():
    data = request.get_json()
    patient = Patient(
        name=data.get('name'),
        dob=data.get('dob'),
        gender=data.get('gender'),
        inpatient=data.get('inpatient', False),
        consultant_id=data.get('consultant_id'),
        senior_registrar_id=data.get('senior_registrar_id'),
        registrar_id=data.get('registrar_id'),
        house_officer_id=data.get('house_officer_id')
    )
    db.session.add(patient)
    db.session.commit()
    return jsonify({'msg': 'Patient created', 'id': patient.id}), 201

@bp.route('/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return jsonify({
        'id': patient.id,
        'name': patient.name,
        'dob': patient.dob.isoformat() if patient.dob else None,
        'gender': patient.gender,
        'inpatient': patient.inpatient,
        'date_registered': patient.date_registered.isoformat() if patient.date_registered else None,
        'consultant_id': patient.consultant_id
    })

@bp.route('/<int:patient_id>', methods=['PUT'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    data = request.get_json()
    patient.name = data.get('name', patient.name)
    patient.dob = data.get('dob', patient.dob)
    patient.gender = data.get('gender', patient.gender)
    patient.inpatient = data.get('inpatient', patient.inpatient)
    patient.consultant_id = data.get('consultant_id', patient.consultant_id)
    patient.senior_registrar_id = data.get('senior_registrar_id', patient.senior_registrar_id)
    patient.registrar_id = data.get('registrar_id', patient.registrar_id)
    patient.house_officer_id = data.get('house_officer_id', patient.house_officer_id)
    db.session.commit()
    return jsonify({'msg': 'Patient updated'})

@bp.route('/<int:patient_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({'msg': 'Patient deleted'})

bp = Blueprint('patients', __name__, url_prefix='/api/patients')

@bp.route('/', methods=['GET'])
@jwt_required()
def list_patients():
    patients = Patient.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'dob': p.dob.isoformat() if p.dob else None,
        'gender': p.gender,
        'inpatient': p.inpatient,
        'date_registered': p.date_registered.isoformat() if p.date_registered else None,
        'consultant_id': p.consultant_id,
        'senior_registrar_id': p.senior_registrar_id,
        'registrar_id': p.registrar_id,
        'house_officer_id': p.house_officer_id
    } for p in patients])

@bp.route('/', methods=['POST'])
@jwt_required()
def create_patient():
    data = request.get_json()
    name = data.get('name')
    dob = data.get('dob')
    gender = data.get('gender')
    inpatient = data.get('inpatient', False)
    consultant_id = data.get('consultant_id')
    senior_registrar_id = data.get('senior_registrar_id')
    registrar_id = data.get('registrar_id')
    house_officer_id = data.get('house_officer_id')
    if not name:
        return jsonify({'msg': 'Name is required'}), 400
    patient = Patient(
        name=name,
        dob=dob,
        gender=gender,
        inpatient=inpatient,
        consultant_id=consultant_id,
        senior_registrar_id=senior_registrar_id,
        registrar_id=registrar_id,
        house_officer_id=house_officer_id
    )
    db.session.add(patient)
    db.session.commit()
    return jsonify({'msg': 'Patient created', 'id': patient.id}), 201

@bp.route('/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return jsonify({
        'id': patient.id,
        'name': patient.name,
        'dob': patient.dob.isoformat() if patient.dob else None,
        'gender': patient.gender,
        'inpatient': patient.inpatient,
        'date_registered': patient.date_registered.isoformat() if patient.date_registered else None,
        'consultant_id': patient.consultant_id,
        'senior_registrar_id': patient.senior_registrar_id,
        'registrar_id': patient.registrar_id,
        'house_officer_id': patient.house_officer_id
    })

@bp.route('/<int:patient_id>', methods=['PUT'])
@jwt_required()
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    data = request.get_json()
    for field in ['name', 'dob', 'gender', 'inpatient', 'consultant_id', 'senior_registrar_id', 'registrar_id', 'house_officer_id']:
        if field in data:
            setattr(patient, field, data[field])
    db.session.commit()
    return jsonify({'msg': 'Patient updated'})

@bp.route('/<int:patient_id>', methods=['DELETE'])
@jwt_required()
def delete_patient(patient_id):
    claims = get_jwt()
    if claims.get('role') not in ['consultant', 'admin']:
        return jsonify({'msg': 'Only consultants or admin can delete patients'}), 403
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({'msg': 'Patient deleted'})
