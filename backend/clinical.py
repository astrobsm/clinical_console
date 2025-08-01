from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.utils import roles_required
from backend.models import db, ClinicalEvaluation, Diagnosis, TreatmentPlan, LabInvestigation, ImagingInvestigation, WoundCarePlan, SurgeryBooking, Appointment

bp = Blueprint('clinical', __name__, url_prefix='/api/clinical')

# Clinical Evaluation
@bp.route('/evaluations', methods=['GET'])
@jwt_required()
def get_evaluations():
    evaluations = ClinicalEvaluation.query.all()

    return jsonify([
        {
            'id': e.id,
            'patient_id': e.patient_id,
            'summary': e.summary,
            'date': e.date.isoformat() if e.date else None
        } for e in evaluations
    ])



@bp.route('/<int:evaluation_id>', methods=['GET'])
@jwt_required()
def get_evaluation(evaluation_id):
    evaluation = ClinicalEvaluation.query.get_or_404(evaluation_id)
    return jsonify({
        'id': evaluation.id,
        'patient_id': evaluation.patient_id,
        'summary': evaluation.summary,
        'date': evaluation.date.isoformat() if evaluation.date else None
    })

@bp.route('/evaluations/<int:evaluation_id>', methods=['PUT'])
@jwt_required()
def update_evaluation(evaluation_id):
    evaluation = ClinicalEvaluation.query.get_or_404(evaluation_id)
    data = request.get_json()
    evaluation.summary = data.get('summary', evaluation.summary)
    evaluation.date = data.get('date', evaluation.date)
    db.session.commit()
    return jsonify({'msg': 'Evaluation updated'})

@bp.route('/evaluations/<int:evaluation_id>', methods=['DELETE'])
@jwt_required()
def delete_evaluation(evaluation_id):
    evaluation = ClinicalEvaluation.query.get_or_404(evaluation_id)
    db.session.delete(evaluation)
    db.session.commit()
    return jsonify({'msg': 'Evaluation deleted'})

    evaluation = ClinicalEvaluation.query.get_or_404(id)
    return jsonify({
        'id': evaluation.id,
        'patient_id': evaluation.patient_id,
        'summary': evaluation.summary,
        'date': evaluation.date.isoformat() if evaluation.date else None
    })

# Diagnosis
@bp.route('/diagnoses', methods=['POST'])
@jwt_required()
def create_diagnosis():
    data = request.get_json()
    diagnosis = Diagnosis(**data)
    db.session.add(diagnosis)
    db.session.commit()
    return jsonify({'msg': 'Diagnosis created', 'id': diagnosis.id}), 201

@bp.route('/diagnoses/<int:id>', methods=['GET'])
@jwt_required()
def get_diagnosis(id):
    diagnosis = Diagnosis.query.get_or_404(id)
    return jsonify({
        'id': diagnosis.id,
        'patient_id': diagnosis.patient_id,
        'diagnosis': diagnosis.diagnosis,
        'date': diagnosis.date.isoformat() if diagnosis.date else None
    })

# Treatment Plan
@bp.route('/treatmentplans', methods=['POST'])
@jwt_required()
def create_treatment_plan():
    data = request.get_json()
    plan = TreatmentPlan(**data)
    db.session.add(plan)
    db.session.commit()
    return jsonify({'msg': 'Treatment plan created', 'id': plan.id}), 201

@bp.route('/treatmentplans/<int:id>', methods=['GET'])
@jwt_required()
def get_treatment_plan(id):
    plan = TreatmentPlan.query.get_or_404(id)
    return jsonify({
        'id': plan.id,
        'patient_id': plan.patient_id,
        'plan': plan.plan,
        'date': plan.date.isoformat() if plan.date else None
    })

# Lab Investigation
@bp.route('/labinvestigations', methods=['POST'])
@jwt_required()
def create_lab_investigation():
    data = request.get_json()
    lab = LabInvestigation(**data)
    db.session.add(lab)
    db.session.commit()
    return jsonify({'msg': 'Lab investigation created', 'id': lab.id}), 201

@bp.route('/labinvestigations/<int:id>', methods=['GET'])
@jwt_required()
def get_lab_investigation(id):
    lab = LabInvestigation.query.get_or_404(id)
    return jsonify({
        'id': lab.id,
        'patient_id': lab.patient_id,
        'investigation': lab.investigation,
        'result': lab.result,
        'date': lab.date.isoformat() if lab.date else None
    })

# Imaging Investigation
@bp.route('/imaginginvestigations', methods=['POST'])
@jwt_required()
def create_imaging_investigation():
    data = request.get_json()
    img = ImagingInvestigation(**data)
    db.session.add(img)
    db.session.commit()
    return jsonify({'msg': 'Imaging investigation created', 'id': img.id}), 201

@bp.route('/imaginginvestigations/<int:id>', methods=['GET'])
@jwt_required()
def get_imaging_investigation(id):
    img = ImagingInvestigation.query.get_or_404(id)
    return jsonify({
        'id': img.id,
        'patient_id': img.patient_id,
        'investigation': img.investigation,
        'result': img.result,
        'date': img.date.isoformat() if img.date else None
    })

# Wound Care Plan
@bp.route('/woundcareplans', methods=['POST'])
@jwt_required()
def create_wound_care_plan():
    data = request.get_json()
    plan = WoundCarePlan(**data)
    db.session.add(plan)
    db.session.commit()
    return jsonify({'msg': 'Wound care plan created', 'id': plan.id}), 201

@bp.route('/woundcareplans/<int:id>', methods=['GET'])
@jwt_required()
def get_wound_care_plan(id):
    plan = WoundCarePlan.query.get_or_404(id)
    return jsonify({
        'id': plan.id,
        'patient_id': plan.patient_id,
        'plan': plan.plan,
        'date': plan.date.isoformat() if plan.date else None
    })

# Surgery Booking
@bp.route('/surgerybookings', methods=['POST'])
@roles_required('consultant', 'admin')
def create_surgery_booking():
    data = request.get_json()
    booking = SurgeryBooking(**data)
    db.session.add(booking)
    db.session.commit()
    return jsonify({'msg': 'Surgery booking created', 'id': booking.id}), 201

@bp.route('/surgerybookings/<int:id>', methods=['GET'])
@jwt_required()
def get_surgery_booking(id):
    booking = SurgeryBooking.query.get_or_404(id)
    return jsonify({
        'id': booking.id,
        'patient_id': booking.patient_id,
        'surgery_type': booking.surgery_type,
        'date_booked': booking.date_booked.isoformat() if booking.date_booked else None,
        'scheduled_date': booking.scheduled_date.isoformat() if booking.scheduled_date else None
    })

# Appointment
@bp.route('/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    data = request.get_json()
    appt = Appointment(**data)
    db.session.add(appt)
    db.session.commit()
    return jsonify({'msg': 'Appointment created', 'id': appt.id}), 201

@bp.route('/appointments/<int:id>', methods=['GET'])
@jwt_required()
def get_appointment(id):
    appt = Appointment.query.get_or_404(id)
    return jsonify({
        'id': appt.id,
        'patient_id': appt.patient_id,
        'date': appt.date.isoformat() if appt.date else None,
        'purpose': appt.purpose
    })
