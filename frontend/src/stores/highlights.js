import { defineStore } from 'pinia'
import soccerIcon from '@/assets/icons/soccer-icon.png'

export const useHighlightsStore = defineStore('highlights', {
  state: () => ({
    highlights: [],
    isGridView: false,
    subreddit: 'soccer',
    subredditImg: soccerIcon,
    subredditDisplayText: 'All',
    endpoint: 'highlightsSubreddit',
    timeFilter: 'all',  
    sortedByFilter: 'top',
    isModalShowing: false,
    filter: 'week',
    isFullscreenGlobal: false
  }),
  actions: {
    setHighlights(highlights) {
      this.highlights = highlights
    },
    setGridView(value) {
      this.isGridView = value
    },  
    setSubreddit(value) {
      this.subreddit = value
    },
    setSubredditImg(value) {
      this.subredditImg = value
    },
    setSubredditDisplayText(value) {
      this.subredditDisplayText = value
    },
    setEndpoint(value) {
      this.endpoint = value
    },
    setTime(value) {
      this.timeFilter = value
    },
    sortedBy(value) {
      this.sortedByFilter= value
    },
    setModal(value) {
      this.isModalShowing = value
    },
    setFullscreen(value) {
      this.isFullscreenGlobal = value
      console.log(this.isFullscreenGlobal)
    }
  },
})
