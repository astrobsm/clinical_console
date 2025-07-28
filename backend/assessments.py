from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from backend.models import db, Assessment, CBTQuestion, Score

bp = Blueprint('assessments', __name__, url_prefix='/api/assessments')

@bp.route('/', methods=['GET'])
@jwt_required()
def list_assessments():
    user_id = get_jwt_identity()
    assessments = Assessment.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            'id': a.id,
            'scheduled_date': a.scheduled_date.isoformat() if a.scheduled_date else None,
            'completed': a.completed,
            'score': a.score
        } for a in assessments
    ])

@bp.route('/cbt', methods=['GET'])
@jwt_required()
def get_cbt_questions():
    # Example: return 20 random questions
    questions = CBTQuestion.query.order_by(db.func.random()).limit(20).all()
    return jsonify([
        {
            'id': q.id,
            'diagnosis': q.diagnosis,
            'question': q.question,
            'option_a': q.option_a,
            'option_b': q.option_b,
            'option_c': q.option_c,
            'option_d': q.option_d,
            'option_e': q.option_e
        } for q in questions
    ])

@bp.route('/score', methods=['POST'])
@jwt_required()
def submit_score():
    user_id = get_jwt_identity()
    data = request.get_json()
    assessment_id = data.get('assessment_id')
    value = data.get('value')
    if not assessment_id or value is None:
        return jsonify({'msg': 'Assessment ID and value required'}), 400
    score = Score(user_id=user_id, assessment_id=assessment_id, value=value)
    db.session.add(score)
    db.session.commit()
    return jsonify({'msg': 'Score submitted'})
