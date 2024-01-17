  <script setup>
  import { onMounted, onBeforeUnmount, watchEffect } from 'vue';
  import Loader from '../components/Loader.vue';
  import { ref, watch } from 'vue';
  import { useHighlightsStore } from '@/stores/highlights';
  import { storeToRefs } from 'pinia';
  import fullScreenIcon from '@/assets/icons/arrow-down.svg';
  import volumeIcon from '@/assets/icons/volume.svg';
  import muteIcon from '@/assets/icons/mute.svg';

const store = useHighlightsStore()

const props = defineProps({
    videoUrl: String,
    audioUrl: String,
    isMuted: Boolean,
    preload: String,
    isFullscreen: Boolean,
    mouseOver: Boolean
  });

const emit = defineEmits(['exitFullscreen', 'toggleMute'])

  const videoElement = ref(null);
  const audioElement = ref(null);
  const playing = ref(true);
  const currentTime = ref(0);
  const duration = ref(0);
  const { isGridView } = storeToRefs(store)
  const progressbar = ref(null)
  const bufferbar = ref(null);
  const isBuffering = ref(null)
  const videoContainer = ref(null)
  const hover = ref(false)

  watch(videoElement, (newVal) => {
    if (newVal) {
      newVal.onloadedmetadata = () => {
        duration.value = newVal.duration;
      };
    }
  });

  const play = () => {
    videoElement.value.play();
    audioElement.value.play();
    playing.value = true;
  };

  const pause = () => {
    videoElement.value.pause();
    audioElement.value.pause();
    playing.value = false;
  };

  const onTimeUpdate = () => {
    currentTime.value = videoElement.value.currentTime;

    const progress = ((currentTime.value / duration.value) * 100) || 0;

    if (progressbar.value) {
      progressbar.value.style.setProperty("width", `${progress}%`);
    } 
  };

  const onSliderInput = (event) => {
    const time = (event.target.value / 100) * duration.value;
    progressbar.value.style.setProperty("width", `${(time / duration.value) * 100}%`);
    videoElement.value.currentTime = time;
    audioElement.value.currentTime = time;
  };

  const getBufferedPercentage = () => {
    if (videoElement.value && videoElement.value.buffered.length > 0) {
      const bufferedEnd = videoElement.value.buffered.end(videoElement.value.buffered.length - 1);
      const duration = videoElement.value.duration;
      return (bufferedEnd / duration) * 100;
    }
    return 0;
  };

  const onProgress = () => {
    const bufferedPercentage = getBufferedPercentage();
    if (bufferbar.value) {
      bufferbar.value.style.setProperty("width", `${bufferedPercentage}%`);
    }
  };

const exitFullscreen = () => {
  emit('exitFullscreen')
}

const toggleInfo = () => {
  hover.value = !hover.value
}

const toggleFullScreen = () => {
  if (!document.fullscreenElement) {
    videoContainer.value.requestFullscreen().catch(err => {
      alert(`Error attempting to enable full-screen mode: ${err.message} (${err.name})`);
    });
  } else {
    document.exitFullscreen() 
  }
};

const toggleMute = () => {
  emit('toggleMute')
}

// autoplay video when 50% of elem is visible
  let observer;

  onMounted(() => {
  const options = {
    threshold: 0.5, // 50% of the item's height
  };

  observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting && !isGridView.value && !document.fullscreenElement) {
        play();
      } else {
        pause();
      }
    });
  }, options);

  if (videoElement.value) {
    observer.observe(videoElement.value);
  }
});

//checks if video is buffering and pauses audio
watchEffect(() => {
    if (currentTime.value) {
      // Check if the video is buffering
      isBuffering.value = videoElement.value.readyState < 3 && !videoElement.value.paused && !videoElement.value.ended;
      if (isBuffering.value) {
        // Pause the audio when video is buffering
        audioElement.value.pause();
      } else if (playing.value) {
        // Resume the audio when video resumes
        audioElement.value.play();
      }
    }
  });

onBeforeUnmount(() => {
  if (observer) {
    observer.disconnect();
  }
});

watch(() => props.isFullscreen, (newValue, oldValue) => {
  // Code to run when myProp changes
  toggleFullScreen()
});

watch(() => props.mouseOver, (newValue, oldValue) => {
  props.mouseOver === true ? play() : pause()
});

</script>

  <template>
    <div class="main-container">
      <div class="video-container" ref="videoContainer">
        <div class="loader"  v-if="isBuffering">
          <Loader :style="'large'" />
        </div> 
        <!-- Add event listeners for play, pause, and timeupdate -->
        <video
          ref="videoElement"
          :src="videoUrl"
          @click="playing ? pause() : play()"
          @play="onTimeUpdate"
          @pause="onTimeUpdate"
          @timeupdate="onTimeUpdate"
          @progress="onProgress"
          :preload="preload"
          loop
        ></video>
        <transition name="fade">
          <div class="video-overlay" v-if="!isFullscreen || hover">
            <slot name="video-overlay"></slot> 
          </div>
        </transition>

        <audio ref="audioElement" :src="audioUrl" :muted="isMuted"></audio>
        <div v-if="isFullscreen">
          <div class="icon-container">
            <img 
              class="fullscreen"
              :src="fullScreenIcon"  
              @click="exitFullscreen"
            >
            <img 
              class="fullscreen"
              :src="isMuted ? muteIcon : volumeIcon" 
              @click="toggleMute" alt=""
            >
          </div>
        </div>
        <transition name="loading">
          <div v-if="isGridView && mouseOver">
            <div class="icon-container">
              <img 
                class="gridview"
                :src="isMuted ? muteIcon : volumeIcon" 
                @click="toggleMute" alt=""
              >
            </div>
          </div>
        </transition>
       
        <div class="player-controls">
          <div class="progress-bar" ref="progressbar"></div>
          <div class="buffer-bar" ref="bufferbar"></div> <!-- New buffer bar -->
          <input 
            type="range" 
            min="0" max="100" 
            :value="(currentTime / duration) * 100 || 0" 
            @input="onSliderInput" 
            @mouseover="toggleInfo"
            @mouseleave="toggleInfo"
          />
        </div>
      </div>
    </div>
  </template>

<style scoped>
.main-container {
  display: flex;
  height: 100%;
  width: 100%;
}
.video-container {
  position: relative;
  display: flex;
  flex: 1;
  background-color: black;

}
video {
  width: 100%;
  height: 100%;
  display: block; /* This ensures that there is no gap under the video */
}
.loader {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 100;
  display: flex;
  justify-content: center;
  align-items: center;
}
.player-controls {
  position: absolute;
  bottom: 0;
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(105, 105, 105, 0); /* Slight background to make text visible on light videos */
  z-index: 2;
}
.player-controls button {
  border: none;
  background-color: #39495c;
  color: white;
  cursor: pointer;
}

.player-controls button:hover {
  background-color: #2e3b4e;
}

.player-controls input[type="range"] {
  position: absolute;
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  background: transparent; /* Make the default background transparent */
  opacity: 1; /* Initially hidden */
  transition: opacity 0.1s ease; /* Smooth transition for opacity */
  z-index: 5;
}
.progress-bar {
    position: absolute;
    height: 4px;
    background-color: red;
    transition: height 0.2s ease;
    z-index: 5;
  }
.player-controls:hover .progress-bar, .player-controls:hover .buffer  -bar {
  height: 6px;
}
.buffer-bar {
  
  height: 4px; /* Same height as progress bar */
  background-color: grey; /* Different color for buffer */
  z-index: 1; /* Ensure it's behind the progress bar */
  transition: height 0.2s ease;
}
.player-controls input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 15px;
  height: 15px;
  background: red; /* Change thumb color */
  cursor: pointer;
  border-radius: 50%;
  transform: scale(0);
  transition: transform 0.2s ease-in-out; /* Smooth transition for opacity */
}

.player-controls:hover input[type="range"]::-webkit-slider-thumb {
  transform: scale(1);
}
.player-controls input[type="range"]::-moz-range-thumb {
  width: 15px;
  height: 15px;
  background: red; /* Change thumb color */
  cursor: pointer;
  border-radius: 50%;
}

.player-controls input[type="range"]::before {
  content: '';
  display: block;
  position: absolute;
  left: 0;
  height: 4px; /* Height of the filled part */
  background-color: rgb(20, 40, 170); /* Color of the filled part */
  z-index: 1;
}

.player-controls input:hover {
  cursor: pointer;
}

.video-overlay {
  position: absolute;
  bottom: 0;
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 1rem;
  padding-right: 6rem;
  padding-left: 1rem;
}

.icon-container {
  position: absolute;
  top: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.22);
  margin: 1rem;
  padding: 0.2rem 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 2px;
}

img.fullscreen {
  width: 1.2rem;
  height: 1.2rem;
  filter: invert(100%);
}
img.gridview {
  width: 1.2rem;
  height: 1.2rem;
  filter: invert(100%);
}
/* Fade Transition styles */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.fade-enter-to, .fade-leave-from {
  opacity: 1;
}
@media (max-width: 534px) {
  video {
    object-fit: cover;
  }
}
</style>
