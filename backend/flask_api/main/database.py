import uuid
import hashlib
from datetime import datetime, timedelta
from backend.flask_api.main.config import search_results_collection, search_cache_collection

def generate_highlight_id():
    """Generate a unique highlight ID for database storage"""
    return str(uuid.uuid4())[:8]  # Short UUID for URLs

def normalize_search_query(query, options):
    """Create a normalized search key for caching"""
    query_lower = query.lower().strip()
    sort = options.get('sort', 'top')
    time = options.get('time', 'all')
    return hashlib.md5(f"{query_lower}:{sort}:{time}".encode()).hexdigest()

def extract_search_terms(query):
    """Extract search terms from query for indexing"""
    # Simple tokenization - split on spaces and common punctuation
    import re
    terms = re.findall(r'\w+', query.lower())
    return list(set(terms))  # Remove duplicates

def create_lean_highlight_document(reddit_data, highlight_id):
    """Convert Reddit post data to lean database document"""
    return {
        'highlight_id': highlight_id,
        'reddit_id': reddit_data['id'],
        'search_terms': extract_search_terms(reddit_data['title']),
        'title': reddit_data['title'],
        'subreddit': reddit_data['subreddit'],
        'date': reddit_data['date'],
        'video_url': reddit_data['video_url'],
        'audio_url': reddit_data.get('audio_url', ''),
        'ups': reddit_data['ups'],
        'num_comments': reddit_data['num_comments'],
        'created_at': datetime.utcnow(),
        'last_accessed': datetime.utcnow()
    }

def save_search_result(reddit_data):
    """Save a search result to the database"""
    if search_results_collection is None:
        return None
    
    # Check if this reddit post already exists
    existing = search_results_collection.find_one({'reddit_id': reddit_data['id']})
    
    if existing:
        # Update last_accessed and return existing highlight_id
        search_results_collection.update_one(
            {'reddit_id': reddit_data['id']},
            {'$set': {'last_accessed': datetime.utcnow()}}
        )
        return existing['highlight_id']
    
    # Create new document
    highlight_id = generate_highlight_id()
    doc = create_lean_highlight_document(reddit_data, highlight_id)
    
    try:
        search_results_collection.insert_one(doc)
        return highlight_id
    except Exception as e:
        print(f"Error saving search result: {e}")
        return None

def save_search_cache(query, options, highlight_ids):
    """Save search cache entry"""
    if search_cache_collection is None:
        return
    
    cache_key = normalize_search_query(query, options)
    expires_at = datetime.utcnow() + timedelta(hours=1)  # 1 hour expiration
    
    cache_doc = {
        'search_query': cache_key,
        'search_options': options,
        'results': highlight_ids,
        'created_at': datetime.utcnow(),
        'expires_at': expires_at,
        'hit_count': 1
    }
    
    try:
        # Use upsert to update existing or create new
        search_cache_collection.replace_one(
            {'search_query': cache_key},
            cache_doc,
            upsert=True
        )
    except Exception as e:
        print(f"Error saving search cache: {e}")

def get_search_cache(query, options):
    """Get cached search results if available and not expired"""
    if search_cache_collection is None:
        return None
    
    cache_key = normalize_search_query(query, options)
    
    try:
        cache_doc = search_cache_collection.find_one({
            'search_query': cache_key,
            'expires_at': {'$gt': datetime.utcnow()}
        })
        
        if cache_doc:
            # Increment hit count
            search_cache_collection.update_one(
                {'_id': cache_doc['_id']},
                {'$inc': {'hit_count': 1}}
            )
            return cache_doc['results']
        
        return None
    except Exception as e:
        print(f"Error getting search cache: {e}")
        return None

def get_highlights_by_ids(highlight_ids):
    """Get highlight documents by their highlight_ids"""
    if search_results_collection is None or not highlight_ids:
        return []
    
    try:
        cursor = search_results_collection.find({'highlight_id': {'$in': highlight_ids}})
        highlights = list(cursor)
        
        # Convert MongoDB documents to the format expected by frontend
        results = []
        for doc in highlights:
            # Update last_accessed
            search_results_collection.update_one(
                {'_id': doc['_id']},
                {'$set': {'last_accessed': datetime.utcnow()}}
            )
            
            # Convert to frontend format (remove MongoDB _id and internal fields)
            result = {
                'id': doc['reddit_id'],
                'highlight_id': doc['highlight_id'],  # Include highlight_id for consistent navigation
                'title': doc['title'],
                'subreddit': doc['subreddit'],
                'date': doc['date'],
                'video_url': doc['video_url'],
                'audio_url': doc['audio_url'],
                'ups': doc['ups'],
                'num_comments': doc['num_comments']
            }
            results.append(result)
        
        return results
    except Exception as e:
        print(f"Error getting highlights by IDs: {e}")
        return []

def get_highlight_by_id(highlight_id):
    """Get a single highlight by highlight_id"""
    if search_results_collection is None:
        return None
    
    try:
        doc = search_results_collection.find_one({'highlight_id': highlight_id})
        
        if doc:
            # Update last_accessed
            search_results_collection.update_one(
                {'_id': doc['_id']},
                {'$set': {'last_accessed': datetime.utcnow()}}
            )
            
            # Convert to frontend format
            return {
                'id': doc['reddit_id'],
                'highlight_id': doc['highlight_id'],  # Include highlight_id for consistent navigation
                'title': doc['title'],
                'subreddit': doc['subreddit'],
                'date': doc['date'],
                'video_url': doc['video_url'],
                'audio_url': doc['audio_url'],
                'ups': doc['ups'],
                'num_comments': doc['num_comments']
            }
        
        return None
    except Exception as e:
        print(f"Error getting highlight by ID: {e}")
        return None

def create_indexes():
    """Create database indexes for optimized queries"""
    if search_results_collection is None or search_cache_collection is None:
        return
    
    try:
        # Search results indexes
        search_results_collection.create_index([('highlight_id', 1)], unique=True)
        search_results_collection.create_index([('reddit_id', 1)], unique=True)
        search_results_collection.create_index([('search_terms', 1)])
        search_results_collection.create_index([('last_accessed', 1)])
        
        # Search cache indexes
        search_cache_collection.create_index([('search_query', 1)], unique=True)
        search_cache_collection.create_index([('expires_at', 1)])
        
        print("MongoDB indexes created successfully")
    except Exception as e:
        print(f"Error creating indexes: {e}")

def cleanup_expired_cache():
    """Remove expired cache entries"""
    if search_cache_collection is None:
        return
    
    try:
        result = search_cache_collection.delete_many({
            'expires_at': {'$lt': datetime.utcnow()}
        })
        print(f"Cleaned up {result.deleted_count} expired cache entries")
    except Exception as e:
        print(f"Error cleaning up expired cache: {e}")

def cleanup_old_highlights():
    """Remove highlights that haven't been accessed in 30 days"""
    if search_results_collection is None:
        return
    
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        result = search_results_collection.delete_many({
            'last_accessed': {'$lt': cutoff_date}
        })
        print(f"Cleaned up {result.deleted_count} old highlight entries")
    except Exception as e:
        print(f"Error cleaning up old highlights: {e}")