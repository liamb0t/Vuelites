<script setup>
import { defineEmits, ref } from 'vue';
import mutedIcon from '@/assets/icons/mute.svg';
import volumeIcon from '@/assets/icons/volume.svg';
import CommentIcon from '@/assets/icons/comment-3.svg'
import fullscreenEnterIcon from '@/assets/icons/fullscreen-enter.svg';
import downloadIcon from '@/assets/icons/download.svg'


const isMuted = ref(true)

const props = defineProps({
    highlight: {
        type: Object,
        required: true
    }
})

// Define the emits
const emit = defineEmits(['fetchComments', 'toggleMute', 'goFullscreen']);

const fetchComments = () => {
  emit('fetchComments')
};

const toggleMute = () => {
  isMuted.value = !isMuted.value
  emit('toggleMute')
};

const goFullscreen = () => {
  emit('goFullscreen')
};

const a = document.getElementById("download-link");

function download() {
  const url = props.highlight.video_url
  let filename = props.highlight.title
  // Current blob size limit is around 500MB for browsers
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

      // Place the resource in the href of the link
      link.href = blobUrl;
      link.download = `${filename}.mp4`;
      document.body.appendChild(link);
      link.click()
      document.body.removeChild(link);
      // Revoke the Blob URL to free up resources
      URL.revokeObjectURL(blobUrl);
    })
    .catch(e => console.error(e));
}

</script>

<template>
  <div class="video-sidebar">
      <div class="img-container clickable" @click="fetchComments">
        <img class="comment-icon" :src="CommentIcon" alt="">
      </div>
      <span>{{ highlight.num_comments }}</span>
      <div class="img-container">
        <img class="thumbs-icon" src="@/assets/icons/thumbs-up.svg" alt="">
      </div>
      <span>{{ highlight.ups }}</span>
      <div class="img-container">
        <img class="thumbs-icon" src="@/assets/icons/thumbs-down.svg" alt="">
      </div>
      <span>{{ highlight.downs }}</span>
      <div class="img-container clickable" @click="toggleMute" >
        <img 
        v-if="highlight.has_audio"
        class="volume-icon"
        :src="isMuted ? mutedIcon : volumeIcon"
        alt=""
        />
      </div>
      <span>Sound</span>
      <div class="img-container clickable" @click="goFullscreen">
        <img 
          class="fullscreen-icon"
          :src="fullscreenEnterIcon"
          alt=""
        />
      </div>
      <span>Fullscreen</span>

      <div class="img-container clickable" @click="download">
        <img 
          class="download-icon"
          :src="downloadIcon"
          alt=""
        />
      </div>
      <span>Download</span>
  </div>
</template>
<style scoped>
.video-sidebar {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    flex-direction: column;
    padding-left: 1rem;
    padding-right: 0.5rem;
}

.img-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 3rem;
  width: 3rem;
  border-radius: 50%;
  background-color: var(--color-background-soft);
  padding: 0rem;
}
img {
  margin: 0;
  height: 1.5rem;
  width: 1.5rem;
}
.img-container:hover {
  background-color: var(--color-background-mute);
}
.img-container.clickable:hover {
  cursor: pointer;
}
span {
  color: var(--color-heading);
  font-size: smaller;
  font-weight: 600;
  margin-bottom: 0.2rem;
  margin-top: 0.25rem;
}
</style>
