<script setup lang="ts">
import { Motion, useMotionTemplate, useMotionValue, useAnimate } from 'motion-v'
import { leagues } from '~/utils/utils'

const route = useRoute()

const activeLeagueId = ref(route.params.league as string || 'soccer')

const activeLeague = computed(() => {
    return leagues.find(league => league.id === activeLeagueId.value)
})

watch(() => route.params.league, (newValue) => {
    activeLeagueId.value = newValue as string
    animate(primary, activeLeague.value?.gradientColor, { duration: 0.3 })
})

const [scope, animate] = useAnimate()

const primary = useMotionValue(activeLeague.value?.gradientColor)
const background = useMotionTemplate`linear-gradient(to bottom, rgb(${primary}), rgb(0 0 0))`

</script>
<template>
    <Motion :style="{ background }" class="fixed opacity-[10%] z-50 pointer-events-none top-0 left-0 size-full" />
</template>