<script setup lang="ts">
import { Trophy, Settings, Search, ArrowLeft } from 'lucide-vue-next'
import { leagues } from '~/utils/utils'

const route = useRoute()
const activeLeagueId = computed(() => route.params.league || 'soccer')
const activeLeague = computed(() => {
    return leagues.find(league => league.id === activeLeagueId.value)
})

// Mobile search state
const mobileSearchOpen = ref(false)
const searchBarRef = ref()

// Focus search input when mobile search opens
watch(mobileSearchOpen, (newVal) => {
    if (newVal) {
        nextTick(() => {
            searchBarRef.value?.focusInput()
        })
    }
})
</script>
<template>
    <header class="relative">
        <!-- Desktop Header -->
        <div class="hidden md:block container">
            <div class="px-4 md:px-8 lg:px-24 flex items-center justify-between py-4 w-full gap-4">
                <a href="/" class="flex items-center gap-2 flex-shrink-0">
                    <span class="text-xl md:text-2xl font-bold tracking-tight text-white">Golazo</span>
                </a>
                <div class="flex-1 max-w-lg">
                    <SearchBar ref="searchBarRef" />
                </div>
                <div class="flex items-center flex-shrink-0">
                    <button :class="[
                        'text-white hover:bg-gray-800 hover:cursor-pointer p-2 rounded-md',
                        `hover:${activeLeague?.color || 'text-emerald-400'}`
                    ]">
                        <Settings class="h-5 w-5" />
                        <span class="sr-only">Settings</span>
                    </button>
                </div>
            </div>
        </div>

        <!-- Mobile Header -->
        <div class="md:hidden">
            <!-- Fixed Header Container -->
            <div class="fixed top-0 left-0 right-0 z-50 bg-gray-950/95 backdrop-blur-sm border-b border-gray-800">
                <!-- Collapsed Header: Logo, Search Icon, Settings -->
                <div v-if="!mobileSearchOpen" class="px-4 flex items-center justify-between py-4">
                    <a href="/" class="flex items-center gap-2">
                        <span class="text-xl font-bold tracking-tight text-white">Golazo</span>
                    </a>

                    <div class="flex items-center gap-2">
                        <button @click="mobileSearchOpen = true"
                            class="text-white hover:bg-gray-800 hover:cursor-pointer p-2 rounded-md">
                            <Search class="h-5 w-5" />
                            <span class="sr-only">Search</span>
                        </button>
                        <button :class="[
                            'text-white hover:bg-gray-800 hover:cursor-pointer p-2 rounded-md',
                            `hover:${activeLeague?.color || 'text-emerald-400'}`
                        ]">
                            <Settings class="h-5 w-5" />
                            <span class="sr-only">Settings</span>
                        </button>
                    </div>
                </div>

                <!-- Expanded Search Bar -->
                <div v-if="mobileSearchOpen" class="px-4 py-4 flex items-center gap-3">
                    <div class="flex-1">
                        <SearchBar ref="searchBarRef" />
                    </div>
                    <button @click="mobileSearchOpen = false"
                        class="text-gray-400 hover:text-white p-2 rounded-md">
                        <ArrowLeft class="h-5 w-5" />
                        <span class="sr-only">Back</span>
                    </button>
                </div>
            </div>

            <!-- Spacer for fixed header -->
            <div class="h-16"></div>
        </div>
    </header>
</template>
