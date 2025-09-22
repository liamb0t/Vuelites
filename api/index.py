import os
import sys
from aiohttp import request
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

# Serve static assets (_nuxt/, img/, favicon, etc.)
@app.route('/_nuxt/<path:filename>')
def nuxt_assets(filename):
    return send_from_directory(os.path.join(dist_dir, '_nuxt'), filename)

@app.route('/img/<path:filename>')
def img_assets(filename):
    return send_from_directory(os.path.join(dist_dir, 'img'), filename)

@app.route('/favicon.ico')
@app.route('/robots.txt')
def root_files():
    return send_from_directory(dist_dir, request.path.lstrip('/'))

# Catch-all: everything else goes to index.html
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def spa_fallback(path):
    file_path = os.path.join(dist_dir, path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(dist_dir, path)
    return send_from_directory(dist_dir, 'index.html')