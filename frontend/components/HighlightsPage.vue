<script setup lang="ts">
import { leagues } from '~/utils/utils'

const { getLeagueHighlights, getSubredditHighlights } = useHighlights()
const route = useRoute()

const highlights = ref<any>({ data: [], status: 'pending' })

const activeLeagueId = route.params.league as string || 'soccer'

// Initialize from URL queries or defaults with validation
const initSort = route.query.sort as string
const initTime = route.query.time as string

const searchQuery = ref<QueryParams>({
    sort: (['top', 'best', 'new', 'hot'].includes(initSort) ? initSort : 'top') as any,
    time: (['today', 'week', 'month', 'year', 'all'].includes(initTime) ? initTime : 'week') as any,
    after: '2023-10-01'
})

// Watch for query changes and update URL
watch(searchQuery, (newQuery) => {
    navigateTo({
        path: route.path,
        query: {
            sort: newQuery.sort !== 'top' ? newQuery.sort : undefined,
            time: newQuery.time !== 'week' ? newQuery.time : undefined
        }
    }, { replace: true })
}, { deep: true })

// Watch for URL query changes (back/forward navigation)
watch(() => route.query, (newQuery) => {
    const sort = newQuery.sort as string
    const time = newQuery.time as string

    if (sort && ['top', 'best', 'new', 'hot'].includes(sort)) {
        searchQuery.value.sort = sort as any
    } else {
        searchQuery.value.sort = 'top'
    }

    if (time && ['today', 'week', 'month', 'year', 'all'].includes(time)) {
        searchQuery.value.time = time as any
    } else {
        searchQuery.value.time = 'week'
    }
})

const activeLeague = computed(() => {
    return leagues.find(league => league.id === activeLeagueId)
})

watchEffect(async () => {
    if (activeLeagueId === 'soccer') {
        highlights.value = await getSubredditHighlights('soccer', searchQuery.value)
    } else {
        highlights.value = await getLeagueHighlights(activeLeagueId, searchQuery.value)
    }
})

// Prevent scrolling when loading
watchEffect(() => {
    if (highlights.value.status === 'pending') {
        document.body.style.overflow = 'hidden'
    } else {
        document.body.style.overflow = 'auto'
    }
})

// Cleanup on unmount
onUnmounted(() => {
    document.body.style.overflow = 'auto'
})



</script>
<template>
    <main v-if="activeLeague" class="relative min-h-screen flex flex-col">
        <div class="container flex flex-wrap gap-2 justify-end py-4"
            :class="highlights.status === 'pending' ? 'opacity-0' : 'opacity-100'">
            <PopularityFilter :active-league="activeLeague" v-model="searchQuery.sort" />
            <TimeFilter :active-league="activeLeague" v-model="searchQuery.time" />
        </div>
        <div class="flex flex-col gap-8 max-w-3xl mx-auto flex-1">
            <LoadingHighlights v-if="highlights.status === 'pending'" :active-league="activeLeague" />
            <Transition name="fade-in" appear>
                <div v-if="highlights.status === 'success'" class="flex flex-col gap-8">
                    <HighlightCard v-for="highlight in highlights.data.highlights" :key="highlight.id"
                        :highlight="highlight" :active-league="activeLeague" />
                </div>
            </Transition>
        </div>
    </main>
</template>
<style scoped>
.fade-in-enter-active {
    transition: opacity 0.5s ease;
}

.fade-in-enter-from {
    opacity: 0;
}

.fade-in-enter-to {
    opacity: 1;
}
</style>