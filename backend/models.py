# SQLAlchemy models for User, Garden, PlantReading
from flask_login import UserMixin
from datetime import datetime
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    last_active_garden_id = db.Column(db.Integer, db.ForeignKey('gardens.id'), nullable=True)
    simulation_frequency = db.Column(db.Integer, default=60)
    moisture_threshold = db.Column(db.Integer, default=30)
    temperature_min = db.Column(db.Float, default=15.0)
    temperature_max = db.Column(db.Float, default=30.0)
    light_min = db.Column(db.Integer, default=200)
    gardens = db.relationship('Garden', backref='owner', lazy=True, cascade='all, delete-orphan')

class Garden(db.Model):
    __tablename__ = 'gardens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    location_lat = db.Column(db.Float, nullable=True)
    location_lon = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    sensor_type = db.Column(db.String(50), default='simulated_basic')
    plant_type = db.Column(db.String(100), default='General')
    watering_frequency = db.Column(db.Integer, default=3)
    readings = db.relationship('PlantReading', backref='garden_obj', lazy=True, cascade='all, delete-orphan')

class PlantReading(db.Model):
    __tablename__ = 'plant_readings'
    id = db.Column(db.Integer, primary_key=True)
    garden_id = db.Column(db.Integer, db.ForeignKey('gardens.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    moisture_level = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    light_intensity = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=True)
    ph_level = db.Column(db.Float, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    is_manual = db.Column(db.Boolean, default=False)
