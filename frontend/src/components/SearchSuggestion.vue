<script setup>
import { ref, computed } from 'vue'
import thumbsIcon from '@/assets/icons/thumbs-up-2.svg';
import commentIcon from '@/assets/icons/comment.svg';

const videoElement = ref(null);
const isLoaded = ref(false)

const props = defineProps({
    suggestion: {
        type: Object,
        required: true
    }
})

// Define the emits
const emit = defineEmits(['openedSuggestion']);

const openedSuggestion = () => {
  emit('openedSuggestion', props.suggestion)
};

const play = () => {
    videoElement.value.play()
}
const pause = () => {
    videoElement.value.pause()
    videoElement.value.currentTime = 0
}

const handleVideoLoad = () => {
  isLoaded.value = true
}


const maxTitleLength = 100;  

const content = computed(() => {
  if (props.suggestion.title.length > maxTitleLength) {
    return `${props.suggestion.title.substring(0, maxTitleLength)}...`;
  }
  return props.suggestion.title;
});
</script>

<template>
<li>
  <div class="suggestion-container" @mouseover="play" @mouseleave="pause" @click="openedSuggestion">
    <div class="info">
        <div class="header">
            <img v-if="suggestion.community_icon" class="subreddit-icon" :src="suggestion.community_icon" alt="">
            <span class="subreddit">r/{{ suggestion.subreddit }}</span>
            <span class="bull">&bull;</span>
            <span class="subreddit">Posted {{ suggestion.date }} by {{ suggestion.author }}</span>
        </div>
    
        <p class="title">{{ content }}</p>
        <div class="footer">
            <img :src="thumbsIcon" alt="">
            <span>{{ suggestion.ups }}</span>
            <img class="comment-icon" :src="commentIcon" alt="" style="margin-top: 0.25rem;">
            <span>{{ suggestion.num_comments }}</span>
        </div>
    </div>
    <transition name="loading">
      <div class="video-container" v-show="isLoaded">
          <video 
            :src="suggestion.video_url" 
            ref="videoElement" 
            muted 
            loop 
            :preload="'auto'"
            @loadedmetadata="handleVideoLoad"></video>
      </div>
    </transition>
  </div>
</li>
</template>

<style scoped>
p {
  white-space: normal;
  word-break: normal;
}
.suggestion-container {
padding: 1rem;
display: flex;
align-items: flex-start;
}
.suggestion-container:hover {
cursor: pointer;
background-color: var(--color-background-soft);
}
.info {
  flex: 1;
}
.header {
  font-size: smaller;
  display: flex;
  align-items: center;
}
.header img {
  width: 20px;
  height: 20px;
  margin-right: 0.4rem;
  border-radius: 50%;
}
.bull {
  font-size: 10px;
  margin: 0 0.3rem;
}
.title {
color: var(--color-heading);
text-align: justify;
font-weight: 600;
margin: 0.5rem 0;
margin-right: 1rem;
}

.footer {
  display: flex;
  align-items: center;
}
.footer img {
  width: 20px;
  height: 20px;
  margin-right: 0.2rem;
}
.comment-icon {
  margin-left: 0.4rem;
}

.video-container {
display: flex;
width: 6rem;
height: 80px;
justify-content: center;
align-items: center;
}
video {
object-fit: cover;
width: 100%;
height: 100%;
pointer-events: none;
border-radius: 10px;
}
@media (max-width: 1080px) {
  .video-container {
    display: none;
  }
}
</style>