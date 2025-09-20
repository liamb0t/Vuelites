export const useHighlights = () => {
    const baseURL = 'http://127.0.0.1:5000'
    
    const getLeagueHighlights = async (league: string, query: Object) => {
        const {data, status} = useFetch<Object>(`/api/highlights/league/${league}`, {
            baseURL: baseURL,
            query: query
        })
        return {
            data,
            status,
        }
    }

    const getSubredditHighlights = async (subreddit: string, query: Object) => {
        const {data, status} = useFetch<Object>(`/api/highlights/subreddit/${subreddit}`, 
        {
            baseURL: baseURL,
            query: query
        })
        return {
            data,
            status,
        }
    }

    const searchHighlights = async (searchQuery: string, query: Object) => {
        const {data, status} = useFetch<Object>(`/api/highlights/search/${searchQuery}`, {
            baseURL: baseURL,
            query: query
        })
        return {
            data,
            status,
        }
    }

    const getHighlightById = async (highlightId: string) => {
        const {data, status} = useFetch<Object>(`/api/highlights/${highlightId}`, {
            baseURL: baseURL
        })
        return {
            data,
            status,
        }
    }

    return {
        getLeagueHighlights,
        getSubredditHighlights,
        searchHighlights,
        getHighlightById,
    }
}
