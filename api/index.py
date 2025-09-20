import os
import sys

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from flask_api import app

# This is the entry point for Vercel
app = app