from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, Score, User

bp = Blueprint('score_api', __name__, url_prefix='/api/scores')

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
def get_scores():
    scores = Score.query.all()
    return jsonify([
        {
            'id': s.id,
            'user_id': s.user_id,
            'assessment_id': s.assessment_id,
            'value': s.value,
            'percentage': s.percentage,
            'recommendation': s.recommendation,
            'advice': s.advice,
            'created_at': s.created_at.isoformat() if s.created_at else None
        }
        for s in scores
    ])

@bp.route('/', methods=['POST'])
@role_required(['admin'])
def create_score():
    data = request.get_json()
    value = data.get('value')
    total = data.get('total', 100)  # default to 100 if not provided
    percentage = (value / total) * 100 if total else None
    # Simple recommendation/advice logic
    if percentage is not None:
        if percentage >= 80:
            recommendation = 'Excellent performance'
            advice = 'Keep up the great work!'
        elif percentage >= 60:
            recommendation = 'Good performance'
            advice = 'Review weak areas for improvement.'
        elif percentage >= 40:
            recommendation = 'Fair performance'
            advice = 'Consider more practice and revision.'
        else:
            recommendation = 'Needs improvement'
            advice = 'Seek help and focus on core concepts.'
    else:
        recommendation = None
        advice = None
    score = Score(
        user_id=data.get('user_id'),
        assessment_id=data.get('assessment_id'),
        value=value,
        percentage=percentage,
        recommendation=recommendation,
        advice=advice,
        created_at=data.get('created_at')
    )
    db.session.add(score)
    db.session.commit()
    return jsonify({'msg': 'Score created', 'id': score.id, 'percentage': percentage, 'recommendation': recommendation, 'advice': advice}), 201

@bp.route('/<int:score_id>', methods=['GET'])
@jwt_required()
def get_score(score_id):
    score = Score.query.get_or_404(score_id)
    return jsonify({
        'id': score.id,
        'user_id': score.user_id,
        'assessment_id': score.assessment_id,
        'value': score.value,
        'percentage': score.percentage,
        'recommendation': score.recommendation,
        'advice': score.advice,
        'created_at': score.created_at.isoformat() if score.created_at else None
    })

@bp.route('/<int:score_id>', methods=['PUT'])
@role_required(['admin'])
def update_score(score_id):
    score = Score.query.get_or_404(score_id)
    data = request.get_json()
    score.value = data.get('value', score.value)
    score.created_at = data.get('created_at', score.created_at)
    db.session.commit()
    return jsonify({'msg': 'Score updated'})

@bp.route('/<int:score_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_score(score_id):
    score = Score.query.get_or_404(score_id)
    db.session.delete(score)
    db.session.commit()
    return jsonify({'msg': 'Score deleted'})
