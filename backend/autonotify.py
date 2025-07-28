from datetime import datetime, timedelta
from models import db, Notification, Assessment, User

def send_assessment_alerts():
    now = datetime.utcnow()
    next_monday = now + timedelta((7 - now.weekday()) % 7)
    test_time = next_monday.replace(hour=9, minute=0, second=0, microsecond=0)
    # Find assessments scheduled for next Monday 9am
    assessments = Assessment.query.filter(
        Assessment.scheduled_date >= test_time - timedelta(hours=24),
        Assessment.scheduled_date < test_time
    ).all()
    for a in assessments:
        user = User.query.get(a.user_id)
        if user:
            n = Notification(user_id=user.id, message=f"You have a CBT assessment scheduled for {a.scheduled_date.strftime('%Y-%m-%d %H:%M')}")
            db.session.add(n)
    db.session.commit()
