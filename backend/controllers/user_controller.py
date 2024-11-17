from flask import Blueprint, jsonify, request, abort
from models.user import User, db
import jwt
from functools import wraps
from datetime import datetime, timedelta
from services.user_service import UserService

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    try:
        new_user = UserService.register_user(data['username'], data['email'], data['password'])
        return jsonify({'message': 'User created successfully'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@user_bp.route('/api/login', methods=['POST'])
def login():
    """Authenticate a user and return a token."""
    data = request.get_json()
    try:
        token = UserService.authenticate_user(data['username'], data['password'])
        return jsonify({'token': token}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

def token_required(f):
    """Decorator to enforce token authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, 'your-secret-key', algorithms=['HS256'])
            current_user = User.query.get(data['id'])
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

@user_bp.route('/api/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        abort(400, 'Invalid request data')

    if User.query.filter_by(username=data['username']).first():
        abort(400, 'Username already exists')

    if User.query.filter_by(email=data['email']).first():
        abort(400, 'Email already exists')

    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@user_bp.route('/api/login', methods=['POST'])
def login():
    """Authenticate a user and return a token."""
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        abort(400, 'Invalid request data')

    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        abort(401, 'Invalid username or password')

    token = user.generate_auth_token()
    return jsonify({'token': token}), 200

@user_bp.route('/api/users/me', methods=['GET'])
@token_required
def get_user_info(current_user):
    """Get current user's information."""
    return jsonify({
        'username': current_user.username,
        'email': current_user.email,
        'id': current_user.id
    }), 200

@user_bp.route('/api/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id, current_user):
    """Get user information by user ID (admin only)."""
    if current_user.id != user_id:
        abort(403, 'Access forbidden: You can only access your own information.')

    user = User.query.get(user_id)
    if user is None:
        abort(404, 'User not found')

    return jsonify({
        'username': user.username,
        'email': user.email,
        'id': user.id
    }), 200

@user_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id, current_user):
    """Update user information."""
    if current_user.id != user_id:
        abort(403, 'Access forbidden: You can only update your own information.')

    user = User.query.get(user_id)
    if user is None:
        abort(404, 'User not found')

    data = request.get_json()
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()
    return jsonify({'message': 'User information updated successfully.'}), 200

@user_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id, current_user):
    """Delete a user by user ID."""
    if current_user.id != user_id:
        abort(403, 'Access forbidden: You can only delete your own account.')

    user = User.query.get(user_id)
    if user is None:
        abort(404, 'User not found')

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully.'}), 200
