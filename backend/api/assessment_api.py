from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, Assessment, User

bp = Blueprint('assessment_api', __name__, url_prefix='/api/assessments')

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
def get_assessments():
    assessments = Assessment.query.all()
    return jsonify([{
        'id': a.id,
        'user_id': a.user_id,
        'scheduled_date': a.scheduled_date.isoformat() if a.scheduled_date else None,
        'completed': a.completed,
        'score': a.score
    } for a in assessments])

@bp.route('/', methods=['POST'])
@role_required(['admin'])
def create_assessment():
    data = request.get_json()
    assessment = Assessment(
        user_id=data.get('user_id'),
        scheduled_date=data.get('scheduled_date'),
        completed=data.get('completed', False),
        score=data.get('score')
    )
    db.session.add(assessment)
    db.session.commit()
    return jsonify({'msg': 'Assessment created', 'id': assessment.id}), 201

@bp.route('/<int:assessment_id>', methods=['GET'])
@jwt_required()
def get_assessment(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    return jsonify({
        'id': assessment.id,
        'user_id': assessment.user_id,
        'scheduled_date': assessment.scheduled_date.isoformat() if assessment.scheduled_date else None,
        'completed': assessment.completed,
        'score': assessment.score
    })

@bp.route('/<int:assessment_id>', methods=['PUT'])
@role_required(['admin'])
def update_assessment(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    data = request.get_json()
    assessment.scheduled_date = data.get('scheduled_date', assessment.scheduled_date)
    assessment.completed = data.get('completed', assessment.completed)
    assessment.score = data.get('score', assessment.score)
    db.session.commit()
    return jsonify({'msg': 'Assessment updated'})

@bp.route('/<int:assessment_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_assessment(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    db.session.delete(assessment)
    db.session.commit()
    return jsonify({'msg': 'Assessment deleted'})
