<script setup lang="ts">
import { Play, Pause, Maximize, Volume2, VolumeX } from 'lucide-vue-next'
import { leagues } from '~/utils/utils'
import { Slider } from '~/components/ui/slider'

const props = defineProps({
    highlight: {
        type: Object,
        required: true
    },
})

const { registerVideo, unregisterVideo, playVideo } = useVideoManager()

const route = useRoute()
const activeLeagueId = computed(() => route.params.league || 'soccer')
const activeLeague = computed(() => {
    return leagues.find(league => league.id === activeLeagueId.value)
})

const videoRef = ref<HTMLVideoElement | null>(null)
const audioRef = ref<HTMLAudioElement | null>(null)
const isPlaying = ref(false)
const progress = ref(0)
const duration = ref(0)
// Load saved volume from localStorage or default to 1
const savedVolume = typeof window !== 'undefined' ? parseFloat(localStorage.getItem('videoVolume') || '1') : 1
const savedPreviousVolume = typeof window !== 'undefined' ? parseFloat(localStorage.getItem('videoPreviousVolume') || '1') : 1
const savedMuted = typeof window !== 'undefined' ? localStorage.getItem('videoMuted') === 'true' : false

const volume = ref(savedVolume)
const previousVolume = ref(savedPreviousVolume)
const isMuted = ref(savedMuted)
const isFullscreen = ref(false)
const showPlayIcon = ref(false)
const showFullTitle = ref(false)

const truncatedTitle = computed(() => {
    const words = props.highlight.title.split(' ')
    const maxWords = 10
    if (words.length > maxWords) {
        return words.slice(0, maxWords).join(' ') + '...'
    }
    return props.highlight.title
})

const displayTitle = computed(() => {
    return showFullTitle.value ? props.highlight.title : truncatedTitle.value
})

const shouldShowMoreButton = computed(() => {
    return props.highlight.title.split(' ').length > 10
})

function playCurrentVideo() {
    console.log('Video clicked!', { paused: videoRef.value?.paused, isPlaying: isPlaying.value })

    if (videoRef.value && videoRef.value.paused) {
        // Pause all other videos first
        playVideo(props.highlight.id)

        videoRef.value.play()
        audioRef.value?.play()
        isPlaying.value = true
    }
    else if (videoRef.value && !videoRef.value.paused) {
        videoRef.value.pause()
        audioRef.value?.pause()
        isPlaying.value = false
    }

    // Show feedback icon briefly
    showPlayIcon.value = true
    setTimeout(() => {
        showPlayIcon.value = false
    }, 500)
}

function updateProgress() {
    if (videoRef.value) {
        const currentTime = videoRef.value.currentTime
        const totalDuration = videoRef.value.duration
        if (totalDuration > 0) {
            progress.value = (currentTime / totalDuration) * 100
        }
    }
}

function updateDuration() {
    if (videoRef.value) {
        duration.value = videoRef.value.duration
    }
}

onMounted(() => {
    if (videoRef.value) {
        videoRef.value.addEventListener('loadedmetadata', updateDuration)
        videoRef.value.addEventListener('timeupdate', updateProgress)
    }
})

function seekVideo(event: MouseEvent) {
    if (videoRef.value && duration.value > 0) {
        const progressBar = event.currentTarget as HTMLElement
        const rect = progressBar.getBoundingClientRect()
        const clickX = event.clientX - rect.left
        const percentage = clickX / rect.width
        const seekTime = percentage * duration.value

        videoRef.value.currentTime = seekTime
        audioRef.value!.currentTime = seekTime
    }
}

function toggleMute() {
    if (videoRef.value && audioRef.value) {
        if (isMuted.value || volume.value === 0) {
            // Unmute: restore previous volume
            volume.value = previousVolume.value
            isMuted.value = false
            videoRef.value.muted = false
            audioRef.value.muted = false
            videoRef.value.volume = volume.value
            audioRef.value.volume = volume.value
        } else {
            // Mute: save current volume and set to 0
            previousVolume.value = volume.value
            volume.value = 0
            isMuted.value = true
            videoRef.value.muted = true
            audioRef.value.muted = true
            videoRef.value.volume = 0
            audioRef.value.volume = 0
        }
        
        // Save to localStorage
        if (typeof window !== 'undefined') {
            localStorage.setItem('videoVolume', volume.value.toString())
            localStorage.setItem('videoPreviousVolume', previousVolume.value.toString())
            localStorage.setItem('videoMuted', isMuted.value.toString())
        }
    }
}

function updateVolume(newVolume: number) {
    volume.value = newVolume
    if (newVolume > 0) {
        previousVolume.value = newVolume
        isMuted.value = false
    } else {
        isMuted.value = true
    }
    
    // Save to localStorage
    if (typeof window !== 'undefined') {
        localStorage.setItem('videoVolume', newVolume.toString())
        localStorage.setItem('videoPreviousVolume', previousVolume.value.toString())
        localStorage.setItem('videoMuted', isMuted.value.toString())
    }
    
    if (videoRef.value && audioRef.value) {
        videoRef.value.volume = newVolume
        audioRef.value.volume = newVolume
        videoRef.value.muted = newVolume === 0
        audioRef.value.muted = newVolume === 0
    }
}

function toggleFullscreen() {
    if (!document.fullscreenElement) {
        videoRef.value?.requestFullscreen()
        isFullscreen.value = true
    } else {
        document.exitFullscreen()
        isFullscreen.value = false
    }
}

onMounted(() => {
    if (videoRef.value) {
        // Register this video with the manager
        registerVideo(
            props.highlight.id,
            videoRef.value,
            audioRef.value || undefined,
            () => { isPlaying.value = false }
        )

        // Apply saved volume settings
        videoRef.value.volume = volume.value
        videoRef.value.muted = isMuted.value
        if (audioRef.value) {
            audioRef.value.volume = volume.value
            audioRef.value.muted = isMuted.value
        }

        videoRef.value.addEventListener('loadedmetadata', updateDuration)
        videoRef.value.addEventListener('timeupdate', updateProgress)
    }
})

onUnmounted(() => {
    if (videoRef.value) {
        videoRef.value.removeEventListener('loadedmetadata', updateDuration)
        videoRef.value.removeEventListener('timeupdate', updateProgress)
    }

    // Unregister this video from the manager
    unregisterVideo(props.highlight.id)
})
</script>

<template>
    <div :class="[
        'relative h-[60dvh] overflow-hidden bg-transparent rounded-md transition-all w-full group',
        `hover:shadow-[0_0_15px_rgba(${activeLeague?.gradientColor || '52,211,153'},0.3)]`
    ]">
        <div class="relative w-full h-full">
            <video ref="videoRef" :src="highlight.video_url" :alt="highlight.title"
                class="w-full h-full object-cover cursor-pointer" loop @click="playCurrentVideo" />
            <audio ref="audioRef" :src="highlight.audio_url" class="hidden" loop />

            <!-- Feedback Icon - only shows briefly when state changes -->
            <div class="absolute inset-0 flex items-center justify-center pointer-events-none transition-all duration-200"
                :class="showPlayIcon ? 'opacity-100 scale-100' : 'opacity-0 scale-150'">
                <div class="size-16 rounded-full flex items-center justify-center bg-black/50 backdrop-blur-sm">
                    <Play v-if="isPlaying" class="size-8 ml-1 text-white" />
                    <Pause v-if="!isPlaying" class="size-8 text-white" />
                </div>
            </div>

            <!-- Top Right Controls -->
            <div
                class="absolute top-4 right-4 flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-auto">
                    <!-- Volume Control -->
                    <div class="group/volume">
                        <div class="flex items-center bg-black/50 backdrop-blur-sm rounded-full transition-all duration-300 group-hover/volume:rounded-r-full group-hover/volume:rounded-l-full">
                            <button @click="toggleMute" class="p-2 text-white hover:text-gray-300 transition-colors cursor-pointer">
                                <VolumeX v-if="isMuted || volume === 0" class="size-4" />
                                <Volume2 v-else class="size-4" />
                            </button>
                            <div class="w-0 group-hover/volume:w-24 transition-all duration-300 relative flex items-center">
                                <div class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 px-2 transform scale-x-0 group-hover/volume:scale-x-100 transition-transform duration-300 origin-center">
                                    <Slider 
                                        :model-value="[volume]" 
                                        @update:model-value="(value) => value && updateVolume(value[0])"
                                        :max="1" 
                                        :min="0" 
                                        :step="0.1"
                                        class="w-20 volume-slider-custom"
                                        :style="{ '--league-color': activeLeague?.gradientColor || '16 185 129' }"
                                    />
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Fullscreen Button -->
                    <button @click="toggleFullscreen"
                        class="bg-black/50 backdrop-blur-sm rounded-full p-2 text-white hover:text-gray-300 transition-colors cursor-pointer">
                        <Maximize class="size-4" />
                    </button>
            </div>

            <!-- Progress Bar -->
            <div class="absolute bottom-0 left-0 right-0 pt-4 cursor-pointer z-20 group/progress"
                @click="seekVideo">
                <div class="h-1 bg-black/20 group-hover/progress:h-2 transition-all duration-150">
                    <div :class="['h-full transition-all duration-100 ease-linear', activeLeague?.bgColor || 'bg-emerald-400']"
                        :style="{ width: progress + '%' }" />
                </div>
            </div>
        </div>
        <div class="p-4 absolute bottom-1 z-10 pointer-events-none">
            <div class="flex p-1 gap-2 rounded-lg items-center justify-between text-white pointer-events-auto">
                <div class="flex-1">
                    <h3 :class="['text-white', `group-hover:${activeLeague?.color || 'text-emerald-400'}`]"
                        :title="highlight.title">
                        {{ displayTitle }}
                    </h3>
                </div>
                <button v-if="shouldShowMoreButton" @click="showFullTitle = !showFullTitle"
                    class="ml-2 text-xs text-gray-300 hover:text-white transition-colors px-2 py-1">
                    {{ showFullTitle ? 'less' : 'more' }}
                </button>
            </div>
        </div>
    </div>
</template>

<style>
.volume-slider-custom [data-slot="slider-range"] {
  background: rgb(var(--league-color, 16 185 129)) !important;
}

.volume-slider-custom [data-slot="slider-thumb"] {
  border-color: rgb(var(--league-color, 16 185 129)) !important;
  background: white !important;
}

.volume-slider-custom [data-slot="slider-track"] {
  background: rgba(107, 114, 128, 0.5) !important;
}
</style>
