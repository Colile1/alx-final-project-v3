# Flask app factory and blueprint registration
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from dotenv import load_dotenv
import os

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    load_dotenv()
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config.from_object('config.Config')
    db.init_app(app)
    login_manager.init_app(app)
    CORS(app, supports_credentials=True)

    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.gardens import gardens_bp
    from routes.data import data_bp
    from routes.weather import weather_bp
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(gardens_bp, url_prefix='/api')
    app.register_blueprint(data_bp, url_prefix='/api')
    app.register_blueprint(weather_bp, url_prefix='/api')

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
