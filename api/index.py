import os
import sys
from flask import Flask, send_from_directory

# Add the backend directory to Python path for API imports
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.append(backend_path)

# Point Flask to Nuxt's build directory
dist_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")

# Create new Flask app instance that serves Nuxt frontend
app = Flask(__name__, static_folder=dist_dir, static_url_path="")

# Import and register your existing API routes
from flask_api.main.routes import main
from flask_api import app as original_app

# Copy configuration from original app
app.config.update(original_app.config)

# Register API blueprints
app.register_blueprint(main, url_prefix='/api')

# Root: serve Nuxt index.html
@app.route("/")
def index():
    return send_from_directory(dist_dir, "index.html")

# Catch-all: either return static files or fallback to index.html for SPA routing
@app.route("/<path:path>")
def serve_file(path):
    file_path = os.path.join(dist_dir, path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(dist_dir, path)
    # Fallback to index.html for SPA routing
    return send_from_directory(dist_dir, "index.html")