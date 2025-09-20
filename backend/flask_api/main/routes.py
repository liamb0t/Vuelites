import os
from flask_api import app, r
from flask import jsonify, request, Blueprint, json, render_template
from flask_api.main.teams import leagues
from flask_api.main.utils import get_highlights, get_comments, get_redditor_profile, \
    get_redditor_submissions, search, load_directory, search_subreddits, \
    serialize_subreddit, get_icon, get_test_data
from flask_api.main.database import (
    get_search_cache, save_search_cache, save_search_result, 
    get_highlights_by_ids, get_highlight_by_id, create_indexes
)

main = Blueprint('main', __name__)

@app.route("/api/highlights/subreddit/<string:subreddit>", methods=["GET"])
def highlights_subreddit(subreddit):
    if subreddit not in leagues.values() and subreddit != 'soccer':
        return jsonify({
            'error': 'Subreddit not found'
        }), 404
    
    time = request.args.get('time', default='week')
    sort = request.args.get('sort', default='top')
    after = request.args.get('after')

    key = f'subreddit:{subreddit}:{sort}:{time}'
    cached_data = r.get(key)

    if cached_data:
        return jsonify({'highlights': json.loads(cached_data)})
    
    highlights = get_highlights(subreddit, sort, after, time)
    if highlights:
        r.set(key, json.dumps(highlights), ex=60 * 60 * 12)
        
    return jsonify({
        'highlights': highlights,
    })

@app.route("/api/highlights/league/<string:league>", methods=["GET"])
def highlights_league(league):
    if league not in leagues:
        return jsonify({
            'error': 'League not found'
        }), 404
    
    time = request.args.get('time', default='week')
    sort = request.args.get('sort', default='top')
    after = request.args.get('after')

    key = f'league:{league}:{sort}:{time}'
    cached_data = r.get(key)

    if cached_data:
        return jsonify({'highlights': json.loads(cached_data)})

    subreddits_string = '+'.join([team for team in leagues[league]])
    highlights = get_highlights(subreddits_string, sort, after, time, content_type='league')

    if highlights:
        r.set(key, json.dumps(highlights), ex=60 * 60 * 12)

    return jsonify({
        'highlights': highlights
    })


@app.route("/api/comments/<string:id>/<string:sort>")
def comments(id, sort='top'):
    return jsonify({
        'comments': get_comments(id, sort)
    })
  
@app.route("/api/redditor/<string:username>")
def redditor_profile(username):
    data = get_redditor_profile(username)
    return jsonify({
        'profile': data
    })

@app.route("/api/highlights/redditor/<string:username>")
def highlights_by_redditor(username):
    after = request.args.get('after')
    data = get_redditor_submissions(username, after)
    return jsonify({
        'highlights': data
    })


@app.route("/api/highlights/search/<string:query>")
def highlights_by_search(query):
    try:
        subreddits = request.args.getlist('r'
                                          ) if request.args.getlist('r') else ['soccer']
        time = request.args.get('time', default='all')
        sort = request.args.get('sort', default='top')
        
        # Create options dict for caching
        options = {'time': time, 'sort': sort, 'subreddits': subreddits}
        
        # Check database cache first
        cached_highlight_ids = get_search_cache(query, options)
        
        if cached_highlight_ids:
            print(f"Cache HIT for query: {query}")
            # Return cached results
            cached_results = get_highlights_by_ids(cached_highlight_ids)
            return jsonify({
                'search_results': cached_results,
                'data': {'search_results': cached_results}  # Frontend compatibility
            })
        
        print(f"Cache MISS for query: {query} - fetching from Reddit")
        
        # Cache miss - fetch from Reddit API
        reddit_data = search(subreddits, query, time, sort)
        
        if not reddit_data:
            return jsonify({
                'search_results': [],
                'data': {'search_results': []}
            })
        
        # Save each result to database and collect highlight_ids
        highlight_ids = []
        processed_results = []
        
        for result in reddit_data:
            try:
                highlight_id = save_search_result(result)
                if highlight_id:
                    highlight_ids.append(highlight_id)
                    # Keep the original format but add highlight_id for frontend URLs
                    result['highlight_id'] = highlight_id
                    processed_results.append(result)
            except Exception as e:
                print(f"Error saving search result: {e}")
                # Still include the result even if saving fails
                processed_results.append(result)
        
        # Cache the search results
        if highlight_ids:
            try:
                save_search_cache(query, options, highlight_ids)
            except Exception as e:
                print(f"Error saving search cache: {e}")
        
        return jsonify({
            'search_results': processed_results,
            'data': {'search_results': processed_results}  # Frontend compatibility
        })
        
    except Exception as e:
        print(f"Error in search route: {e}")
        return jsonify({
            'search_results': [],
            'data': {'search_results': []},
            'error': 'Search failed'
        }), 500

@app.route("/api/highlights/<string:highlight_id>")
def get_highlight_by_highlight_id(highlight_id):
    """Get individual highlight by highlight_id"""
    highlight = get_highlight_by_id(highlight_id)
    
    if highlight:
        return jsonify({
            'highlight': highlight,
            'data': {'highlight': highlight}  # Frontend compatibility
        })
    else:
        return jsonify({
            'error': 'Highlight not found'
        }), 404

@app.route("/api/search/subreddits/<string:query>")
def get_subreddits(query):
    data = []
    subreddits = search_subreddits(query)
    for subreddit in subreddits:
        result = serialize_subreddit(subreddit)
        if result is not None:
            data.append(result)
    sorted_results = sorted(data, key=lambda x: x['subscribers'], reverse=True)
    return jsonify({
        'search_results': sorted_results
        })

@app.route("/directory/leagues/all", methods=["GET"])
def league_directory():
    return jsonify({
        'directory_data': load_directory(),
    })

@app.route("/directory/subreddit/<string:subreddit>", methods=["GET"])
def subreddit_directory(league, filter='week'):
    all_highlights = []
    for team in leagues[league]:
        try:
            all_highlights.extend(get_highlights(team, limit=10, filter=filter))
        except:
            print(f"Access to r/{team} is forbidden.")
    sorted_highlights = sorted(all_highlights, key=lambda x: x['score'], reverse=True)
    return jsonify({
        'highlights': sorted_highlights,
    })

@app.route("/api/img/<string:subreddit>", methods=["GET"])
def get_subreddit_icon(subreddit):
    return jsonify({
        'img_url': get_icon(subreddit),
    })

@app.route("/test")
def test():
    data = get_test_data()
    return jsonify({
        'test_data': data
    })


client_bp = Blueprint('client',
    __name__,
    static_folder='dist',
    template_folder='dist',
    static_url_path='/'
    )

@client_bp.route('/img/<path:filename>')
def serve_images(filename):
    from flask import send_from_directory
    return send_from_directory(os.path.join(client_bp.static_folder, 'img'), filename)

@client_bp.route('/_nuxt/<path:filename>')
def serve_nuxt_assets(filename):
    from flask import send_from_directory
    return send_from_directory(os.path.join(client_bp.static_folder, '_nuxt'), filename)

@client_bp.route('/', defaults={'path': ''})
@client_bp.route('/<path:path>')
@client_bp.route('/<string:path>')
def index(path=''):
    return render_template('index.html')

# Initialize database indexes when the app starts
try:
    create_indexes()
except Exception as e:
    print(f"Failed to create database indexes: {e}")