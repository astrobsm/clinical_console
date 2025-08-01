from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, SurgeryBooking, User

bp = Blueprint('surgery_booking', __name__, url_prefix='/api/surgery-bookings')

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
def get_surgery_bookings():
    bookings = SurgeryBooking.query.all()
    return jsonify([
        {
            'id': b.id,
            'patient_id': b.patient_id,
            'surgery_type': b.surgery_type,
            'date_booked': b.date_booked.isoformat() if b.date_booked else None,
            'scheduled_date': b.scheduled_date.isoformat() if b.scheduled_date else None,
            'clinical_images': b.clinical_images,
            'admission_type': b.admission_type,
            'ward': b.ward,
            'indications': b.indications,
            'requirements': b.requirements,
            'anaesthesia_type': b.anaesthesia_type,
            'position': b.position,
            'estimated_duration': b.estimated_duration,
            'comorbidities': b.comorbidities
        } for b in bookings
    ])

@bp.route('/', methods=['POST'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def create_surgery_booking():
    data = request.get_json()
    booking = SurgeryBooking(
        patient_id=data.get('patient_id'),
        surgery_type=data.get('surgery_type'),
        date_booked=data.get('date_booked'),
        scheduled_date=data.get('scheduled_date'),
        clinical_images=','.join(data.get('clinical_images', [])) if isinstance(data.get('clinical_images'), list) else data.get('clinical_images'),
        admission_type=data.get('admission_type'),
        ward=data.get('ward'),
        indications=data.get('indications'),
        requirements=','.join(data.get('requirements', [])) if isinstance(data.get('requirements'), list) else data.get('requirements'),
        anaesthesia_type=data.get('anaesthesia_type'),
        position=data.get('position'),
        estimated_duration=data.get('estimated_duration'),
        comorbidities=','.join(data.get('comorbidities', [])) if isinstance(data.get('comorbidities'), list) else data.get('comorbidities')
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({'msg': 'Surgery booking created', 'id': booking.id}), 201

@bp.route('/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_surgery_booking(booking_id):
    booking = SurgeryBooking.query.get_or_404(booking_id)
    return jsonify({
        'id': booking.id,
        'patient_id': booking.patient_id,
        'surgery_type': booking.surgery_type,
        'date_booked': booking.date_booked.isoformat() if booking.date_booked else None,
        'scheduled_date': booking.scheduled_date.isoformat() if booking.scheduled_date else None,
        'clinical_images': booking.clinical_images,
        'admission_type': booking.admission_type,
        'ward': booking.ward,
        'indications': booking.indications,
        'requirements': booking.requirements,
        'anaesthesia_type': booking.anaesthesia_type,
        'position': booking.position,
        'estimated_duration': booking.estimated_duration,
        'comorbidities': booking.comorbidities
    })

@bp.route('/<int:booking_id>', methods=['PUT'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def update_surgery_booking(booking_id):
    booking = SurgeryBooking.query.get_or_404(booking_id)
    data = request.get_json()
    booking.surgery_type = data.get('surgery_type', booking.surgery_type)
    booking.date_booked = data.get('date_booked', booking.date_booked)
    booking.scheduled_date = data.get('scheduled_date', booking.scheduled_date)
    booking.clinical_images = ','.join(data.get('clinical_images', booking.clinical_images.split(','))) if isinstance(data.get('clinical_images'), list) else data.get('clinical_images') or booking.clinical_images
    booking.admission_type = data.get('admission_type', booking.admission_type)
    booking.ward = data.get('ward', booking.ward)
    booking.indications = data.get('indications', booking.indications)
    booking.requirements = ','.join(data.get('requirements', booking.requirements.split(','))) if isinstance(data.get('requirements'), list) else data.get('requirements') or booking.requirements
    booking.anaesthesia_type = data.get('anaesthesia_type', booking.anaesthesia_type)
    booking.position = data.get('position', booking.position)
    booking.estimated_duration = data.get('estimated_duration', booking.estimated_duration)
    booking.comorbidities = ','.join(data.get('comorbidities', booking.comorbidities.split(','))) if isinstance(data.get('comorbidities'), list) else data.get('comorbidities') or booking.comorbidities
    db.session.commit()
    return jsonify({'msg': 'Surgery booking updated'})

@bp.route('/<int:booking_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_surgery_booking(booking_id):
    booking = SurgeryBooking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    return jsonify({'msg': 'Surgery booking deleted'})
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, SurgeryBooking, User

bp = Blueprint('surgery_booking', __name__, url_prefix='/api/surgery-bookings')

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
def get_surgery_bookings():
    bookings = SurgeryBooking.query.all()
    return jsonify([
        {
            'id': b.id,
            'patient_id': b.patient_id,
            'surgery_type': b.surgery_type,
            'date_booked': b.date_booked.isoformat() if b.date_booked else None,
            'scheduled_date': b.scheduled_date.isoformat() if b.scheduled_date else None,
            'clinical_images': b.clinical_images,
            'admission_type': b.admission_type,
            'ward': b.ward,
            'indications': b.indications,
            'requirements': b.requirements,
            'anaesthesia_type': b.anaesthesia_type,
            'position': b.position,
            'estimated_duration': b.estimated_duration,
            'comorbidities': b.comorbidities
        } for b in bookings
    ])

@bp.route('/', methods=['POST'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def create_surgery_booking():
    data = request.get_json()
    booking = SurgeryBooking(
        patient_id=data.get('patient_id'),
        surgery_type=data.get('surgery_type'),
        date_booked=data.get('date_booked'),
        scheduled_date=data.get('scheduled_date'),
        clinical_images=','.join(data.get('clinical_images', [])) if isinstance(data.get('clinical_images'), list) else data.get('clinical_images'),
        admission_type=data.get('admission_type'),
        ward=data.get('ward'),
        indications=data.get('indications'),
        requirements=','.join(data.get('requirements', [])) if isinstance(data.get('requirements'), list) else data.get('requirements'),
        anaesthesia_type=data.get('anaesthesia_type'),
        position=data.get('position'),
        estimated_duration=data.get('estimated_duration'),
        comorbidities=','.join(data.get('comorbidities', [])) if isinstance(data.get('comorbidities'), list) else data.get('comorbidities')
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({'msg': 'Surgery booking created', 'id': booking.id}), 201

@bp.route('/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_surgery_booking(booking_id):
    booking = SurgeryBooking.query.get_or_404(booking_id)
    return jsonify({
        'id': booking.id,
        'patient_id': booking.patient_id,
        'surgery_type': booking.surgery_type,
        'date_booked': booking.date_booked.isoformat() if booking.date_booked else None,
        'scheduled_date': booking.scheduled_date.isoformat() if booking.scheduled_date else None,
        'clinical_images': booking.clinical_images,
        'admission_type': booking.admission_type,
        'ward': booking.ward,
        'indications': booking.indications,
        'requirements': booking.requirements,
        'anaesthesia_type': booking.anaesthesia_type,
        'position': booking.position,
        'estimated_duration': booking.estimated_duration,
        'comorbidities': booking.comorbidities
    })

@bp.route('/<int:booking_id>', methods=['PUT'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def update_surgery_booking(booking_id):
    booking = SurgeryBooking.query.get_or_404(booking_id)
    data = request.get_json()
    booking.surgery_type = data.get('surgery_type', booking.surgery_type)
    booking.date_booked = data.get('date_booked', booking.date_booked)
    booking.scheduled_date = data.get('scheduled_date', booking.scheduled_date)
    booking.clinical_images = ','.join(data.get('clinical_images', booking.clinical_images.split(','))) if isinstance(data.get('clinical_images'), list) else data.get('clinical_images') or booking.clinical_images
    booking.admission_type = data.get('admission_type', booking.admission_type)
    booking.ward = data.get('ward', booking.ward)
    booking.indications = data.get('indications', booking.indications)
    booking.requirements = ','.join(data.get('requirements', booking.requirements.split(','))) if isinstance(data.get('requirements'), list) else data.get('requirements') or booking.requirements
    booking.anaesthesia_type = data.get('anaesthesia_type', booking.anaesthesia_type)
    booking.position = data.get('position', booking.position)
    booking.estimated_duration = data.get('estimated_duration', booking.estimated_duration)
    booking.comorbidities = ','.join(data.get('comorbidities', booking.comorbidities.split(','))) if isinstance(data.get('comorbidities'), list) else data.get('comorbidities') or booking.comorbidities
    db.session.commit()
    return jsonify({'msg': 'Surgery booking updated'})

@bp.route('/<int:booking_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_surgery_booking(booking_id):
    booking = SurgeryBooking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    return jsonify({'msg': 'Surgery booking deleted'})
