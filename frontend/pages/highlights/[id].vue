<script setup lang="ts">
const route = useRoute()
const highlightId = route.params.id as string

// Fetch individual highlight data
const { data: highlightData, pending, error } = await useFetch(`/api/highlights/${highlightId}`)

// If highlight not found, show 404
if (error.value) {
  throw createError({
    statusCode: 404,
    statusMessage: 'Highlight not found'
  })
}

const highlight = computed(() => highlightData.value?.highlight || highlightData.value?.data?.highlight)

// Set page meta
useHead({
  title: highlight.value?.title || 'Highlight',
  meta: [
    { name: 'description', content: highlight.value?.title || 'Football highlight' }
  ]
})

// Get league info from subreddit
import { leagues } from '~/utils/utils'
const activeLeague = computed(() => {
  if (!highlight.value?.subreddit) return null

  // Find league by checking if subreddit matches any league's teams
  for (const [leagueId, teams] of Object.entries(leagues)) {
    if (Array.isArray(teams) && teams.includes(highlight.value.subreddit) || highlight.value.subreddit === leagueId) {
      return leagues[leagueId]
    }
  }
  return null
})

// Default to soccer league if no match found
const defaultLeague = leagues.soccer || {
  name: 'Soccer',
  id: 'soccer',
  color: 'text-emerald-400',
  bgColor: 'bg-emerald-400',
  borderColor: 'border-emerald-400'
}

const displayLeague = computed(() => activeLeague.value || defaultLeague)
</script>

<template>
  <div class="min-h-screen bg-gray-950 text-white">
    <div class="container mx-auto px-4 py-8">
      <!-- Loading state -->
      <div v-if="pending" class="flex justify-center items-center min-h-[60vh]">
        <div class="animate-spin rounded-full h-32 w-32 border-b-2 border-emerald-400"></div>
      </div>

      <!-- Highlight content -->
      <div v-else-if="highlight" class="max-w-4xl mx-auto">
        <!-- Header -->
        <div class="mb-6">
          <h1 class="text-3xl font-bold mb-4">{{ highlight.title }}</h1>
w
          <!-- Metadata -->
          <div class="flex items-center gap-6 text-sm text-gray-400">
            <div class="flex items-center gap-2">
              <span :class="['font-medium', displayLeague.color]">r/{{ highlight.subreddit }}</span>
            </div>
            <div>{{ highlight.date }}</div>
            <div class="flex items-center gap-1">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path
                  d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
              </svg>
              <span>{{ highlight.ups }}</span>
            </div>
            <div class="flex items-center gap-1">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd"
                  d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z"
                  clip-rule="evenodd" />
              </svg>
              <span>{{ highlight.num_comments }}</span>
            </div>
          </div>
        </div>

        <!-- Video Player -->
        <div class="mb-8">
          <VideoCard :highlight="highlight" />
        </div>

      </div>

      <!-- Error state -->
      <div v-else class="text-center py-12">
        <h1 class="text-4xl font-bold text-gray-400 mb-4">404</h1>
        <p class="text-xl text-gray-500 mb-8">Highlight not found</p>
        <NuxtLink to="/"
          class="inline-flex items-center px-6 py-3 bg-emerald-500 hover:bg-emerald-600 text-white font-medium rounded-lg transition-colors">
          Back to Home
        </NuxtLink>
      </div>
    </div>
  </div>
</template>