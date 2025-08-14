
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash
from backend.models import db, User

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Fetch users by role for frontend staff assignment
@bp.route('/users', methods=['GET'])
@jwt_required()
def get_users_by_role():
    role = request.args.get('role')
    if not role:
        return jsonify({'msg': 'Role is required'}), 400
    users = User.query.filter_by(role=role, is_active=True).all()
    return jsonify([
        {'id': u.id, 'name': u.name, 'email': u.email, 'role': u.role}
        for u in users
    ])


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    if not all([name, email, password, role]):
        return jsonify({'msg': 'All fields required'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'Email already registered'}), 409
    hashed_password = generate_password_hash(password)
    user = User(name=name, email=email, password=hashed_password, role=role)
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'User registered successfully'}), 201


@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'msg': 'No JSON data provided'}), 400
            
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({'msg': 'Email and password required'}), 400
            
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({'msg': 'Invalid credentials'}), 401
            
        access_token = create_access_token(identity=str(user.id), additional_claims={
            'role': user.role,
            'name': user.name,
            'email': user.email
        })
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role
            }
        })
    except Exception as e:
        # Log the error and return a generic message
        print(f"Login error: {str(e)}")
        return jsonify({'msg': 'Internal server error', 'error': str(e)}), 500
