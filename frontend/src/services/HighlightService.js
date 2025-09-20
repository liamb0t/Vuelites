import axios from 'axios'

const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:5000',
    withCredentials: false, 
    headers: {
        Accept: 'application/json',
        'Content-type': 'application/json'
    }
})

export default {
    getHighlightsSubreddit(subreddit, sort, filter, after) {
        const baseURL = `/highlights/${subreddit}/${filter}/${sort}`
        const url = after ? `${baseURL}?after=${after}` : baseURL;
        return apiClient.get(url);
    },
    getHighlightsLeague(league, sort, filter, after) {
        const baseURL = `/highlights-all/${league}/${filter}/${sort}`
        const url = after ? `${baseURL}?after=${after}` : baseURL;
        return apiClient.get(url);
    },
    getComments(postId, sort) {
        return apiClient.get(`/comments/${postId}/${sort}`);
    },
    getHighlightsRedditor(username, after) {
        const baseURL = `/highlights/redditor/${username}`
        const url = after ? `${baseURL}?after=${after}` : baseURL;
        return apiClient.get(url);
    },
    getRedditorProfile(username) {
        return apiClient.get(`/redditor/${username}`);
    },
    getSearchResults(subreddits, query, timeFilter, sort) {
        let baseURL = `/search/highlights/${query}/${timeFilter}/${sort}?sub=${subreddits[0].subreddit}`
        if (subreddits.length > 1) {
            subreddits.slice(1).forEach(subreddit => {
                baseURL += `&sub=${subreddit.subreddit}`
            });
        }
        return apiClient.get(baseURL);
    },
    getSubreddits(query) {
        return apiClient.get(`/search/subreddits/${query}`);
    },
    getSubredditImg(subreddit) {
        return apiClient.get(`/img/${subreddit}`);
    },
}