<script setup lang="ts">
import { LayoutGroup } from 'motion-v'

defineProps({
    highlight: {
        type: Object,
        required: true
    },
    activeLeague: {
        type: Object,
        required: true
    }
})

const openComments = ref(false)
</script>

<template>
    <div class="relative flex flex-row space-x-2">
        <LayoutGroup>
            <VideoCard :highlight="highlight" />
            <CommentsDialog :active-league="activeLeague" v-model="openComments" :highlight="highlight" />
        </LayoutGroup>
        <HighlightSidebar @open-comments="openComments = true" :highlight="highlight" />
    </div>
</template>