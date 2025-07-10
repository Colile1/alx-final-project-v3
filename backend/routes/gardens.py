# Garden management routes blueprint
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import Garden, PlantReading, db
from datetime import datetime

gardens_bp = Blueprint('gardens', __name__)

@gardens_bp.route('/gardens', methods=['GET'])
@login_required
def get_gardens():
    gardens = Garden.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': g.id,
        'name': g.name,
        'location': g.location,
        'location_lat': g.location_lat,
        'location_lon': g.location_lon,
        'created_at': g.created_at.isoformat() if g.created_at else None,
        'last_accessed': g.last_accessed.isoformat() if g.last_accessed else None,
        'sensor_type': g.sensor_type,
        'plant_type': g.plant_type,
        'watering_frequency': g.watering_frequency
    } for g in gardens]), 200

@gardens_bp.route('/gardens', methods=['POST'])
@login_required
def add_garden():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Garden name required'}), 400
    new_garden = Garden(
        user_id=current_user.id,
        name=data['name'].strip(),
        location=data.get('location', '').strip(),
        location_lat=data.get('location_lat'),
        location_lon=data.get('location_lon'),
        sensor_type=data.get('sensor_type', 'simulated_basic'),
        plant_type=data.get('plant_type', 'General'),
        watering_frequency=data.get('watering_frequency', 3),
        created_at=datetime.utcnow(),
        last_accessed=datetime.utcnow()
    )
    db.session.add(new_garden)
    db.session.commit()
    return jsonify({'message': 'Garden added', 'garden_id': new_garden.id}), 201

@gardens_bp.route('/gardens/<int:garden_id>', methods=['GET'])
@login_required
def get_garden(garden_id):
    garden = Garden.query.filter_by(id=garden_id, user_id=current_user.id).first()
    if not garden:
        return jsonify({'error': 'Garden not found'}), 404
    garden.last_accessed = datetime.utcnow()
    db.session.commit()
    return jsonify({
        'id': garden.id,
        'name': garden.name,
        'location': garden.location,
        'location_lat': garden.location_lat,
        'location_lon': garden.location_lon,
        'created_at': garden.created_at.isoformat() if garden.created_at else None,
        'last_accessed': garden.last_accessed.isoformat() if garden.last_accessed else None,
        'sensor_type': garden.sensor_type,
        'plant_type': garden.plant_type,
        'watering_frequency': garden.watering_frequency
    }), 200

@gardens_bp.route('/gardens/<int:garden_id>', methods=['PUT'])
@login_required
def update_garden(garden_id):
    garden = Garden.query.filter_by(id=garden_id, user_id=current_user.id).first()
    if not garden:
        return jsonify({'error': 'Garden not found'}), 404
    data = request.get_json()
    if 'name' in data:
        garden.name = data['name']
    if 'location' in data:
        garden.location = data['location']
    if 'location_lat' in data:
        garden.location_lat = data['location_lat']
    if 'location_lon' in data:
        garden.location_lon = data['location_lon']
    if 'sensor_type' in data:
        garden.sensor_type = data['sensor_type']
    if 'plant_type' in data:
        garden.plant_type = data['plant_type']
    if 'watering_frequency' in data:
        garden.watering_frequency = data['watering_frequency']
    garden.last_accessed = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Garden updated'}), 200

@gardens_bp.route('/gardens/<int:garden_id>', methods=['DELETE'])
@login_required
def delete_garden(garden_id):
    garden = Garden.query.filter_by(id=garden_id, user_id=current_user.id).first()
    if not garden:
        return jsonify({'error': 'Garden not found'}), 404
    db.session.delete(garden)
    db.session.commit()
    return jsonify({'message': 'Garden deleted'}), 200

@gardens_bp.route('/gardens/<int:garden_id>/readings', methods=['GET'])
@login_required
def get_garden_readings(garden_id):
    garden = Garden.query.filter_by(id=garden_id, user_id=current_user.id).first()
    if not garden:
        return jsonify({'error': 'Garden not found'}), 404
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 100, type=int)
    readings = PlantReading.query.filter_by(garden_id=garden_id).order_by(PlantReading.timestamp.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify([
        {
            'id': r.id,
            'timestamp': r.timestamp.isoformat() if r.timestamp else None,
            'moisture_level': r.moisture_level,
            'temperature': r.temperature,
            'light_intensity': r.light_intensity,
            'humidity': r.humidity,
            'ph_level': r.ph_level,
            'notes': r.notes,
            'is_manual': r.is_manual
        } for r in readings.items
    ]), 200

@gardens_bp.route('/gardens/<int:garden_id>/readings', methods=['POST'])
@login_required
def add_reading(garden_id):
    garden = Garden.query.filter_by(id=garden_id, user_id=current_user.id).first()
    if not garden:
        return jsonify({'error': 'Garden not found'}), 404
    data = request.get_json()
    required_fields = ['moisture_level', 'temperature', 'light_intensity']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    new_reading = PlantReading(
        garden_id=garden_id,
        moisture_level=float(data['moisture_level']),
        temperature=float(data['temperature']),
        light_intensity=float(data['light_intensity']),
        humidity=float(data.get('humidity')) if data.get('humidity') is not None else None,
        ph_level=float(data.get('ph_level')) if data.get('ph_level') is not None else None,
        notes=data.get('notes', '').strip(),
        is_manual=data.get('is_manual', True),
        timestamp=datetime.utcnow()
    )
    db.session.add(new_reading)
    garden.last_accessed = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Reading added', 'reading_id': new_reading.id}), 201

@gardens_bp.route('/gardens/<int:garden_id>/pair_sensor', methods=['POST'])
@login_required
def pair_sensor(garden_id):
    garden = Garden.query.filter_by(id=garden_id, user_id=current_user.id).first()
    if not garden:
        return jsonify({'error': 'Garden not found'}), 404
    sensor_type = request.json.get('sensor_type')
    garden.sensor_type = sensor_type
    db.session.commit()
    return jsonify({'message': f'Sensor type {sensor_type} paired with garden {garden_id}'}), 200

@gardens_bp.route('/gardens/<int:garden_id>/unpair_sensor', methods=['DELETE'])
@login_required
def unpair_sensor(garden_id):
    garden = Garden.query.filter_by(id=garden_id, user_id=current_user.id).first()
    if not garden:
        return jsonify({'error': 'Garden not found'}), 404
    garden.sensor_type = 'none'
    db.session.commit()
    return jsonify({'message': f'Sensor unpaired from garden {garden_id}'}), 200

@gardens_bp.route('/gardens/<int:garden_id>/sensors', methods=['GET'])
@login_required
def list_sensors(garden_id):
    garden = Garden.query.filter_by(id=garden_id, user_id=current_user.id).first()
    if not garden:
        return jsonify({'error': 'Garden not found'}), 404
    return jsonify({'garden_id': garden.id, 'sensor_type': garden.sensor_type}), 200
