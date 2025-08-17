from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, WoundCarePlan, User
from datetime import datetime

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
    try:
        plans = WoundCarePlan.query.all()
        return jsonify([
            {
                'id': p.id,
                'patient_id': p.patient_id,
                'care_given': p.care_given,
                'date': p.date.isoformat() if p.date else None
            } for p in plans
        ])
    except Exception as e:
        return jsonify({'msg': f'Error fetching wound care plans: {str(e)}'}), 500

@bp.route('/', methods=['POST'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def create_wound_care_plan():
    try:
        data = request.get_json()
        plan = WoundCarePlan(
            patient_id=data.get('patient_id'),
            care_given=data.get('care_given'),
            date=datetime.fromisoformat(data.get('date')) if data.get('date') else datetime.utcnow()
        )
        db.session.add(plan)
        db.session.commit()
        return jsonify({'msg': 'Wound care plan created', 'id': plan.id}), 201
    except Exception as e:
        return jsonify({'msg': f'Error creating wound care plan: {str(e)}'}), 500

@bp.route('/<int:plan_id>', methods=['GET'])
@jwt_required()
def get_wound_care_plan(plan_id):
    try:
        plan = WoundCarePlan.query.get_or_404(plan_id)
        return jsonify({
            'id': plan.id,
            'patient_id': plan.patient_id,
            'care_given': plan.care_given,
            'date': plan.date.isoformat() if plan.date else None
        })
    except Exception as e:
        return jsonify({'msg': f'Error fetching wound care plan: {str(e)}'}), 500

@bp.route('/<int:plan_id>', methods=['PUT'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def update_wound_care_plan(plan_id):
    try:
        plan = WoundCarePlan.query.get_or_404(plan_id)
        data = request.get_json()
        
        if 'care_given' in data:
            plan.care_given = data['care_given']
        if 'date' in data:
            plan.date = datetime.fromisoformat(data['date']) if data['date'] else plan.date
            
        db.session.commit()
        return jsonify({'msg': 'Wound care plan updated'})
    except Exception as e:
        return jsonify({'msg': f'Error updating wound care plan: {str(e)}'}), 500

@bp.route('/<int:plan_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_wound_care_plan(plan_id):
    try:
        plan = WoundCarePlan.query.get_or_404(plan_id)
        db.session.delete(plan)
        db.session.commit()
        return jsonify({'msg': 'Wound care plan deleted'})
    except Exception as e:
        return jsonify({'msg': f'Error deleting wound care plan: {str(e)}'}), 500

@bp.route('/patient/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient_wound_care_plans(patient_id):
    try:
        plans = WoundCarePlan.query.filter_by(patient_id=patient_id).all()
        return jsonify([
            {
                'id': p.id,
                'patient_id': p.patient_id,
                'care_given': p.care_given,
                'date': p.date.isoformat() if p.date else None
            } for p in plans
        ])
    except Exception as e:
        return jsonify({'msg': f'Error fetching patient wound care plans: {str(e)}'}), 500
