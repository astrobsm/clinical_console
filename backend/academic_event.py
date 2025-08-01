from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, AcademicEvent, User

bp = Blueprint('academic_event', __name__, url_prefix='/api/academic-events')

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
def get_academic_events():
    events = AcademicEvent.query.all()
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'event_date': e.event_date.isoformat() if e.event_date else None,
        'created_at': e.created_at.isoformat() if e.created_at else None,
        'topics': e.topics.split(',') if e.topics else [],
        'moderator_id': e.moderator_id,
        'presenter_id': e.presenter_id,
        'meet_link': e.meet_link,
        'auto_generated': e.auto_generated
    } for e in events])

@bp.route('/', methods=['POST'])
@role_required(['admin'])
def create_academic_event():
    data = request.get_json()
    event = AcademicEvent(
        title=data.get('title'),
        description=data.get('description'),
        event_date=data.get('event_date'),
        created_at=data.get('created_at'),
        topics=','.join(data.get('topics', [])),
        moderator_id=data.get('moderator_id'),
        presenter_id=data.get('presenter_id'),
        meet_link=data.get('meet_link'),
        auto_generated=data.get('auto_generated', False)
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'msg': 'Academic event created', 'id': event.id}), 201

@bp.route('/<int:event_id>', methods=['GET'])
@jwt_required()
def get_academic_event(event_id):
    event = AcademicEvent.query.get_or_404(event_id)
    return jsonify({
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'event_date': event.event_date.isoformat() if event.event_date else None,
        'created_at': event.created_at.isoformat() if event.created_at else None,
        'topics': event.topics.split(',') if event.topics else [],
        'moderator_id': event.moderator_id,
        'presenter_id': event.presenter_id,
        'meet_link': event.meet_link,
        'auto_generated': event.auto_generated
    })

@bp.route('/<int:event_id>', methods=['PUT'])
@role_required(['admin'])
def update_academic_event(event_id):
    event = AcademicEvent.query.get_or_404(event_id)
    data = request.get_json()
    event.title = data.get('title', event.title)
    event.description = data.get('description', event.description)
    event.event_date = data.get('event_date', event.event_date)
    event.created_at = data.get('created_at', event.created_at)
    event.topics = ','.join(data.get('topics', event.topics.split(','))) if isinstance(data.get('topics'), list) else data.get('topics') or event.topics
    event.moderator_id = data.get('moderator_id', event.moderator_id)
    event.presenter_id = data.get('presenter_id', event.presenter_id)
    event.meet_link = data.get('meet_link', event.meet_link)
    event.auto_generated = data.get('auto_generated', event.auto_generated)

@bp.route('/auto-generate', methods=['POST'])
@role_required(['admin'])
def auto_generate_academic_events():
    data = request.get_json()
    topics = data.get('topics', [])
    meet_link = data.get('meet_link', 'https://meet.google.com/ojm-qqae-wfo')
    now = datetime.datetime.now()
    days_ahead = (3 - now.weekday() + 7) % 7  # 3 = Thursday
    if days_ahead == 0:
        days_ahead = 7
    next_thursday = now + datetime.timedelta(days=days_ahead)
    events = []
    consultants = User.query.filter_by(role='consultant', is_active=True).all()
    registrars = User.query.filter(User.role.in_(['registrar', 'senior_registrar']), User.is_active==True).all()
    for i, topic in enumerate(topics):
        event_date = next_thursday + datetime.timedelta(weeks=i)
        moderator = consultants[i % len(consultants)] if consultants else None
        presenter = registrars[i % len(registrars)] if registrars else None
        event = AcademicEvent(
            title=f"Burns & Plastic Surgery Clinical Meeting",
            description=f"Weekly clinical meeting on {topic}",
            event_date=event_date.replace(hour=19, minute=0, second=0, microsecond=0),
            topics=topic,
            moderator_id=moderator.id if moderator else None,
            presenter_id=presenter.id if presenter else None,
            meet_link=meet_link,
            auto_generated=True
        )
        db.session.add(event)
        events.append(event)
    db.session.commit()
    for event in events:
        if event.moderator_id:
            send_notification(event.moderator_id, f"You have been assigned as moderator for '{event.title}' on {event.event_date.strftime('%A, %B %d, %Y at %I:%M %p')} (Google Meet: {event.meet_link})")
        if event.presenter_id:
            send_notification(event.presenter_id, f"You have been assigned as presenter for '{event.title}' on {event.event_date.strftime('%A, %B %d, %Y at %I:%M %p')} (Google Meet: {event.meet_link})")
    return jsonify({'msg': f'{len(events)} academic events auto-generated', 'event_ids': [e.id for e in events]}), 201

@bp.route('/<int:event_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_academic_event(event_id):
    event = AcademicEvent.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'msg': 'Academic event deleted'})
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, AcademicEvent, User

bp = Blueprint('academic_event', __name__, url_prefix='/api/academic-events')

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
def get_academic_events():
    events = AcademicEvent.query.all()
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'event_date': e.event_date.isoformat() if e.event_date else None,
        'created_at': e.created_at.isoformat() if e.created_at else None,
        'topics': e.topics.split(',') if e.topics else [],
        'moderator_id': e.moderator_id,
        'presenter_id': e.presenter_id,
        'meet_link': e.meet_link,
        'auto_generated': e.auto_generated
    } for e in events])

@bp.route('/', methods=['POST'])
@role_required(['admin'])
def create_academic_event():
    data = request.get_json()
    event = AcademicEvent(
        title=data.get('title'),
        description=data.get('description'),
        event_date=data.get('event_date'),
        created_at=data.get('created_at'),
        topics=','.join(data.get('topics', [])),
        moderator_id=data.get('moderator_id'),
        presenter_id=data.get('presenter_id'),
        meet_link=data.get('meet_link'),
        auto_generated=data.get('auto_generated', False)
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'msg': 'Academic event created', 'id': event.id}), 201

@bp.route('/<int:event_id>', methods=['GET'])
@jwt_required()
def get_academic_event(event_id):
    event = AcademicEvent.query.get_or_404(event_id)
    return jsonify({
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'event_date': event.event_date.isoformat() if event.event_date else None,
        'created_at': event.created_at.isoformat() if event.created_at else None,
        'topics': event.topics.split(',') if event.topics else [],
        'moderator_id': event.moderator_id,
        'presenter_id': event.presenter_id,
        'meet_link': event.meet_link,
        'auto_generated': event.auto_generated
    })

@bp.route('/<int:event_id>', methods=['PUT'])
@role_required(['admin'])
def update_academic_event(event_id):
    event = AcademicEvent.query.get_or_404(event_id)
    data = request.get_json()
    event.title = data.get('title', event.title)
    event.description = data.get('description', event.description)
    event.event_date = data.get('event_date', event.event_date)
    event.created_at = data.get('created_at', event.created_at)
    event.topics = ','.join(data.get('topics', event.topics.split(','))) if isinstance(data.get('topics'), list) else data.get('topics') or event.topics
    event.moderator_id = data.get('moderator_id', event.moderator_id)
    event.presenter_id = data.get('presenter_id', event.presenter_id)
    event.meet_link = data.get('meet_link', event.meet_link)
    event.auto_generated = data.get('auto_generated', event.auto_generated)
# Auto-generate academic events for upcoming Thursdays, assign moderator/presenter, and set Google Meet link
import datetime
from backend.notifications import send_notification
@bp.route('/auto-generate', methods=['POST'])
@role_required(['admin'])
def auto_generate_academic_events():
    data = request.get_json()
    topics = data.get('topics', [])
    meet_link = data.get('meet_link', 'https://meet.google.com/ojm-qqae-wfo')
    now = datetime.datetime.now()
    # Find next Thursday
    days_ahead = (3 - now.weekday() + 7) % 7  # 3 = Thursday
    if days_ahead == 0:
        days_ahead = 7
    next_thursday = now + datetime.timedelta(days=days_ahead)
    events = []
    # Fetch all consultants and registrars
    consultants = User.query.filter_by(role='consultant', is_active=True).all()
    registrars = User.query.filter(User.role.in_(['registrar', 'senior_registrar']), User.is_active==True).all()
    for i, topic in enumerate(topics):
        event_date = next_thursday + datetime.timedelta(weeks=i)
        moderator = consultants[i % len(consultants)] if consultants else None
        presenter = registrars[i % len(registrars)] if registrars else None
        event = AcademicEvent(
            title=f"Burns & Plastic Surgery Clinical Meeting",
            description=f"Weekly clinical meeting on {topic}",
            event_date=event_date.replace(hour=19, minute=0, second=0, microsecond=0),
            topics=topic,
            moderator_id=moderator.id if moderator else None,
            presenter_id=presenter.id if presenter else None,
            meet_link=meet_link,
            auto_generated=True
        )
        db.session.add(event)
        events.append(event)
    db.session.commit()
    # Send notifications to moderator and presenter for each event
    for event in events:
        if event.moderator_id:
            send_notification(event.moderator_id, f"You have been assigned as moderator for '{event.title}' on {event.event_date.strftime('%A, %B %d, %Y at %I:%M %p')} (Google Meet: {event.meet_link})")
        if event.presenter_id:
            send_notification(event.presenter_id, f"You have been assigned as presenter for '{event.title}' on {event.event_date.strftime('%A, %B %d, %Y at %I:%M %p')} (Google Meet: {event.meet_link})")
    return jsonify({'msg': f'{len(events)} academic events auto-generated', 'event_ids': [e.id for e in events]}), 201

@bp.route('/<int:event_id>', methods=['DELETE'])
@role_required(['admin'])
def delete_academic_event(event_id):
    event = AcademicEvent.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'msg': 'Academic event deleted'})
