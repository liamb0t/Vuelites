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
    <!-- Mobile Layout: Full width video with sidebar inside -->
    <div class="md:hidden">
        <LayoutGroup>
            <div class="relative w-full">
                <VideoCard :highlight="highlight" />
                <!-- Mobile Sidebar - positioned inside video container -->
                <div class="absolute right-0 top-4 bottom-4 z-20 flex flex-col justify-end">
                    <HighlightSidebar @open-comments="openComments = true" :highlight="highlight" />
                </div>
            </div>
            <CommentsDialog :active-league="activeLeague" v-model="openComments" :highlight="highlight" />
        </LayoutGroup>
    </div>

    <!-- Desktop Layout: Video + external sidebar -->
    <div class="hidden md:flex flex-row space-x-2">
        <LayoutGroup>
            <div class="relative w-full">
                <VideoCard :highlight="highlight" />
            </div>
            <CommentsDialog :active-league="activeLeague" v-model="openComments" :highlight="highlight" />
        </LayoutGroup>
        <HighlightSidebar @open-comments="openComments = true" :highlight="highlight" />
    </div>
</template>