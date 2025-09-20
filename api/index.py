import os
import sys

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.append(backend_path)

# Ensure the working directory is set correctly for template finding
os.chdir(os.path.join(backend_path, 'flask_api', 'main'))

from flask_api import app

# This is the entry point for Vercel
app = app