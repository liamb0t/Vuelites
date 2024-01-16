import os
from flask import Flask
from flask_cors import CORS
import praw

app = Flask(__name__)
CORS(app, origins=['https://soccer-highlights-frontend.onrender.com'])
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

### setting up the Reddit Instance

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

id = os.environ.get('ID')
client_secret = os.environ.get('CLIENT_SECRET')
user_agent = os.environ.get('USER_AGENT')
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

reddit = praw.Reddit(
    client_id=id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password
)

### register routes

from flask_api.main.routes import main

app.register_blueprint(main)