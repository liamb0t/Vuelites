import os
import praw
import redis
import pymongo
from pymongo import MongoClient

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Load from project root (go up to vuelites directory)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
    env_path = os.path.join(project_root, '.env')
    load_dotenv(env_path)
    print(f"Loading .env from: {env_path}")
except ImportError:
    print("python-dotenv not installed, using system environment variables")

### setting up the Reddit Instance

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT', '<console:SopranosBot:1.0 (by u/AlbertBareseBarese)>'),
    username=os.getenv('REDDIT_USERNAME'),
    password=os.getenv('REDDIT_PASSWORD')
)

### setting up Redis Connection

r = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    decode_responses=True,
    username=os.getenv('REDIS_USERNAME', 'default'),
    password=os.getenv('REDIS_PASSWORD'),
)

### setting up MongoDB Connection
try:
    # Use the MongoDB URI from environment variables
    mdb_username = os.getenv('MONGODB_USERNAME')
    mdb_password = os.getenv('MONGODB_PASSWORD')
    mdb_cluster = os.getenv('MONGODB_CLUSTER', 'cluster0.kh4xxy0.mongodb.net')
    uri = f"mongodb+srv://{mdb_username}:{mdb_password}@{mdb_cluster}/?retryWrites=true&w=majority&appName=Cluster0"
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