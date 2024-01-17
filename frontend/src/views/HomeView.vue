<script setup>
import HighlightCard from '../components/HighlightCard.vue';
import Loader from '../components/Loader.vue';
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { useRoute } from 'vue-router'
import HighlightService from '../services/HighlightService.js';
import { useHighlightsStore } from '@/stores/highlights';
import { storeToRefs } from 'pinia';
import Utils from '../services/Utils.js';
import soccerIcon from '@/assets/icons/soccer-icon.png'

const store = useHighlightsStore()

const { highlights, isGridView } = storeToRefs(store)
const loadingText = ref('Fetching highlights')
const textKey = ref(0)

const props = defineProps({
  subreddit: {
    type: String,
    required: true,
    default: 'soccer'
  },
  timeFilter: {
    type: String,
    required: false, 
    default: 'week'
  },
  sortFilter: {
    type: String,
    required: false, 
    default: 'top'
  }
})

const route = useRoute()
const isLoading = ref(null)
const isPaginating = ref(false)
const elapsedTime = ref(0)
const after = ref(null)
const observer = ref(null);
const imgUrl = ref(soccerIcon)

const updateimg = () => { 
  const subreddit = route.params.subreddit
  
  if (subreddit) {
    const category = Utils.getImgUrl(subreddit)

    if (category) {
      imgUrl.value = category.img_url
    }
    
    else {
      HighlightService.getSubredditImg(subreddit)
      .then((response) => {
            imgUrl.value = response.data.img_url;
      })
      .catch((error) => { 
          console.log(error);
      });
    }
  } 
}

const loadHighlights = () => {
  highlights.value = null
  after.value = null
  loadingText.value = 'Fetching highlights'
  isLoading.value = true
  const league = route.name == 'highlightsLeague';
  const serviceFunc = league ? HighlightService.getHighlightsLeague : HighlightService.getHighlightsSubreddit;

  const interval = setInterval(() => {
    elapsedTime.value++;

    if (elapsedTime.value === 10) {
      loadingText.value = 'Almost there...';
      textKey.value++
    } else if (elapsedTime.value === 20) {
      loadingText.value = 'Just a little bit longer...';
      textKey.value++
    }
  }, 1000); // Run every 1 second

  serviceFunc(props.subreddit, props.sortFilter, props.timeFilter, after.value)
  .then((response) => {
      store.setHighlights(response.data['highlights'])
      isLoading.value = false
      clearInterval(interval); // Clear the interval after maxDuration
  })
  .catch((error) => {
      console.log(error);
  });
}

const loadMoreHighlights = () => {
  isPaginating.value = true
  const league = route.name == 'highlightsLeague';
  const serviceFunc = league ? HighlightService.getHighlightsLeague : HighlightService.getHighlightsSubreddit;

  serviceFunc(props.subreddit, props.sortFilter, props.timeFilter, after.value)
  .then((response) => {
      highlights.value.push(...response.data['highlights'])
      isPaginating.value = false
  })
  .catch((error) => {
      console.log(error);
  });
}


onMounted(() => {
  loadHighlights()
  updateimg()
  
  // Set up the intersection observer
  observer.value = new IntersectionObserver((entries) => {
    const [entry] = entries;
    if (entry.isIntersecting && highlights.value) {
      // Load more highlights
      // You can call the function inside the watchEffect here
      after.value = highlights.value[highlights.value.length - 1].fullname
      if (!isPaginating.value) {
        loadMoreHighlights()
        isPaginating.value = true
      }
    }
  }, {
    rootMargin: '200px', // Trigger the event a bit before reaching the element
  });

  // Start observing the target element
  const targetElement = document.getElementById('observer-target');
  if (targetElement) {
    observer.value.observe(targetElement);
  }
});

watch(() => props.subreddit, loadHighlights);
watch(() => props.timeFilter, loadHighlights);
watch(() => props.sortFilter, loadHighlights);
watch(() => route.params.subreddit, updateimg);

onUnmounted(() => {
  // Disconnect the observer when the component is unmounted
  if (observer.value) {
    observer.value.disconnect();
  }
});

</script>

<template>
  <transition name="loading">
    <div class="loader-container" v-if="isLoading">
      <div class="loader-inner">
        <Loader :style="'main'" />
        <img :src="imgUrl" alt="">
      </div>
        <span :key="textKey">{{ loadingText }}</span>
    </div>
  </transition>
  <div class="highlights" :class="{ grid: isGridView, list: !isGridView }">
    <HighlightCard 
      v-for="highlight in highlights" 
      :key="highlight.id" 
      :highlight="highlight" 
      :isGridView="isGridView"
    />
  </div>
  <div class="flex" v-if="isPaginating">
    <Loader :style="'large'" />
  </div>
  <div id="observer-target"></div>
</template>

<style scoped>
.flex {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 5rem;
}
.highlights.list {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.highlights.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1rem;
}
.loader-container {
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  min-height: 200px;
}
.loader-inner {
  position: relative;
  display: inline-block;
}
.loader-container img {
  display: block;
  width: 100px;
  max-height: 200px;
  object-fit: cover;
}
.loader-container span {
  font-weight: 500;
  max-width: 90%; /* Prevents text from overflowing the screen */
  text-align: center; /* Center the text */
  padding: 100px;
}
</style>