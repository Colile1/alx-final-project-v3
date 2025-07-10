# Weather API integration routes blueprint
from flask import Blueprint, request, jsonify
from flask_login import login_required
from utils.weather_api import get_current_weather

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/weather', methods=['GET'])
@login_required
def get_weather():
    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'Location parameter required'}), 400
    try:
        weather_data = get_current_weather(location)
        return jsonify(weather_data), 200
    except Exception as e:
        return jsonify({'error': f'Weather API error: {str(e)}'}), 500
