from flask import current_app
from datetime import datetime

def send_notification(user_id, message):
    """Create and commit a notification for a user."""
    # Import here to avoid circular imports
    from backend.models import db, Notification
    
    notification = Notification(
        user_id=user_id,
        message=message,
        is_read=False,
        created_at=datetime.utcnow()
    )
    db.session.add(notification)
    db.session.commit()
    return notification

def mark_notification_read(notification_id):
    """Mark notification as read."""
    # Import here to avoid circular imports
    from backend.models import db, Notification
    
    notification = Notification.query.get(notification_id)
    if notification:
        notification.is_read = True
        db.session.commit()
    return notification

def get_user_notifications(user_id):
    """Get all notifications for a user."""
    # Import here to avoid circular imports
    from backend.models import Notification
    
    return Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()

def send_email_notification(subject, recipients, body):
    """Send email notification (placeholder - requires Flask-Mail setup)."""
    print(f"Email notification: {subject} to {recipients}")
    print(f"Body: {body}")
    # This would require Flask-Mail configuration
    pass
