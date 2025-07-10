import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_super_secret_development_key_change_in_production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///plant_care.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
