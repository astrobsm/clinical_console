from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, Discharge, DischargeSummary, Patient
from backend.utils import roles_required

bp = Blueprint('discharge', __name__, url_prefix='/api/discharge')

@bp.route('/<int:patient_id>', methods=['POST'])
@jwt_required()
def discharge_patient(patient_id):
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    summary_text = data.get('summary_text')
    if not summary_text:
        return jsonify({'msg': 'Discharge summary required'}), 400
    summary = DischargeSummary(patient_id=patient_id, summary_text=summary_text)
    db.session.add(summary)
    db.session.commit()
    discharge = Discharge(patient_id=patient_id, discharged_by=user_id, summary_id=summary.id)
    db.session.add(discharge)
    db.session.commit()
    return jsonify({'msg': 'Patient discharged', 'discharge_id': discharge.id, 'summary_id': summary.id}), 201

@bp.route('/summary/<int:summary_id>', methods=['GET'])
@jwt_required()
def get_discharge_summary(summary_id):
    summary = DischargeSummary.query.get_or_404(summary_id)
    return jsonify({
        'id': summary.id,
        'patient_id': summary.patient_id,
        'summary_text': summary.summary_text,
        'created_at': summary.created_at.isoformat() if summary.created_at else None
    })
