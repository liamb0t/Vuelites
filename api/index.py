import os
import sys
from flask import send_from_directory

# Add the backend directory to Python path for API imports
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.append(backend_path)

# Point Flask to Nuxt's build directory
dist_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")

# Import your existing Flask app
from flask_api.main.routes import app

# Update the static folder to serve Nuxt files
app.static_folder = dist_dir
app.static_url_path = ""

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