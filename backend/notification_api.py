from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Notification, User

bp = Blueprint('notification_api', __name__, url_prefix='/api/notifications')

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
def get_notifications():
    notifications = Notification.query.all()
    return jsonify([{
        'id': n.id,
        'user_id': n.user_id,
        'message': n.message,
        'is_read': n.is_read,
        'created_at': n.created_at.isoformat() if n.created_at else None
    } for n in notifications])

@bp.route('/', methods=['POST'])
@role_required(['admin'])
def create_notification():
    data = request.get_json()
    notification = Notification(
        user_id=data.get('user_id'),
        message=data.get('message'),
        is_read=data.get('is_read', False),
        created_at=data.get('created_at')
    )
    db.session.add(notification)
    db.session.commit()
    return jsonify({'msg': 'Notification created', 'id': notification.id}), 201

@bp.route('/<int:notification_id>', methods=['GET'])
@jwt_required()
def get_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    return jsonify({
        'id': notification.id,
        'user_id': notification.user_id,
        'message': notification.message,
        'is_read': notification.is_read,
        'created_at': notification.created_at.isoformat() if notification.created_at else None
    })

@bp.route('/<int:notification_id>', methods=['PUT'])
@role_required(['admin'])
def update_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    data = request.get_json()
    notification.message = data.get('message', notification.message)
    notification.is_read = data.get('is_read', notification.is_read)
    notification.created_at = data.get('created_at', notification.created_at)
    db.session.commit()
    return jsonify({'msg': 'Notification updated'})

@bp.route('/<int:notification_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    db.session.delete(notification)
    db.session.commit()
    return jsonify({'msg': 'Notification deleted'})
