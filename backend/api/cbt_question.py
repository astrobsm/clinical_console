from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, CBTQuestion, User

bp = Blueprint('cbt_question', __name__, url_prefix='/api/cbt-questions')

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
def get_cbt_questions():
    questions = CBTQuestion.query.all()
    return jsonify([{
        'id': q.id,
        'diagnosis': q.diagnosis,
        'question': q.question,
        'option_a': q.option_a,
        'option_b': q.option_b,
        'option_c': q.option_c,
        'option_d': q.option_d,
        'option_e': q.option_e,
        'correct_option': q.correct_option
    } for q in questions])

@bp.route('/', methods=['POST'])
@role_required(['admin'])
def create_cbt_question():
    data = request.get_json()
    question = CBTQuestion(
        diagnosis=data.get('diagnosis'),
        question=data.get('question'),
        option_a=data.get('option_a'),
        option_b=data.get('option_b'),
        option_c=data.get('option_c'),
        option_d=data.get('option_d'),
        option_e=data.get('option_e'),
        correct_option=data.get('correct_option')
    )
    db.session.add(question)
    db.session.commit()
    return jsonify({'msg': 'CBT question created', 'id': question.id}), 201

@bp.route('/<int:question_id>', methods=['GET'])
@jwt_required()
def get_cbt_question(question_id):
    question = CBTQuestion.query.get_or_404(question_id)
    return jsonify({
        'id': question.id,
        'diagnosis': question.diagnosis,
        'question': question.question,
        'option_a': question.option_a,
        'option_b': question.option_b,
        'option_c': question.option_c,
        'option_d': question.option_d,
        'option_e': question.option_e,
        'correct_option': question.correct_option
    })

@bp.route('/<int:question_id>', methods=['PUT'])
@role_required(['admin'])
def update_cbt_question(question_id):
    question = CBTQuestion.query.get_or_404(question_id)
    data = request.get_json()
    question.diagnosis = data.get('diagnosis', question.diagnosis)
    question.question = data.get('question', question.question)
    question.option_a = data.get('option_a', question.option_a)
    question.option_b = data.get('option_b', question.option_b)
    question.option_c = data.get('option_c', question.option_c)
    question.option_d = data.get('option_d', question.option_d)
    question.option_e = data.get('option_e', question.option_e)
    question.correct_option = data.get('correct_option', question.correct_option)
    db.session.commit()
    return jsonify({'msg': 'CBT question updated'})

@bp.route('/<int:question_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_cbt_question(question_id):
    question = CBTQuestion.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({'msg': 'CBT question deleted'})
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, CBTQuestion, User

bp = Blueprint('cbt_question', __name__, url_prefix='/api/cbt-questions')

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
def get_cbt_questions():
    questions = CBTQuestion.query.all()
    return jsonify([{
        'id': q.id,
        'diagnosis': q.diagnosis,
        'question': q.question,
        'option_a': q.option_a,
        'option_b': q.option_b,
        'option_c': q.option_c,
        'option_d': q.option_d,
        'option_e': q.option_e,
        'correct_option': q.correct_option
    } for q in questions])

@bp.route('/', methods=['POST'])
@role_required(['admin'])
def create_cbt_question():
    data = request.get_json()
    question = CBTQuestion(
        diagnosis=data.get('diagnosis'),
        question=data.get('question'),
        option_a=data.get('option_a'),
        option_b=data.get('option_b'),
        option_c=data.get('option_c'),
        option_d=data.get('option_d'),
        option_e=data.get('option_e'),
        correct_option=data.get('correct_option')
    )
    db.session.add(question)
    db.session.commit()
    return jsonify({'msg': 'CBT question created', 'id': question.id}), 201

@bp.route('/<int:question_id>', methods=['GET'])
@jwt_required()
def get_cbt_question(question_id):
    question = CBTQuestion.query.get_or_404(question_id)
    return jsonify({
        'id': question.id,
        'diagnosis': question.diagnosis,
        'question': question.question,
        'option_a': question.option_a,
        'option_b': question.option_b,
        'option_c': question.option_c,
        'option_d': question.option_d,
        'option_e': question.option_e,
        'correct_option': question.correct_option
    })

@bp.route('/<int:question_id>', methods=['PUT'])
@role_required(['admin'])
def update_cbt_question(question_id):
    question = CBTQuestion.query.get_or_404(question_id)
    data = request.get_json()
    question.diagnosis = data.get('diagnosis', question.diagnosis)
    question.question = data.get('question', question.question)
    question.option_a = data.get('option_a', question.option_a)
    question.option_b = data.get('option_b', question.option_b)
    question.option_c = data.get('option_c', question.option_c)
    question.option_d = data.get('option_d', question.option_d)
    question.option_e = data.get('option_e', question.option_e)
    question.correct_option = data.get('correct_option', question.correct_option)
    db.session.commit()
    return jsonify({'msg': 'CBT question updated'})

@bp.route('/<int:question_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_cbt_question(question_id):
    question = CBTQuestion.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({'msg': 'CBT question deleted'})
