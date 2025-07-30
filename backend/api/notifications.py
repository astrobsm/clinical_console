from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, Notification
from datetime import datetime

def send_notification(user_id, message):
    """Create and commit a notification for a user."""
    n = Notification(user_id=user_id, message=message, is_read=False, created_at=datetime.utcnow())
    db.session.add(n)
    db.session.commit()
    return n.id

bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')

@bp.route('/', methods=['GET'])
@jwt_required()
def list_notifications():
    user_id = str(get_jwt_identity())
    notifications = Notification.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            'id': n.id,
            'message': n.message,
            'is_read': n.is_read,
            'created_at': n.created_at.isoformat() if n.created_at else None
        } for n in notifications
    ])

@bp.route('/<int:notification_id>/read', methods=['POST'])
@jwt_required()
def mark_read(notification_id):
    user_id = str(get_jwt_identity())
    notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first_or_404()
    notification.is_read = True
    db.session.commit()
    return jsonify({'msg': 'Notification marked as read'})

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, Notification
from datetime import datetime

def send_notification(user_id, message):
    """Create and commit a notification for a user."""
    n = Notification(user_id=user_id, message=message, is_read=False, created_at=datetime.utcnow())
    db.session.add(n)
    db.session.commit()
    return n.id

bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')

@bp.route('/', methods=['GET'])
@jwt_required()
def list_notifications():
    user_id = str(get_jwt_identity())
    notifications = Notification.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            'id': n.id,
            'message': n.message,
            'is_read': n.is_read,
            'created_at': n.created_at.isoformat() if n.created_at else None
        } for n in notifications
    ])

@bp.route('/<int:notification_id>/read', methods=['POST'])
@jwt_required()
def mark_read(notification_id):
    user_id = str(get_jwt_identity())
    notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first_or_404()
    notification.is_read = True
    db.session.commit()
    return jsonify({'msg': 'Notification marked as read'})
