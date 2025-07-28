from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, DischargeSummary, User

bp = Blueprint('discharge_summary', __name__, url_prefix='/api/discharge-summaries')

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
def get_discharge_summaries():
    summaries = DischargeSummary.query.all()
    return jsonify([{
        'id': s.id,
        'patient_id': s.patient_id,
        'summary_text': s.summary_text,
        'created_at': s.created_at.isoformat() if s.created_at else None
    } for s in summaries])

@bp.route('/', methods=['POST'])
@role_required(['admin'])
def create_discharge_summary():
    data = request.get_json()
    summary = DischargeSummary(
        patient_id=data.get('patient_id'),
        summary_text=data.get('summary_text'),
        created_at=data.get('created_at')
    )
    db.session.add(summary)
    db.session.commit()
    return jsonify({'msg': 'Discharge summary created', 'id': summary.id}), 201

@bp.route('/<int:summary_id>', methods=['GET'])
@jwt_required()
def get_discharge_summary(summary_id):
    summary = DischargeSummary.query.get_or_404(summary_id)
    return jsonify({
        'id': summary.id,
        'patient_id': summary.patient_id,
        'summary_text': summary.summary_text,
        'created_at': summary.created_at.isoformat() if summary.created_at else None
    })

@bp.route('/<int:summary_id>', methods=['PUT'])
@role_required(['admin'])
def update_discharge_summary(summary_id):
    summary = DischargeSummary.query.get_or_404(summary_id)
    data = request.get_json()
    summary.summary_text = data.get('summary_text', summary.summary_text)
    summary.created_at = data.get('created_at', summary.created_at)
    db.session.commit()
    return jsonify({'msg': 'Discharge summary updated'})

@bp.route('/<int:summary_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_discharge_summary(summary_id):
    summary = DischargeSummary.query.get_or_404(summary_id)
    db.session.delete(summary)
    db.session.commit()
    return jsonify({'msg': 'Discharge summary deleted'})
