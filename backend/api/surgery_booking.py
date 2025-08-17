from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, SurgeryBooking, User
from datetime import datetime

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
    try:
        bookings = SurgeryBooking.query.all()
        return jsonify([
            {
                'id': b.id,
                'patient_id': b.patient_id,
                'surgery_type': b.surgery_type,
                'date': b.date.isoformat() if b.date else None,
                'purpose': b.purpose
            } for b in bookings
        ])
    except Exception as e:
        return jsonify({'msg': f'Error fetching surgery bookings: {str(e)}'}), 500

@bp.route('/', methods=['POST'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def create_surgery_booking():
    try:
        data = request.get_json()
        booking = SurgeryBooking(
            patient_id=data.get('patient_id'),
            surgery_type=data.get('surgery_type'),
            date=datetime.fromisoformat(data.get('date')) if data.get('date') else None,
            purpose=data.get('purpose')
        )
        db.session.add(booking)
        db.session.commit()
        return jsonify({'msg': 'Surgery booking created', 'id': booking.id}), 201
    except Exception as e:
        return jsonify({'msg': f'Error creating surgery booking: {str(e)}'}), 500

@bp.route('/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_surgery_booking(booking_id):
    try:
        booking = SurgeryBooking.query.get_or_404(booking_id)
        return jsonify({
            'id': booking.id,
            'patient_id': booking.patient_id,
            'surgery_type': booking.surgery_type,
            'date': booking.date.isoformat() if booking.date else None,
            'purpose': booking.purpose
        })
    except Exception as e:
        return jsonify({'msg': f'Error fetching surgery booking: {str(e)}'}), 500

@bp.route('/<int:booking_id>', methods=['PUT'])
@role_required(['consultant', 'senior_registrar', 'admin'])
def update_surgery_booking(booking_id):
    try:
        booking = SurgeryBooking.query.get_or_404(booking_id)
        data = request.get_json()
        
        if 'surgery_type' in data:
            booking.surgery_type = data['surgery_type']
        if 'date' in data:
            booking.date = datetime.fromisoformat(data['date']) if data['date'] else booking.date
        if 'purpose' in data:
            booking.purpose = data['purpose']
            
        db.session.commit()
        return jsonify({'msg': 'Surgery booking updated'})
    except Exception as e:
        return jsonify({'msg': f'Error updating surgery booking: {str(e)}'}), 500

@bp.route('/<int:booking_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_surgery_booking(booking_id):
    try:
        booking = SurgeryBooking.query.get_or_404(booking_id)
        db.session.delete(booking)
        db.session.commit()
        return jsonify({'msg': 'Surgery booking deleted'})
    except Exception as e:
        return jsonify({'msg': f'Error deleting surgery booking: {str(e)}'}), 500

@bp.route('/patient/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient_surgery_bookings(patient_id):
    try:
        bookings = SurgeryBooking.query.filter_by(patient_id=patient_id).all()
        return jsonify([
            {
                'id': b.id,
                'patient_id': b.patient_id,
                'surgery_type': b.surgery_type,
                'date': b.date.isoformat() if b.date else None,
                'purpose': b.purpose
            } for b in bookings
        ])
    except Exception as e:
        return jsonify({'msg': f'Error fetching patient surgery bookings: {str(e)}'}), 500
