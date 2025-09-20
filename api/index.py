import os
import sys

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.append(backend_path)

from flask_api import app

# This is the entry point for Vercel
app = app