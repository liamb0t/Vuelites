import os
from flask import Flask
from flask_cors import CORS
import praw
import redis
import pymongo
from pymongo import MongoClient
from urllib.parse import quote_plus

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

### setting up the Reddit Instance

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

id = 'ougRB1VYJVa8kH9XyphsnA'
client_secret = 'RUTKKzZFxArP328gG2emXZgRhiZHLw'
user_agent = '<console:SopranosBot:1.0 (by u/AlbertBareseBarese)>'
username = 'AlbertBareseBarese'
password = '8Stevieg8@'

reddit = praw.Reddit(
    client_id=id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password
)

r = redis.Redis(
    host='redis-17054.c82.us-east-1-2.ec2.redns.redis-cloud.com',
    port=17054,
    decode_responses=True,
    username="default",
    password="YIPMUZin37cqMlrmjl3x2HuynaWFz5aY",
)

### setting up MongoDB Connection
try:
    # Use the MongoDB URI from the Nuxt frontend or default to local MongoDB
    mdb_password = 'keHxN5YJ3YXjnVdu'
    uri = f"mongodb+srv://liammcl33:{mdb_password}@cluster0.kh4xxy0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    mongo_client = MongoClient(uri)
    
    # Connect to the goalrush database
    db = mongo_client.goalrush
    
    # Collections for our caching system
    search_results_collection = db.search_results
    search_cache_collection = db.search_cache
    
    print("MongoDB connected successfully")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    mongo_client = None
    db = None
    search_results_collection = None
    search_cache_collection = None

### register routes

from flask_api.main.routes import main
from flask_api.main.routes import client_bp

app.register_blueprint(main, url_prefix='/api')
app.register_blueprint(client_bp)