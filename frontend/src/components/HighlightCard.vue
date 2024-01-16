<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue';
import VideoPlayer from '../components/VideoPlayer.vue';
import Loader from '../components/Loader.vue';
import VideoOverlay from '../components/VideoOverlay.vue';
import CommentCard from '../components/CommentCard.vue';
import VideoSidebar from '../components/VideoSidebar.vue';
import HighlightService from '../services/HighlightService';
import crossIcon from '@/assets/icons/cross.svg';
import filterIcon from '@/assets/icons/filter.svg';
import { useHighlightsStore } from '@/stores/highlights';
import { storeToRefs } from 'pinia';

const store = useHighlightsStore()

const comments = ref([])
const viewingComments = ref(false)
const sort = ref('top')
const isMuted = ref(true)
const isFilterVisible = ref(false)
const filterbox = ref(null)
const filterbtn = ref(null)
const isFullscreen = ref(false)
const mouseOver = ref(false)
const { isGridView } = storeToRefs(store)

const props = defineProps({
  highlight: {
    type: Object,
    required: true
  },
  isGridView: {
    type: Boolean,
    required: true
  }
})

const toggleComments = () => {
  viewingComments.value = !viewingComments.value
  if (comments.value.length === 0) {
    fetchComments()
  }
};

const fetchComments = () => {
  comments.value = []
  if (!comments.value.length > 0) {
    HighlightService.getComments(props.highlight.id, sort.value)
    .then((response) => {
        comments.value = response.data['comments'];
    })
    .catch((error) => {
        console.log(error);
    });
  }
}

const toggleMute = () => {
  isMuted.value = !isMuted.value;
};


const toggleFullscreen = () => {
  isFullscreen.value = !isFullscreen.value
  store.setFullscreen(isFullscreen.value)
};

const toggleFilter = () => {
  isFilterVisible.value = !isFilterVisible.value
}

const updateSortedBy = (value) => {
  sort.value = value
  isFilterVisible.value = false
}

const handleClickOutside = (event) => {
  if (filterbox.value && !filterbox.value.contains(event.target) && !filterbtn.value.contains(event.target)) {
    isFilterVisible.value = false;
  }
};

let hoverTimeout;

const onMouseOver = () => {
  // Clear any existing timeout to avoid multiple triggers
  clearTimeout(hoverTimeout);

  hoverTimeout = setTimeout(() => {
    if (isGridView.value) {
      mouseOver.value = true;
    }
  }, 150); // 2000 milliseconds = 2 seconds
};

const onMouseLeave = () => {
  if (isGridView.value) {
      mouseOver.value = false;
    }
  // Clear the timeout if the user stops hovering
  clearTimeout(hoverTimeout);
};

onMounted(() => {
  window.addEventListener('click', handleClickOutside);
});

onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside);
});

watch(sort, fetchComments)

</script>

<template>
  <div class="highlight-card" :class="{ list: !isGridView, grid: isGridView}" @click="handleOpenVideo">
    <div class="video-player">
      <VideoPlayer 
        @exit-fullscreen="toggleFullscreen"
        @toggle-mute="toggleMute"
        @mouseover="onMouseOver"
        @mouseleave="onMouseLeave"
        :videoUrl="highlight.video_url" 
        :audioUrl="highlight.audio_url" 
        :isMuted="isMuted" 
        :isFullscreen="isFullscreen" 
        :mouseOver="mouseOver"
        :preload="'auto'">
        <template v-slot:video-overlay>
          <VideoOverlay :highlight="highlight"/>
        </template>
      </VideoPlayer>
      <div class="sidebar" :class="{ 'shift': viewingComments}">
        <VideoSidebar 
          v-show="!isGridView" 
          @fetch-comments="toggleComments" 
          @go-fullscreen="toggleFullscreen" 
          @toggle-mute="toggleMute" 
          :highlight="highlight" 
        />
      </div>
    </div>
  <transition name="slide">
    <div class="comments-container" v-if="viewingComments&&!isGridView">
      <div class="comments-header">
        <div>
          <span class="comments-title">Comments</span>
          <span class="comments-count">{{ highlight.num_comments }}</span>
        </div>
        <div>
          <img class="filter-btn" @click="toggleFilter" :src="filterIcon" alt="" ref="filterbtn">
          <transition name="fade">
            <div class="filter-dropdown" v-show="isFilterVisible" ref="filterbox">
              <div class="filter-option" :class="{ active: sort==='top'}" @click="updateSortedBy('top')">
                <span>Top comments</span>
              </div>
              <div class="filter-option" :class="{ active: sort==='new'}" @click="updateSortedBy('new')">
                <span>Newest</span>
              </div>
              <div class="filter-option" :class="{ active: sort==='controversial'}" @click="updateSortedBy('controversial')">
                <span>Controversial</span>
              </div>
            </div>
          </transition>
       
          <img @click="toggleComments" class="collapse-icon" :src="crossIcon" alt="">
        </div>
      </div>
      <div class="loader-container" v-if="comments.length === 0">
        <Loader :style="'large'"/>
      </div>
      <div class="cards-container">
        <CommentCard v-for="comment in comments" :key="comment.id" :comment="comment"/>
      </div>
    </div>
  </transition>
  </div>
</template>

<style scoped>

.video-player {
  display: flex;
  position: relative;
}
.highlight-card.list {
  display: flex;
  height: 80vh;
  margin-bottom: 48px;
  z-index: 2;
}
.highlight-card.grid {
  display: flex;
  height: 20rem;
  margin-bottom: 48px;
  z-index: 2;
}
.highlight-card.grid:hover {
  cursor: pointer;
}
.video-player {
  width: 45vw;
  z-index: 10;
}
.comments-container {
  padding: 0.5rem 0rem 0 1rem;
  width: 30vw;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
}

:root.dark .comments-container {
  background-color: var(--color-background-mute);
}
.comments-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.comments-title {
  color: var(--color-heading);
  font-size: 1.25rem;
  font-weight: 700;
  margin-right: 0.5rem;
}
.cards-container {
  height: 85%;
  overflow-y: scroll;
}
.filter-dropdown {
  background-color: var(--color-background);
  position: absolute;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
}
.filter-option {
  padding: 0.75rem;
}
.filter-option:hover {
  background-color: var(--color-background-soft);
  cursor: pointer;
}
.filter-option.active {
  background-color: var(--color-background-mute);
}

.sidebar {
  display: flex;
  align-items: flex-end;
  height: 100%;
}
.sidebar.shift {
  position: absolute;
  top: 0;
  right: 0;
  z-index: 999;
  padding-bottom: 1.5rem;
}

@media (max-width: 924px) {
  .video-player {
    width: 100%;
  }
}
@media (max-width: 924px) {
  .sidebar{
    position: absolute;
    top: 0;
    right: 0;
    z-index: 999;
    padding-bottom: 1.5rem;
  }
}
/* Transition styles */
.slide-enter-active {
  transition: transform 0.5s ease-in-out;
}

.slide-enter-from {
  transform: translateX(-100%);
}

.slide-enter-to {
  transform: translateX(0%);
}

img {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  padding: 10px;
}
img:hover {
  cursor: pointer;
  background-color: var(--color-background-mute);
}
.collapse-icon {
  margin-left: 1rem;
  margin-right: 0.5rem;
}
.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 90%;
}
/* Fade Transition styles */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
  transform-origin: top left;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: scale(0);
}
.fade-enter-to, .fade-leave-from {
  opacity: 1;
  transform: scale(1);
}
</style>
