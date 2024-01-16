import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProfileView from '../views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      props: route => ({ 
        timeFilter: route.query.time || 'week', 
        subreddit: route.params.subreddit,
        sortFilter: route.query.sort || 'top',
      }),
    },
    {
      path: '/r/:subreddit',
      name: 'highlightsSubreddit',
      component: HomeView,
      props: route => ({ 
        timeFilter: route.query.time || 'week', 
        subreddit: route.params.subreddit,
        sortFilter: route.query.sort || 'top',
      }),
    },
    {
      path: '/league/:subreddit',
      name: 'highlightsLeague',
      component: HomeView,
      props: route => ({ 
        timeFilter: route.query.time || 'week', 
        subreddit: route.params.subreddit,
        sortFilter: route.query.sort || 'top',
      }),
    },
    {
      path: '/u/:redditor',
      name: 'profile',
      props: true,
      component: ProfileView
    },
  ],
  scrollBehavior() {
    document.getElementById('app').scrollIntoView();
}
})

export default router
