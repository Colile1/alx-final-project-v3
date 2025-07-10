# Authentication routes blueprint
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import User, db
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    username = data['username'].strip()
    password = data['password']
    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, created_at=datetime.utcnow())
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    username = data['username'].strip()
    password = data['password']
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        login_user(user, remember=True)
        user.last_login = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': 'Logged in', 'user_id': user.id, 'username': user.username, 'last_active_garden_id': user.last_active_garden_id}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/status', methods=['GET'])
def status():
    if current_user.is_authenticated:
        return jsonify({'isAuthenticated': True, 'userId': current_user.id, 'username': current_user.username, 'last_active_garden_id': current_user.last_active_garden_id}), 200
    return jsonify({'isAuthenticated': False}), 200

@auth_bp.route('/profile', methods=['GET', 'PUT'])
@login_required
def profile():
    if request.method == 'GET':
        return jsonify({
            'id': current_user.id,
            'username': current_user.username,
            'created_at': current_user.created_at.isoformat() if current_user.created_at else None,
            'last_login': current_user.last_login.isoformat() if current_user.last_login else None,
            'last_active_garden_id': current_user.last_active_garden_id,
            'preferences': {
                'simulation_frequency': current_user.simulation_frequency,
                'moisture_threshold': current_user.moisture_threshold,
                'temperature_min': current_user.temperature_min,
                'temperature_max': current_user.temperature_max,
                'light_min': current_user.light_min
            }
        }), 200
    elif request.method == 'PUT':
        data = request.get_json()
        # Allow updating preferences only
        prefs = data.get('preferences', {})
        if 'simulation_frequency' in prefs:
            current_user.simulation_frequency = int(prefs['simulation_frequency'])
        if 'moisture_threshold' in prefs:
            current_user.moisture_threshold = int(prefs['moisture_threshold'])
        if 'temperature_min' in prefs:
            current_user.temperature_min = float(prefs['temperature_min'])
        if 'temperature_max' in prefs:
            current_user.temperature_max = float(prefs['temperature_max'])
        if 'light_min' in prefs:
            current_user.light_min = int(prefs['light_min'])
        db.session.commit()
        return jsonify({'message': 'Profile updated'}), 200
