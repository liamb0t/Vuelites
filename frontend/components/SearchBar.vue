<script setup lang="ts">
import { Search, MessageCircle, ThumbsUp, Loader2 } from 'lucide-vue-next'
import { onClickOutside } from '@vueuse/core'
import { leagues } from '~/utils/utils'
const { searchHighlights } = useHighlights()

const route = useRoute()
const query = ref('')
const results = ref()
const showResults = ref(false)
const searchContainer = ref<HTMLElement>()
const searchInput = ref<HTMLInputElement>()
const isLoading = ref(false)

// Expose focus method for parent components
const focusInput = () => {
    if (searchInput.value) {
        searchInput.value.focus()
    }
}

defineExpose({
    focusInput
})

const activeLeagueId = computed(() => route.params.league || 'soccer')
const activeLeague = computed(() => {
    return leagues.find(league => league.id === activeLeagueId.value)
})

function debounce<T extends (...args: any[]) => void>(fn: T, delay = 300): (...args: Parameters<T>) => void {
    let timeout: ReturnType<typeof setTimeout>
    return (...args: Parameters<T>) => {
        clearTimeout(timeout)
        timeout = setTimeout(() => fn(...args), delay)
    }
}

const fetchResults = async (query: string, options: { time: string; sort: string }) => {
    isLoading.value = true
    try {
        results.value = await searchHighlights(query, options)
        showResults.value = true
    } finally {
        isLoading.value = false
    }
}

const debouncedFetch = debounce(fetchResults, 300)

const closeResults = () => {
    showResults.value = false
}

const onFocus = () => {
    if (query.value.trim() !== '' && results.value && results.value.data && results.value.data.search_results && results.value.data.search_results.length > 0) {
        showResults.value = true
    }
}

onClickOutside(searchContainer, closeResults)

watch(query, (newVal) => {
    if (newVal.trim() !== '') {
        debouncedFetch(newVal, {
            time: 'all',
            sort: 'top'
        })
        console.log('Results:', results.value)
    } else {
        closeResults()
    }
})

</script>
<template>
    <div ref="searchContainer" class="relative w-full max-w-lg md:block">
        <Search v-if="!isLoading" class="absolute left-2.5 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
        <Loader2 v-if="isLoading"
            :class="['absolute left-2.5 top-1/2 transform -translate-y-1/2 h-4 w-4 animate-spin', activeLeague?.color || 'text-emerald-400']" />
        <input ref="searchInput" v-model="query" type="search" placeholder="Search highlights" :class="[
            'w-full text-sm p-2 rounded-full border border-gray-800 bg-gray-900 pl-9 text-white placeholder:text-gray-400 focus-visible:ring focus-visible:outline-none',
            `focus-visible:ring-${activeLeague?.color?.replace('text-', '') || 'emerald-400'}`
        ]" @focus="onFocus" />
        <div v-if="showResults && results && results.data && results.data.search_results && results.data.search_results.length > 0"
            class="absolute z-10 mt-2 w-full rounded-md bg-gray-800 shadow-lg overflow-hidden">
            <ul class="max-h-96 overflow-y-auto">
                <li v-for="result in results.data.search_results" :key="result.id"
                    class="p-4 hover:bg-gray-700 border-b border-gray-700 last:border-b-0 first:rounded-t-md last:rounded-b-md">
                    <NuxtLink
                        :to="`/highlights/${result.highlight_id}`"
                        class="block">
                        <div class="flex gap-4">
                            <!-- Main content -->
                            <div class="flex-1">
                                <!-- Top: Subreddit and date -->
                                <div class="flex items-center gap-2 mb-2">
                                    <span
                                        :class="['text-xs font-medium', activeLeague?.color || 'text-emerald-400']">r/{{
                                            result.subreddit }}</span>
                                    <span class="text-xs text-gray-400">•</span>
                                    <span class="text-xs text-gray-400">{{ result.date }}</span>
                                </div>

                                <!-- Middle: Title -->
                                <h3 class="text-white font-medium text-sm leading-tight mb-3 line-clamp-2">
                                    {{ result.title }}
                                </h3>

                                <!-- Bottom: Stats -->
                                <div class="flex items-center gap-4 text-xs text-gray-400">
                                    <div class="flex items-center gap-1">
                                        <ThumbsUp class="w-3 h-3" />
                                        <span>{{ result.ups || 0 }}</span>
                                    </div>
                                    <div class="flex items-center gap-1">
                                        <MessageCircle class="w-3 h-3" />
                                        <span>{{ result.num_comments || 0 }}</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Right: Video preview -->
                            <div class="w-20 h-14 flex-shrink-0">
                                <video v-if="result.video_url" :src="result.video_url"
                                    class="w-full h-full object-cover rounded bg-gray-900" muted preload="metadata"
                                    @mouseenter="($event.target as HTMLVideoElement)?.play()"
                                    @mouseleave="($event.target as HTMLVideoElement)?.pause()" />
                                <div v-else class="w-full h-full bg-gray-900 rounded flex items-center justify-center">
                                    <span class="text-gray-500 text-xs">No video</span>
                                </div>
                            </div>
                        </div>
                    </NuxtLink>
                </li>
            </ul>
        </div>
    </div>
</template>