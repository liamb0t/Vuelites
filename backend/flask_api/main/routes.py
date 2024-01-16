from flask_api import app
from flask import jsonify, request, Blueprint
from flask_api.main.teams import leagues
from flask_api.main.utils import get_highlights, get_comments, get_redditor_profile, \
    get_redditor_submissions, search, load_directory, search_subreddits, \
    serialize_subreddit, get_icon, get_test_data

main = Blueprint('main', __name__)

@app.route("/highlights/<string:subreddit>/<string:filter>/<string:sort>", methods=["GET"])
def highlights(subreddit, filter='week', sort='top'):
    after = request.args.get('after')
    highlights = get_highlights(subreddit, sort, after, filter)
    return jsonify({
        'highlights': highlights,
    })

@app.route("/highlights-all/<string:league>/<string:filter>/<string:sort>", methods=["GET"])
def highlights_all(league, filter='week', sort='top'):
    after = request.args.get('after')
    subreddits_string = '+'.join([team for team in leagues[league]])
    highlights = get_highlights(subreddits_string, sort, after, filter, content_type='league')

    return jsonify({
        'highlights': highlights
    })


@app.route("/comments/<string:id>/<string:sort>")
def comments(id, sort='top'):
    return jsonify({
        'comments': get_comments(id, sort)
    })
  
@app.route("/redditor/<string:username>")
def redditor_profile(username):
    data = get_redditor_profile(username)
    return jsonify({
        'profile': data
    })

@app.route("/highlights/redditor/<string:username>")
def highlights_by_redditor(username):
    after = request.args.get('after')
    data = get_redditor_submissions(username, after)
    return jsonify({
        'highlights': data
    })


@app.route("/search/highlights/<string:query>/<string:time_filter>/<string:sorted_by>")
def highlights_by_search(query, time_filter, sorted_by):
    subreddits = request.args.getlist('sub')
    data = search(subreddits, query, time_filter, sorted_by)
    return jsonify({
        'search_results': data
    })

@app.route("/search/subreddits/<string:query>")
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

@app.route("/img/<string:subreddit>", methods=["GET"])
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