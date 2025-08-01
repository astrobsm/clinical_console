from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app

def notify_users():
    with current_app.app_context():
        # Import inside the function to avoid circular imports
        from backend.models import User
        from backend.notifications import send_notification
        
        users = User.query.filter(User.role.in_(['senior_registrar', 'registrar', 'house_officer'])).all()
        for user in users:
            send_notification(user.id, "CBT test is scheduled for 8am Tuesday. Please be prepared.")

def start_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(notify_users, 'cron', day_of_week='mon', hour=8, minute=0)
    scheduler.start()
    app.scheduler = scheduler
