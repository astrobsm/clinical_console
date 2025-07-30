from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, ImagingInvestigation, User

bp = Blueprint('imaging_investigation', __name__, url_prefix='/api/imaging-investigations')

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
def get_imaging_investigations():
    investigations = ImagingInvestigation.query.all()
    result = []
    for i in investigations:
        patient = i.patient
        patient_data = None
        if patient:
            patient_data = {
                'id': patient.id,
                'name': patient.name,
                'dob': patient.dob.isoformat() if patient.dob else None,
                'gender': patient.gender,
                'inpatient': patient.inpatient,
                'date_registered': patient.date_registered.isoformat() if patient.date_registered else None
            }
        result.append({
            'id': i.id,
            'patient_id': i.patient_id,
            'patient': patient_data,
            'investigation': i.investigation,
            'result': i.result,
            'date': i.date.isoformat() if i.date else None
        })
    return jsonify(result)

@bp.route('/', methods=['POST'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def create_imaging_investigation():
    data = request.get_json()
    investigation = ImagingInvestigation(
        patient_id=data.get('patient_id'),
        investigation=data.get('investigation'),
        result=data.get('result'),
        date=data.get('date')
    )
    db.session.add(investigation)
    db.session.commit()
    return jsonify({'msg': 'Imaging investigation created', 'id': investigation.id}), 201

@bp.route('/<int:investigation_id>', methods=['GET'])
@jwt_required()
def get_imaging_investigation(investigation_id):
    investigation = ImagingInvestigation.query.get_or_404(investigation_id)
    patient = investigation.patient
    patient_data = None
    if patient:
        patient_data = {
            'id': patient.id,
            'name': patient.name,
            'dob': patient.dob.isoformat() if patient.dob else None,
            'gender': patient.gender,
            'inpatient': patient.inpatient,
            'date_registered': patient.date_registered.isoformat() if patient.date_registered else None
        }
    return jsonify({
        'id': investigation.id,
        'patient_id': investigation.patient_id,
        'patient': patient_data,
        'investigation': investigation.investigation,
        'result': investigation.result,
        'date': investigation.date.isoformat() if investigation.date else None
    })

@bp.route('/<int:investigation_id>', methods=['PUT'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def update_imaging_investigation(investigation_id):
    investigation = ImagingInvestigation.query.get_or_404(investigation_id)
    data = request.get_json()
    investigation.investigation = data.get('investigation', investigation.investigation)
    investigation.result = data.get('result', investigation.result)
    investigation.date = data.get('date', investigation.date)
    db.session.commit()
    return jsonify({'msg': 'Imaging investigation updated'})

@bp.route('/<int:investigation_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_imaging_investigation(investigation_id):
    investigation = ImagingInvestigation.query.get_or_404(investigation_id)
    db.session.delete(investigation)
    db.session.commit()
    return jsonify({'msg': 'Imaging investigation deleted'})
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, ImagingInvestigation, User

bp = Blueprint('imaging_investigation', __name__, url_prefix='/api/imaging-investigations')

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
def get_imaging_investigations():
    investigations = ImagingInvestigation.query.all()
    result = []
    for i in investigations:
        patient = i.patient
        patient_data = None
        if patient:
            patient_data = {
                'id': patient.id,
                'name': patient.name,
                'dob': patient.dob.isoformat() if patient.dob else None,
                'gender': patient.gender,
                'inpatient': patient.inpatient,
                'date_registered': patient.date_registered.isoformat() if patient.date_registered else None
            }
        result.append({
            'id': i.id,
            'patient_id': i.patient_id,
            'patient': patient_data,
            'investigation': i.investigation,
            'result': i.result,
            'date': i.date.isoformat() if i.date else None
        })
    return jsonify(result)

@bp.route('/', methods=['POST'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def create_imaging_investigation():
    data = request.get_json()
    investigation = ImagingInvestigation(
        patient_id=data.get('patient_id'),
        investigation=data.get('investigation'),
        result=data.get('result'),
        date=data.get('date')
    )
    db.session.add(investigation)
    db.session.commit()
    return jsonify({'msg': 'Imaging investigation created', 'id': investigation.id}), 201

@bp.route('/<int:investigation_id>', methods=['GET'])
@jwt_required()
def get_imaging_investigation(investigation_id):
    investigation = ImagingInvestigation.query.get_or_404(investigation_id)
    patient = investigation.patient
    patient_data = None
    if patient:
        patient_data = {
            'id': patient.id,
            'name': patient.name,
            'dob': patient.dob.isoformat() if patient.dob else None,
            'gender': patient.gender,
            'inpatient': patient.inpatient,
            'date_registered': patient.date_registered.isoformat() if patient.date_registered else None
        }
    return jsonify({
        'id': investigation.id,
        'patient_id': investigation.patient_id,
        'patient': patient_data,
        'investigation': investigation.investigation,
        'result': investigation.result,
        'date': investigation.date.isoformat() if investigation.date else None
    })

@bp.route('/<int:investigation_id>', methods=['PUT'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def update_imaging_investigation(investigation_id):
    investigation = ImagingInvestigation.query.get_or_404(investigation_id)
    data = request.get_json()
    investigation.investigation = data.get('investigation', investigation.investigation)
    investigation.result = data.get('result', investigation.result)
    investigation.date = data.get('date', investigation.date)
    db.session.commit()
    return jsonify({'msg': 'Imaging investigation updated'})

@bp.route('/<int:investigation_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_imaging_investigation(investigation_id):
    investigation = ImagingInvestigation.query.get_or_404(investigation_id)
    db.session.delete(investigation)
    db.session.commit()
    return jsonify({'msg': 'Imaging investigation deleted'})
