from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, TreatmentPlan, User

bp = Blueprint('treatment', __name__, url_prefix='/api/treatment')

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
def get_plans():
    plans = TreatmentPlan.query.all()
    return jsonify([{
        'id': p.id,
        'patient_id': p.patient_id,
        'plan': p.plan,
        'date': p.date.isoformat() if p.date else None
    } for p in plans])

@bp.route('/', methods=['POST'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def create_plan():
    data = request.get_json()
    plan = TreatmentPlan(
        patient_id=data.get('patient_id'),
        plan=data.get('plan'),
        date=data.get('date')
    )
    db.session.add(plan)
    db.session.commit()
    return jsonify({'msg': 'Treatment plan created', 'id': plan.id}), 201

@bp.route('/<int:plan_id>', methods=['GET'])
@jwt_required()
def get_plan(plan_id):
    plan = TreatmentPlan.query.get_or_404(plan_id)
    return jsonify({
        'id': plan.id,
        'patient_id': plan.patient_id,
        'plan': plan.plan,
        'date': plan.date.isoformat() if plan.date else None
    })

@bp.route('/<int:plan_id>', methods=['PUT'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def update_plan(plan_id):
    plan = TreatmentPlan.query.get_or_404(plan_id)
    data = request.get_json()
    plan.plan = data.get('plan', plan.plan)
    plan.date = data.get('date', plan.date)
    db.session.commit()
    return jsonify({'msg': 'Treatment plan updated'})

@bp.route('/<int:plan_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_plan(plan_id):
    plan = TreatmentPlan.query.get_or_404(plan_id)
    db.session.delete(plan)
    db.session.commit()
    return jsonify({'msg': 'Treatment plan deleted'})
