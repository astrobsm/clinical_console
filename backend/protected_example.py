from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt

bp = Blueprint('protected', __name__, url_prefix='/api/protected')

@bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    claims = get_jwt()
    return jsonify({
        'msg': f"Welcome, {claims.get('name')}!",
        'role': claims.get('role')
    })
