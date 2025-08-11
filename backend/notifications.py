from flask import current_app
try:
    from flask_mail import Message
except ImportError:
    Message = None
from threading import Thread
from backend.database import db
from datetime import datetime

# Example: send email notification (requires Flask-Mail setup)
def send_async_email(app, msg):
    with app.app_context():
        mail = current_app.extensions.get('mail')
        if mail:
            mail.send(msg)

def send_email_notification(subject, recipients, body):
    if Message is None:
        print("Flask-Mail not installed, skipping email notification")
        return
    app = current_app._get_current_object()
    msg = Message(subject, recipients=recipients, body=body)
    Thread(target=send_async_email, args=(app, msg)).start()

# In-app notification: create a Notification record in the DB
def send_notification(user_id, message):
    from backend.models import Notification
    notification = Notification(
        user_id=user_id,
        message=message,
        is_read=False,
        created_at=datetime.utcnow()
    )
    db.session.add(notification)
    db.session.commit()
    return notification

# Mark notification as read
def mark_notification_read(notification_id):
    from backend.models import Notification
    notification = Notification.query.get(notification_id)
    if notification:
        notification.is_read = True
        db.session.commit()
    return notification

# Get all notifications for a user
def get_user_notifications(user_id):
    from backend.models import Notification
    return Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
