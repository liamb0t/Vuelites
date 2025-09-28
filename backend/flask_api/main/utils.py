from flask_api.main.config import reddit, headers
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import requests
from praw.models import MoreComments
from flask_api.main.teams import leagues

media_sites = ['streamin', 'dubz', 'imgur', 'twitter', 'streamff', 'streamable']
media_tags = [('Media'), ('Video'), 'Great Goal']

### test function, ignore
def get_test_data():
    return [(submission.title, submission.subreddit.display_name) for submission in reddit.subreddit("all-pics").top()]

### methods for extracting highlights from posts ###

def find_redirected_link(url):
    response = requests.head(url, allow_redirects=True)
    redirected_url = response.url
    return redirected_url

def scraper(url):
    response = requests.get(url, headers=headers)
    html = response.text    
    soup = bs(html, 'html.parser')
    video_element = soup.find('video')
    try:
        video_url = video_element['src']
        return video_url
    except:
        return None

def is_video(post):
    if post.is_video:
        return True
    elif post.link_flair_text in media_tags or post.link_flair_text in media_tags:
        if post.is_video:
            return True
        else:
            is_external_site(post)
    return False

def is_external_site(post):
    for site in media_sites:
        return True if site in post.url else False
    
def is_removed(post):
    if post.removed_by_category is None:
        return False
    elif post.removed_by_category in ('author', 'moderator', 'deleted', 'copyright_takedown'):
       return True
    else:
        print(f"Unknown post state: {post.removed_by_category}")

def has_video_url(post):
    if is_video(post) and not is_removed(post):
        if hasattr(post, 'media'):
            try:
                return post.media['reddit_video']['fallback_url']
            except:
                print('There was an error. This video might have been removed for copyright reasons')
        else:
            video_url = scraper(post.url)
            return video_url if video_url else None
        
def get_date(timestamp):
    dt_object = datetime.utcfromtimestamp(timestamp)
    return dt_object.strftime('%b %-d, %Y')

def get_downvotes(score, ratio, ups):
    if ratio == 0.5:  # If the ratio is 0.5, it means that the number of upvotes and downvotes is equal
        return ups - score  # This is because score = ups - downs, and if ups = downs, score should be 0.
    else:
        total_votes = ups / ratio
        downs = total_votes - ups
        return int(round(downs))

def get_audio_url(video_url, video_date):
    if video_date < 1672531200:
        return video_url.split('DASH_')[0] + 'DASH_audio.mp4'
    else:
        return video_url.split('DASH_')[0] + 'DASH_AUDIO_64.mp4'

def serialize(post, video_url, content_type):
    unix_timestamp = post.created_utc
    date = get_date(unix_timestamp)
    post_url = f"https://www.reddit.com{post.permalink}"
    author_username = post.author.name if post.author is not None else 'Deleted'
    audio_url = get_audio_url(video_url, unix_timestamp)
    ups = post.ups
    score = post.score
    downs = get_downvotes(score, post.upvote_ratio, ups)
    id = post.id
    
    if content_type in ('league', 'multi-search'):
        subreddit_display_name = post.subreddit.display_name
        community_icon = post.subreddit.community_icon
    else:
        subreddit_display_name = None
        community_icon = None

    return ({'video_url': video_url,
            'id': id,
            'audio_url': audio_url,
            'has_audio': True if audio_url else False,
            'subreddit': subreddit_display_name,
            'author': author_username,
            'title': post.title,
            'score': score,
            'ups': ups,
            'downs': downs,
            'date': date,
            'post_url': post_url,
            'num_comments': post.num_comments,
            'nsfw': True if post.over_18 else False,
            'fullname': 't3_' + id,
            'community_icon': community_icon
            })

def get_posts(subreddit, sort, time_filter, limit, params):
    if sort == 'top':
        return subreddit.top(time_filter=time_filter, limit=limit, params=params)
    elif sort == 'best':
        return subreddit.top(time_filter=time_filter, limit=limit, params=params)
    elif sort == 'new':
        return subreddit.new(limit=limit, params=params)
    elif sort == 'hot':
        return subreddit.hot(limit=limit, params=params)

def get_highlights(r, sort, after, time_filter='week', content_type='none', limit=100):
    highlights = []
    subreddit = reddit.subreddit(r)     
    # Parameters for fetching submissions
    params = {'after': after if after else None}

    for post in get_posts(subreddit, sort, time_filter, limit, params):
        url = has_video_url(post)
        if url:
            json_data = serialize(post, url, content_type=content_type)
            if content_type != 'league':
                json_data['community_icon'] = subreddit.community_icon
                json_data['subreddit'] = subreddit.display_name
            highlights.append(json_data)
    return highlights

def get_comments(id, sort):
    post = reddit.submission(id=id)
    post.comment_limit = 20
    post.comment_sort = sort
    comments = []
    for comment in post.comments:
        if not isinstance(comment, MoreComments):
            author = comment.author
            author_name = author.name if author else 'Deleted'
            if author_name != 'AutoModerator':
                comments.append({
                    'id': comment.id,
                    'author': author_name, 
                    'body': comment.body,
                    'date': get_date(comment.created_utc),
                    'ups': comment.ups})
    return comments

def get_redditor_submissions(username, after, limit=15, time_filter='all'):
    highlights = []
    redditor = reddit.redditor(username)
    params = {'after': after if after else None}
    posts = redditor.submissions.top(time_filter=time_filter, limit=limit, params=params)
    for post in posts:
        if post.subreddit.display_name in leagues.values() or post.subreddit.display_name == 'soccer':
            url = has_video_url(post)
            if url:
                json_data = serialize(post, url, post.subreddit)
                highlights.append(json_data)
    return highlights

def get_redditor_profile(username):
    redditor = reddit.redditor(username)
    return {
        'id': redditor.id,
        'username': username,
        'joined': get_date(redditor.created_utc),
        'avatar': redditor.icon_img,
        'comment_karma': redditor.comment_karma,
        'link_karma': redditor.link_karma
    }

def search(subreddits, query, time_filter, sort):
    highlights = []
    mutli_subreddit_string = '+'.join(subreddits)
    subreddit = reddit.subreddit(mutli_subreddit_string)
    content_type = 'multi-search' if len(subreddits) > 1 else 'none'

    if content_type != 'multi-search':
        community_icon = subreddit.community_icon
        display_name = subreddit.display_name

    for post in subreddit.search(query, limit=100, sort=sort, time_filter=time_filter):
        url = has_video_url(post)
        if url:
            json_data = serialize(post, url, content_type=content_type)
            highlights.append(json_data)

            if content_type != 'multi-search':
                json_data['community_icon'] = community_icon
                json_data['subreddit'] = display_name

    return highlights

def load_directory():
    data = []
    for league, teams in leagues.items():
        num_subscribers = 0
        for team in teams:
            subreddit = reddit.subreddit(team)
            if subreddit:
                try:
                    num_subscribers += subreddit.subscribers
                except:
                    print('Forbidden subreddit', subreddit)
       
        data.append({
            'name': league,
            'num_subscribers': num_subscribers,
        })
    return data

def league_directory_info(league):
    data = []
    num_subscribers = 0
    for team in leagues[league]:
        num_sunscribers += reddit.subreddit(team).subscribers
    try:
        data.append({
            'name': league,
            'num_subscribers': num_subscribers,
        })
    except:
        print('Error for this subreddit')

def subreddit_directory_info(s):
    subreddit = reddit.subreddit(s)
    try:
        return({
            'name': subreddit.display_name,
            'num_subscribers': subreddit.subscribers,
            'icon': subreddit.community_icon
        })
    except:
        print('Error for this subreddit')

def search_subreddits(query):
    results = []
    for league_name, teams in leagues.items():
        matching_teams = [team for team in teams if query.lower() in team.lower()]
        if matching_teams:
            results.extend(matching_teams)
    return results

def serialize_subreddit(r):
    try:
        subreddit = reddit.subreddit(r)
        return {
            'id': subreddit.id,
            'subreddit': subreddit.display_name,
            'community_icon': subreddit.community_icon,
            'subscribers': subreddit.subscribers
        }
    except:
        print(f'Error: r/{r} is forbidden')
   
def get_icon(subreddit):
    subreddit = reddit.subreddit(subreddit)
    try:
        return subreddit.community_icon
    except:
        print('Error getting community icon. This subreddit might be private')