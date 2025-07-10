# Data import/export and analytics routes blueprint
from flask import Blueprint, request, jsonify, Response
from flask_login import login_required, current_user
from models import Garden, PlantReading, db
from utils.csv_handler import import_readings, export_readings
from utils.analytics import predict_next_watering

data_bp = Blueprint('data', __name__)

@data_bp.route('/gardens/<int:garden_id>/import_data', methods=['POST'])
@login_required
def import_garden_data(garden_id):
    garden = Garden.query.filter_by(id=garden_id, user_id=current_user.id).first()
    if not garden:
        return jsonify({'error': 'Garden not found'}), 404
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files allowed'}), 400
    import_readings(file.stream, current_user.id, garden_id)
    db.session.commit()
    return jsonify({'message': 'Data imported'}), 200

@data_bp.route('/gardens/<int:garden_id>/export_data', methods=['GET'])
@login_required
def export_garden_data(garden_id):
    garden = Garden.query.filter_by(id=garden_id, user_id=current_user.id).first()
    if not garden:
        return jsonify({'error': 'Garden not found'}), 404
    csv_data = export_readings(current_user.id, garden_id)
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={
            'Content-Disposition': f'attachment; filename=garden_{garden_id}_data.csv'
        }
    )

@data_bp.route('/gardens/<int:garden_id>/prediction', methods=['GET'])
@login_required
def get_prediction(garden_id):
    garden = Garden.query.filter_by(id=garden_id, user_id=current_user.id).first()
    if not garden:
        return jsonify({'error': 'Garden not found'}), 404
    prediction = predict_next_watering(garden_id, current_user.id)
    return jsonify({'next_watering_estimate': prediction}), 200
