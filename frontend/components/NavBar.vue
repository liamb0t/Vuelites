<script setup lang="ts">
import { Trophy, Settings } from 'lucide-vue-next'
import { leagues } from '~/utils/utils'

const route = useRoute()
const activeLeagueId = computed(() => route.params.league || 'soccer')
const activeLeague = computed(() => {
    return leagues.find(league => league.id === activeLeagueId.value)
})
</script>
<template>
    <header>
        <div class="px-24 flex items-center justify-between py-4 w-full">
            <a href="/" class="flex items-center gap-2">
                <span class="text-2xl font-bold tracking-tight text-white">Golazo</span>
            </a>
            <SearchBar />
            <div class="flex items-center">
                <button :class="[
                    'text-white hover:bg-gray-800 hover:cursor-pointer p-2 rounded-md',
                    `hover:${activeLeague?.color || 'text-emerald-400'}`
                ]">
                    <Settings class="h-5 w-5" />
                    <span class="sr-only">Settings</span>
                </button>
            </div>
        </div>
    </header>
</template>
