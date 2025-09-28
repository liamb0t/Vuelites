from flask import Flask
from flask_cors import CORS
from flask_api.main.routes import api

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api)
    
    return app

# Create app instance for imports
app = create_app()