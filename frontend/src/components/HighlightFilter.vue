<script setup>
import { ref, computed, onMounted, onBeforeUnmount} from 'vue'
import { useRoute, RouterLink } from 'vue-router';
import GridIcon from '@/assets/icons/grid-view.svg';
import ListIcon from '@/assets/icons/list-view.svg';
import CheckIcon from '@/assets/icons/check-icon.svg';
import { useHighlightsStore } from '@/stores/highlights';

const route = useRoute()
const showOptions = ref(false)
const isGridView= ref(false)
const filter = ref(false)

const props = defineProps({
  timeFilter: {
    type: String,
    required: true,
    default: 'week'
  },
  sortFilter: {
    type: String,
    required: true,
    default: 'top'
  },
})

const store = useHighlightsStore()

const toggleOptions = () => {
    showOptions.value = !showOptions.value
}

const text = computed(() => {
  const defaultTextSortFilter = route.query.sort || 'top'
  const defaultTextTimeFilter = route.query.time || 'week'

  const computedString = defaultTextSortFilter.charAt(0).toUpperCase() + defaultTextSortFilter.slice(1)

  if (route.query.time === 'all') {
    return computedString + ' ' + 'of all time'
  } 
  else if (route.query.time === 'day') {
    return computedString + ' ' + 'today'
  }
  else if (route.query.sort === 'new') {
    return 'Newest'
  }
  else if (route.query.sort === 'hot') {
    return 'Hottest'
  }
  else {
    return computedString + ' this ' + defaultTextTimeFilter
  }
})

function listMode() {
  isGridView.value = false;
  store.setGridView(false)
}

function gridMode() {
  isGridView.value = true;
  store.setGridView(true)
}

const handleClickOutside = (event) => {
  if (filter.value && !filter.value.contains(event.target)) {
    showOptions.value = false;
  }
};

onMounted(() => {
  window.addEventListener('click', handleClickOutside);
});

onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside);
});

</script>
<template>
<div class="button-container" @click="toggleOptions" ref="filter">
  <div class="button-container-inner">
    <span>{{ text }}</span>
    <img :src="isGridView ? GridIcon : ListIcon" alt="">
  </div>
  <div v-show="showOptions" class="options">
    <ul>
      <div class="legend">
        <span>Sort by</span>
      </div>
      <RouterLink 
        :to="{ 
          name: route.name, 
          params: { subreddit: route.params.subreddit},
          query: { time: route.query.time, sort: 'top'}  
        }">
        <div class="option">
          <span>Top</span>
          <img :src="CheckIcon" alt="" v-if="route.query.sort=='top' || !route.query.sort">
        </div>
      </RouterLink>
      <RouterLink 
        :to="{ 
          name: route.name, 
          params: { subreddit: route.params.subreddit},
          query: { time: route.query.time, sort: 'hot'}  
        }">
        <div class="option">
          <span>Hottest</span>
          <img :src="CheckIcon" alt="" v-if="route.query.sort=='hot'">
        </div>
      </RouterLink>
      <RouterLink 
        :to="{ 
          name: route.name, 
          params: { subreddit: route.params.subreddit},
          query: { sort: 'new'}  
        }">
         <div class="option">
          <span>Newest</span>
          <img :src="CheckIcon" alt="" v-if="route.query.sort=='new'">
        </div>
      </RouterLink>
    </ul>
    <ul v-if="route.query.sort==='top' || !route.query.sort">
      <div class="legend">
        <span>Date by</span>
      </div>
      <RouterLink 
        :to="{ 
          name: route.name, 
          params: { subreddit: route.params.subreddit},
          query: { time: 'day', sort: route.query.sort}  
        }">
        <div class="option">
          <span>Today</span>
          <img :src="CheckIcon" alt="" v-if="route.query.time=='day'">
        </div>
      </RouterLink>
    
      <RouterLink 
        :to="{ 
          name: route.name, 
          params: { subreddit: route.params.subreddit},
          query: { time: 'week', sort: route.query.sort}  
        }">
        <div class="option">
          <span>This week</span>
          <img :src="CheckIcon" alt="" v-if="route.query.time=='week' || !route.query.time">
        </div>
      </RouterLink>
      <RouterLink 
        :to="{ 
          name: route.name, 
          params: { subreddit: route.params.subreddit},
          query: { time: 'month', sort: route.query.sort}  
        }">
        <div class="option">
          <span>This month</span>
          <img :src="CheckIcon" alt="" v-if="route.query.time=='month'">
        </div>
      </RouterLink>
      <RouterLink 
        :to="{ 
          name: route.name, 
          params: { subreddit: route.params.subreddit},
          query: { time: 'year', sort: route.query.sort}  
        }">
         <div class="option">
          <span>This year</span>
          <img :src="CheckIcon" alt="" v-if="route.query.time=='year'">
        </div>
      </RouterLink>
      <RouterLink 
        :to="{ 
          name: route.name, 
          params: { subreddit: route.params.subreddit},
          query: { time: 'all', sort: route.query.sort}  
        }">
        <div class="option">
          <span>All time</span>
          <img :src="CheckIcon" alt="" v-if="route.query.time=='all'">
        </div>
      </RouterLink>
    </ul>
    <div>
      <div class="legend">
        <span>View as</span>
      </div>
      <div @click="listMode()">
        <div class="flexbox">
          <div class="option">
            <div class="option-inner">
              <div class="view-option-text">
                <span>List</span>
              </div>
              <img :src="ListIcon" alt="">
            </div>
          </div>
          <div class="check-icon-container">
            <img class="check-icon" :src="CheckIcon" alt="" v-if="!isGridView">
          </div>
        </div>
      </div>
      <div @click="gridMode()">
        <div class="flexbox">
          <div class="option">
            <div class="option-inner">
              <div class="view-option-text">
                <span>Grid</span>
              </div>
           
              <img :src="GridIcon" alt="">
            </div>
          </div>
          <div class="check-icon-container">
            <img :src="CheckIcon" alt="" v-if="isGridView">
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

</template>
<style scoped>
.button-container {
  position: relative;
  border: 1px solid var(--vt-c-divider-light-2);
  border-radius: 10px;
  width: 100%;
  min-width:6rem;
  background-color:var(--color-background-mute);
}
.button-container:hover {
  cursor: pointer;
}
.button-container-inner {
  color: var(--color-heading);
  display: flex;
  align-items: center;
  padding: 0.5rem;
}
.button-container-inner span {
  font-weight: 600;
}
.options {
background-color: var(--color-background);
position: absolute;
width: 100%;
margin-top: 0.5rem;
box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); /* horizontal offset, vertical offset, blur radius, spread radius, color */
-webkit-box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); /* For Safari */
-moz-box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); /* For old Firefox versions */
z-index: 999;
padding: 0.2rem;
}
:root.dark .options {
  background-color: var(--color-background-mute);
}
ul {
  padding: 0;
  border-bottom: 1px solid var(--vt-c-divider-light-2);
}
.legend span {
  color: var(--color-text);
  font-weight: 500;
  font-size: 0.75rem;
}
.option {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  
}
.option span {
  color: var(--color-heading);
  font-weight: 500;
  text-align: left;
  flex-grow: 1;
}
.option:hover, .flexbox:hover {
  cursor: pointer;
  background-color: var(--color-background-soft);
}
img {
  height: 14px;
  width: 14px;;
  margin-left: 0.3rem;
}
.flexbox {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.legend {
  display: flex;
  padding: 0.5rem;
}
.option-inner {
  display: flex;
  align-items: center;
}
.check-icon-container {
  padding-right: 0.5rem;
}
.view-option-text {
  width: 2rem;
}
@media (max-width: 385px) {
  .button-container-inner img {
    display: none;
  }
}
</style>

