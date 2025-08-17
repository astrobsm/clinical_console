from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, WoundCarePlan, User

bp = Blueprint('wound_care', __name__, url_prefix='/api/wound-care')

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
def get_wound_care_plans():
    plans = WoundCarePlan.query.all()
    return jsonify([
        {
            'id': p.id,
            'patient_id': p.patient_id,
            'dressing_protocol': p.dressing_protocol,
            'phase': p.phase,
            'comorbidities': p.comorbidities,
            'images': p.images,
            'date': p.date.isoformat() if p.date else None
        } for p in plans
    ])

@bp.route('/', methods=['POST'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def create_wound_care_plan():
    data = request.get_json()
    plan = WoundCarePlan(
        patient_id=data.get('patient_id'),
        dressing_protocol=data.get('dressing_protocol'),
        phase=data.get('phase'),
        comorbidities=','.join(data.get('comorbidities', [])) if isinstance(data.get('comorbidities'), list) else data.get('comorbidities'),
        images=','.join(data.get('images', [])) if isinstance(data.get('images'), list) else data.get('images'),
        date=data.get('date')
    )
    db.session.add(plan)
    db.session.commit()
    return jsonify({'msg': 'Wound care plan created', 'id': plan.id}), 201

@bp.route('/<int:plan_id>', methods=['GET'])
@jwt_required()
def get_wound_care_plan(plan_id):
    plan = WoundCarePlan.query.get_or_404(plan_id)
    return jsonify({
        'id': plan.id,
        'patient_id': plan.patient_id,
        'dressing_protocol': plan.dressing_protocol,
        'phase': plan.phase,
        'comorbidities': plan.comorbidities,
        'images': plan.images,
        'date': plan.date.isoformat() if plan.date else None
    })

@bp.route('/<int:plan_id>', methods=['PUT'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def update_wound_care_plan(plan_id):
    plan = WoundCarePlan.query.get_or_404(plan_id)
    data = request.get_json()
    plan.dressing_protocol = data.get('dressing_protocol', plan.dressing_protocol)
    plan.phase = data.get('phase', plan.phase)
    plan.comorbidities = ','.join(data.get('comorbidities', plan.comorbidities.split(','))) if isinstance(data.get('comorbidities'), list) else data.get('comorbidities') or plan.comorbidities
    plan.images = ','.join(data.get('images', plan.images.split(','))) if isinstance(data.get('images'), list) else data.get('images') or plan.images
    plan.date = data.get('date', plan.date)
    db.session.commit()
    return jsonify({'msg': 'Wound care plan updated'})

@bp.route('/<int:plan_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_wound_care_plan(plan_id):
    plan = WoundCarePlan.query.get_or_404(plan_id)
    db.session.delete(plan)
    db.session.commit()
    return jsonify({'msg': 'Wound care plan deleted'})
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, WoundCarePlan, User

bp = Blueprint('wound_care', __name__, url_prefix='/api/wound-care')

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
def get_wound_care_plans():
    plans = WoundCarePlan.query.all()
    return jsonify([
        {
            'id': p.id,
            'patient_id': p.patient_id,
            'dressing_protocol': p.dressing_protocol,
            'phase': p.phase,
            'comorbidities': p.comorbidities,
            'images': p.images,
            'date': p.date.isoformat() if p.date else None
        } for p in plans
    ])

@bp.route('/', methods=['POST'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def create_wound_care_plan():
    data = request.get_json()
    plan = WoundCarePlan(
        patient_id=data.get('patient_id'),
        dressing_protocol=data.get('dressing_protocol'),
        phase=data.get('phase'),
        comorbidities=','.join(data.get('comorbidities', [])) if isinstance(data.get('comorbidities'), list) else data.get('comorbidities'),
        images=','.join(data.get('images', [])) if isinstance(data.get('images'), list) else data.get('images'),
        date=data.get('date')
    )
    db.session.add(plan)
    db.session.commit()
    return jsonify({'msg': 'Wound care plan created', 'id': plan.id}), 201

@bp.route('/<int:plan_id>', methods=['GET'])
@jwt_required()
def get_wound_care_plan(plan_id):
    plan = WoundCarePlan.query.get_or_404(plan_id)
    return jsonify({
        'id': plan.id,
        'patient_id': plan.patient_id,
        'dressing_protocol': plan.dressing_protocol,
        'phase': plan.phase,
        'comorbidities': plan.comorbidities,
        'images': plan.images,
        'date': plan.date.isoformat() if plan.date else None
    })

@bp.route('/<int:plan_id>', methods=['PUT'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def update_wound_care_plan(plan_id):
    plan = WoundCarePlan.query.get_or_404(plan_id)
    data = request.get_json()
    plan.dressing_protocol = data.get('dressing_protocol', plan.dressing_protocol)
    plan.phase = data.get('phase', plan.phase)
    plan.comorbidities = ','.join(data.get('comorbidities', plan.comorbidities.split(','))) if isinstance(data.get('comorbidities'), list) else data.get('comorbidities') or plan.comorbidities
    plan.images = ','.join(data.get('images', plan.images.split(','))) if isinstance(data.get('images'), list) else data.get('images') or plan.images
    plan.date = data.get('date', plan.date)
    db.session.commit()
    return jsonify({'msg': 'Wound care plan updated'})

@bp.route('/<int:plan_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_wound_care_plan(plan_id):
    plan = WoundCarePlan.query.get_or_404(plan_id)
    db.session.delete(plan)
    db.session.commit()
    return jsonify({'msg': 'Wound care plan deleted'})
