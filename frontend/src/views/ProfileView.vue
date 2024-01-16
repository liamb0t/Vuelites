<script setup>
import { ref, onMounted, watchEffect, onBeforeMount, onUnmounted } from 'vue';
import HighlightCard from '../components/HighlightCard.vue';
import RedditorProfile from '../components/RedditorProfile.vue';
import HighlightService from '../services/HighlightService.js';
import Loader from '../components/Loader.vue';
import { useHighlightsStore } from '@/stores/highlights';
import { storeToRefs } from 'pinia';

const store = useHighlightsStore()

const { isGridView, highlights } = storeToRefs(store)

const props = defineProps({
  redditor: {
    type: String,   
    required: true,
  },
})

const profile = ref(null)
const isLoading = ref(true)
const after = ref(null)
const observer = ref(null);
const isPaginating = ref(false)

const loadMoreHighlights = () => {
  isPaginating.value = true

  HighlightService.getHighlightsRedditor(props.redditor, after.value)
  .then((response) => {
      highlights.value.push(...response.data['highlights'])
      isPaginating.value = false
  })
  .catch((error) => {
      console.log(error);
  });
}

const loadHighlights = () => {
  HighlightService.getHighlightsRedditor(props.redditor, after.value)
  .then((response) => {
      highlights.value = response.data['highlights'];
      isLoading.value = true
  })
  .catch((error) => {
      console.log(error);
  });
}

onMounted(() => {
  highlights.value = null
  after.value = null

  loadHighlights()

  // Set up the intersection observer
  observer.value = new IntersectionObserver((entries) => {
    const [entry] = entries;
    if (entry.isIntersecting && highlights.value) {
      // Load more highlights
      after.value = highlights.value[highlights.value.length - 1].fullname
      if (!isPaginating.value) {
        loadMoreHighlights()
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

onBeforeMount(() => {
  HighlightService.getRedditorProfile(props.redditor)
  .then((response) => {
      profile.value = response.data['profile'];
  })
  .catch((error) => {
      console.log(error);
  });
})

onUnmounted(() => {
  // Disconnect the observer when the component is unmounted
  if (observer.value) {
    observer.value.disconnect();
  }
});

</script>

<template>
<div>
  <div class="main-container">
      <RedditorProfile :profile="profile"/>
      <div class="highlights" :class="{ grid: isGridView, list: !isGridView }">
          <HighlightCard 
          v-for="highlight in highlights" 
          :key="highlight.id" 
          :highlight="highlight" 
          :isGridView="isGridView"
          />
      </div>
      <div class="flex" v-if="isLoading">
        <Loader :style="'large'" />
      </div>
  </div>
  <div id="observer-target"></div>
</div>
</template>

<style scoped>
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
.flex {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 5rem;
}
</style>