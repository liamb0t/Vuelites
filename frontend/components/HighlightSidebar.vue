<script setup>
import { Download, ThumbsUp, ThumbsDown, MessageCircle } from 'lucide-vue-next';

const isMuted = ref(true)

const props = defineProps({
    highlight: {
        type: Object,
        required: true
    }
})

const emit = defineEmits(['openComments', 'toggleMute', 'goFullscreen'])

const toggleMute = () => {
    isMuted.value = !isMuted.value
    emit('toggleMute')
}

const goFullscreen = () => {
    emit('goFullscreen')
}

function download() {
    const url = props.highlight.video_url
    let filename = props.highlight.title
    if (!filename) filename = url.split('\\').pop().split('/').pop();
    fetch(url, {
        headers: new Headers({
            'Origin': location.origin
        }),
        mode: 'cors'
    })
        .then(response => response.blob())
        .then(blob => {
            let blobUrl = window.URL.createObjectURL(blob);
            let link = document.createElement('a');
            link.href = blobUrl;
            link.download = `${filename}.mp4`;
            document.body.appendChild(link);
            link.click()
            document.body.removeChild(link);
            URL.revokeObjectURL(blobUrl);
        })
        .catch(e => console.error(e));
}
</script>

<template>
    <div class="flex flex-col items-center justify-end pl-4 pr-2 gap-4">
        <!-- Thumbs up -->
        <HighlightSidebarButton>
            <template #icon>
                <ThumbsUp class="size-6 text-secondary" alt="thumbs up" />
            </template>
            <template #text>
                {{ highlight.ups }}
            </template>
        </HighlightSidebarButton>

        <!-- Thumbs down -->
        <HighlightSidebarButton>
            <template #icon>
                <ThumbsDown class="size-6 text-secondary" alt="thumbs down" />
            </template>
            <template #text>
                {{ highlight.downs }}
            </template>
        </HighlightSidebarButton>

        <!-- Comments -->
        <HighlightSidebarButton @click="$emit('openComments')">
            <template #icon>
                <MessageCircle class="size-6 text-secondary" alt="comments" />
            </template>
            <template #text>
                {{ highlight.num_comments }}
            </template>
        </HighlightSidebarButton>

        <!-- Toggle Mute
        <div class="flex items-center justify-center w-12 h-12 rounded-full bg-background-soft hover:bg-background-mute cursor-pointer"
            @click="toggleMute">
            <VolumeX v-if="highlight.has_audio && isMuted" class="size-6 text-secondary" alt="volume" />
            <Volume v-if="highlight.has_audio && !isMuted" class="size-6 text-secondary" alt="volume" />
        </div>
        <span class="text-sm font-light text-heading my-1 text-secondary">Sound</span> -->

        <!-- Download -->
        <HighlightSidebarButton @click="download">
            <template #icon>
                <Download class="size-6 text-secondary" alt="download" />
            </template>
            <template #text>
                Download
            </template>
        </HighlightSidebarButton>

        <a :href="`https://reddit.com/r/${highlight.subreddit}`" target="_blank">
            <div class="flex text-white text-sm font-semibold items-center gap-2">
                <img class="size-12 rounded-full" :src="highlight.community_icon" alt="">
            </div>
        </a>
    </div>
</template>
