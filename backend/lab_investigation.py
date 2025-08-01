from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, LabInvestigation, User

bp = Blueprint('lab_investigation', __name__, url_prefix='/api/lab-investigations')

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
def get_lab_investigations():
    investigations = LabInvestigation.query.all()
    return jsonify([{
        'id': i.id,
        'patient_id': i.patient_id,
        'investigation': i.investigation,
        'result': i.result,
        'date': i.date.isoformat() if i.date else None
    } for i in investigations])

@bp.route('/', methods=['POST'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def create_lab_investigation():
    data = request.get_json()
    investigation = LabInvestigation(
        patient_id=data.get('patient_id'),
        investigation=data.get('investigation'),
        result=data.get('result'),
        date=data.get('date')
    )
    db.session.add(investigation)
    db.session.commit()
    return jsonify({'msg': 'Lab investigation created', 'id': investigation.id}), 201

@bp.route('/<int:investigation_id>', methods=['GET'])
@jwt_required()
def get_lab_investigation(investigation_id):
    investigation = LabInvestigation.query.get_or_404(investigation_id)
    return jsonify({
        'id': investigation.id,
        'patient_id': investigation.patient_id,
        'investigation': investigation.investigation,
        'result': investigation.result,
        'date': investigation.date.isoformat() if investigation.date else None
    })

@bp.route('/<int:investigation_id>', methods=['PUT'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def update_lab_investigation(investigation_id):
    investigation = LabInvestigation.query.get_or_404(investigation_id)
    data = request.get_json()
    investigation.investigation = data.get('investigation', investigation.investigation)
    investigation.result = data.get('result', investigation.result)
    investigation.date = data.get('date', investigation.date)
    db.session.commit()
    return jsonify({'msg': 'Lab investigation updated'})

@bp.route('/<int:investigation_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_lab_investigation(investigation_id):
    investigation = LabInvestigation.query.get_or_404(investigation_id)
    db.session.delete(investigation)
    db.session.commit()
    return jsonify({'msg': 'Lab investigation deleted'})
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, LabInvestigation, User

bp = Blueprint('lab_investigation', __name__, url_prefix='/api/lab-investigations')

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
def get_lab_investigations():
    investigations = LabInvestigation.query.all()
    return jsonify([{
        'id': i.id,
        'patient_id': i.patient_id,
        'investigation': i.investigation,
        'result': i.result,
        'date': i.date.isoformat() if i.date else None
    } for i in investigations])

@bp.route('/', methods=['POST'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def create_lab_investigation():
    data = request.get_json()
    investigation = LabInvestigation(
        patient_id=data.get('patient_id'),
        investigation=data.get('investigation'),
        result=data.get('result'),
        date=data.get('date')
    )
    db.session.add(investigation)
    db.session.commit()
    return jsonify({'msg': 'Lab investigation created', 'id': investigation.id}), 201

@bp.route('/<int:investigation_id>', methods=['GET'])
@jwt_required()
def get_lab_investigation(investigation_id):
    investigation = LabInvestigation.query.get_or_404(investigation_id)
    return jsonify({
        'id': investigation.id,
        'patient_id': investigation.patient_id,
        'investigation': investigation.investigation,
        'result': investigation.result,
        'date': investigation.date.isoformat() if investigation.date else None
    })

@bp.route('/<int:investigation_id>', methods=['PUT'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def update_lab_investigation(investigation_id):
    investigation = LabInvestigation.query.get_or_404(investigation_id)
    data = request.get_json()
    investigation.investigation = data.get('investigation', investigation.investigation)
    investigation.result = data.get('result', investigation.result)
    investigation.date = data.get('date', investigation.date)
    db.session.commit()
    return jsonify({'msg': 'Lab investigation updated'})

@bp.route('/<int:investigation_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_lab_investigation(investigation_id):
    investigation = LabInvestigation.query.get_or_404(investigation_id)
    db.session.delete(investigation)
    db.session.commit()
    return jsonify({'msg': 'Lab investigation deleted'})
