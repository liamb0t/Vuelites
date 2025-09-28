<script setup>
import { Motion } from 'motion-v'
import { leagues } from '~/utils/utils'

const props = defineProps({
    activeLeague: {
        type: Object,
        required: true
    }
})

const route = useRoute()

const activeLeagueId = ref(route.params.league || 'soccer')

const activeLeague = computed(() => {
    return leagues.find(league => league.id === activeLeagueId.value)
})

watch(() => route.params.league, (newValue) => {
    activeLeagueId.value = newValue
})

</script>

<template>
    <div class="no-scrollbar w-full overflow-x-auto">
        <nav class="flex border-gray-800 transition-all duration-200">
            <div class="relative w-full flex md:items-center md:justify-center">
                <NuxtLink :external="false" :to="'/' + league.id" v-for="league in leagues" :key="league.id"
                    class="hover:cursor-pointer" :class="[
                        'relative py-4 px-4.5 md:px-6 lg:px-12 text-sm font-medium transition-colors text-nowrap',
                        activeLeague.id === league.id ? 'text-white' : 'text-gray-400 hover:bg-gray-900'
                    ]">
                    {{ league.name }}
                    <Motion v-if="activeLeague.id === league.id" layout-id="underline" :class="league.bgColor"
                        class="absolute bottom-0 left-0 right-0 h-[2px]" />
                </NuxtLink>
                <div class="hidden md:block absolute bottom-0 rounded-lg left-0 right-0 h-[2px] opacity-30 transition-colors duration-300"
                    :class="activeLeague.bgColor" />
            </div>
        </nav>
    </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>