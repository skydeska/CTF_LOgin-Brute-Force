from flask import Flask, session
from flask_session import Session
import os
from config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object(config[config_name])
    
    # Initialiser les sessions
    Session(app)
    
    # Enregistrer les blueprints
    from blueprints.main import main_bp
    from blueprints.auth import auth_bp
    from blueprints.dashboard import dashboard_bp
    from blueprints.hidden_admin import hidden_admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(hidden_admin_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, host='0.0.0.0', port=5000)