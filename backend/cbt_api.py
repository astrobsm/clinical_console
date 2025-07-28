from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from backend.models import db, Diagnosis, LabInvestigation, Score, User
import openai
import os

bp = Blueprint('cbt', __name__, url_prefix='/api/cbt')

@bp.route('/weekly-diagnoses', methods=['GET'])
@jwt_required()
def get_weekly_diagnoses():
    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)
    diagnoses = Diagnosis.query.filter(Diagnosis.date >= week_ago).all()
    result = []
    for d in diagnoses:
        labs = LabInvestigation.query.filter_by(patient_id=d.patient_id).all()
        result.append({
            'diagnosis': d.diagnosis,
            'date': d.date.isoformat(),
            'patient_id': d.patient_id,
            'lab_results': [{'investigation': l.investigation, 'result': l.result} for l in labs]
        })
    return jsonify(result)

@bp.route('/generate-mcqs', methods=['POST'])
@jwt_required()
def generate_mcqs():
    import json
    try:
        data = request.get_json()
        diagnoses = data.get('diagnoses', [])
        openai.api_key = os.getenv('OPENAI_API_KEY')
        print('OPENAI_API_KEY loaded:', bool(openai.api_key), '| Value:', (openai.api_key[:6] + '...' if openai.api_key else None))
        if not diagnoses or not openai.api_key:
            return jsonify({'questions': [], 'error': 'No diagnoses provided or OpenAI key missing.'}), 200
        prompt = (
            "For each of the following diagnoses: " + "; ".join(diagnoses) + ". "
            "Generate multiple standard, midlevel-difficulty clinical MCQs (with options a-e, only one correct answer, 4 points each) "
            "that assess: general knowledge, pathology, clinical features, investigations, management approaches, and complications. "
            "Distribute questions to cover all these aspects for each diagnosis. "
            "Format: For each question, provide: 'question', 'options' (a-e), and 'answer' (the correct option letter). Return as a JSON array."
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000,
            temperature=0.7,
        )
        try:
            questions = json.loads(response.choices[0].message['content'])
        except Exception:
            questions = response.choices[0].message['content']
        return jsonify({'questions': questions})
    except Exception as e:
        import traceback
        print('MCQ generation error:', e)
        traceback.print_exc()
        return jsonify({'questions': [], 'error': str(e)}), 200

@bp.route('/submit-score', methods=['POST'])
@jwt_required()
def submit_score():
    user_id = get_jwt_identity()
    data = request.get_json()
    value = data.get('score')
    total = data.get('total', 100)  # default to 100 if not provided
    test_date = datetime.utcnow()
    percentage = (value / total) * 100 if total else None
    # Recommendation/advice logic
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
    s = Score(user_id=user_id, value=value, percentage=percentage, recommendation=recommendation, advice=advice, created_at=test_date)
    db.session.add(s)
    db.session.commit()
    return jsonify({'msg': 'Score saved', 'percentage': percentage, 'recommendation': recommendation, 'advice': advice})
