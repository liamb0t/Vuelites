import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS

# Add the backend directory to Python path for API imports
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.append(backend_path)

# Point Flask to Nuxt's build directory
dist_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")

# Create new Flask app instance that serves Nuxt frontend
app = Flask(__name__, static_folder=dist_dir, static_url_path="")

CORS(app, origins=[
    'http://localhost:3000',
    'https://goalrush-six.vercel.app',
    'https://goalrush-git-main-liam-mclaughlins-projects.vercel.app',
    'https://goalrush-b26xszc68-liam-mclaughlins-projects.vercel.app'
])

# Import and register your existing API routes
from backend.flask_api.main.routes import api

# Register API blueprints
app.register_blueprint(api)

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