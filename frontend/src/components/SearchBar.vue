<script setup>
import { ref, watch, onBeforeUnmount, onMounted, computed} from 'vue'
import SearchSuggestion from '../components/SearchSuggestion.vue';
import Modal from '../components/Modal.vue';
import debounce from 'lodash.debounce'
import HighlightService from '../services/HighlightService';
import Loader from '../components/Loader.vue';
import searchIcon from '@/assets/icons/search-icon.svg';
import backIcon from '@/assets/icons/back.svg';
import filterIcon from '@/assets/icons/filter-2.svg';
import { useHighlightsStore } from '@/stores/highlights';

const searchQuery = ref("")
const timeFilter  = ref('all')
const sortedByFilter = ref('top')
const subreddits = ref([{'subreddit': 'soccer', 'icon': 'https://styles.redditmedia.com/t5_2qi58/styles/communityIcon_fihq6rzyq7q91.png?width=256&s=3497aeefc618e652e94ba8b3e6b3318e213d0b55'}])
const subredditIcon = ref(null)
const suggestions = ref([])
const isLoading = ref(false)
const isDropdownVisible = ref(false)
const dropdown = ref(null);
const input = ref(null)
const filterBtn = ref(null);
const modal = ref(null)
const pages = ref(1)

const store = useHighlightsStore()

const debouncedWatch = debounce(() => {
  fetchSuggestions()
}, 500)

const fetchSuggestions = () => {
      suggestions.value = []
      isLoading.value = true
      isDropdownVisible.value = true
      pages.value = 1
      HighlightService.getSearchResults(subreddits.value, searchQuery.value, timeFilter.value, sortedByFilter.value)
      .then((response) => {
          suggestions.value = response.data['search_results'];
          isLoading.value = false
      })
      .catch((error) => { 
          console.log(error);
          isLoading.value = false
      });
    }

const onInput = () => {
  if (searchQuery.value.trim() === '') {
        suggestions.value = [];
        isDropdownVisible.value = false
      }
  else {
    isDropdownVisible.value = true
    debouncedWatch()
  }
}

watch(searchQuery, onInput);

const handleClickOutside = (event) => {
  if (dropdown.value && !dropdown.value.contains(event.target) 
    && !input.value.contains(event.target) 
    && !filterBtn.value.contains(event.target)
    && !modal.value.contains(event.target)) {
    isDropdownVisible.value = false;
  }
};

const handleInputFocus = () => {
  if (searchQuery.value.trim() !== '') {
    isDropdownVisible.value = true;
  }
};

const handleOpen = (data) => {
  isDropdownVisible.value = false;

  // Find the index of the suggestion in the array
  const index = suggestions.value.findIndex(suggestion => {
    return suggestion.id === data.id; // Assuming each suggestion has a unique 'id' property
  });

  // If found, remove it from its current position
  if (index !== -1) {
    suggestions.value.splice(index, 1);
  }

  // Add the suggestion to the beginning of the array
  suggestions.value.unshift(data);

  store.setHighlights(suggestions.value);
}

const handleSeeMore = () => {
  if ( pages.value * 5 === suggestions.value.length) {
  isDropdownVisible.value = false 
  store.setHighlights(suggestions.value);
  }
  else {
    pages.value += 1
  }
}

onMounted(() => {
  window.addEventListener('click', handleClickOutside);
});

onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside);
  debouncedWatch.cancel();
});

const openModal = () => {
  store.setModal(true)
}

const updateFilters = (data) => {
  timeFilter.value = data.time
  sortedByFilter.value = data.sort
  subreddits.value = data.subreddit
  subredditIcon.value = data.icon
  if (searchQuery.value) {
    debouncedWatch()
  }
}

const viewMore = computed(() => {
  return pages.value * 5 === suggestions.value.length ? 'View all' : 'Show more results'
})

const tagText = computed(() => {
  if (subreddits.value.length > 1) {
    return `r/${subreddits.value[0].subreddit} & ${subreddits.value.length - 1} more`
  }
  else {
    return `r/${subreddits.value[0].subreddit}`
  }
})

</script>

<template>
  <div class="main-container">
    <div class="search-bar-container">
      <div class="search-bar-container-inner">
        <img class="search-icon" :src="searchIcon" alt="">
        <img class="back-icon" :src="backIcon" alt="">
        <div class="search-tag-container" v-if="subreddits != 'soccer'">
          <div class="search-tag-inner">
            <img v-if="subreddits[0].icon" :src="subreddits[0].icon" alt="">
            <span>{{ tagText }}</span>
          </div>
        </div>
        <input
        ref="input"
        type="text"
        v-model="searchQuery"
        placeholder="Search Highlights"
        @focus="handleInputFocus"
        />
        <div class="filter-container" ref="modal">
          <img class="filter-icon" :src="filterIcon" alt="" @click="openModal" ref="filterBtn">
          <Modal :subreddit="subreddits" @applied-filter="updateFilters"/>
        </div>
      </div>
    </div>
    
    <div ref="dropdown" v-if="isDropdownVisible" class="dropdown">
      <ul >
        <li v-if="!suggestions.length" class="loading-dropdown">
          <div class="loading-container">
            <img v-show="!isLoading" class="search-icon" :src="searchIcon" alt="">
            <span v-show="!isLoading" class="query">{{ searchQuery }}</span>
            <transition name="loading">
              <div class="flex" v-show="isLoading" >
                <span class="query">{{ isLoading ? 'Searching for ' : '' }} "<span class="bold">{{ searchQuery }}</span></span>
                <Loader v-if="isLoading" :style="'small'"/>
              </div>  
            </transition>
          </div>
        </li>
        <SearchSuggestion 
          @opened-suggestion="handleOpen" 
          v-for="suggestion in suggestions.slice(0, 5 * pages)" 
          :key="suggestion.id" 
          :suggestion="suggestion"
        />
        <div class="see-all-container">
          <span 
            class="see-all" 
            v-if="suggestions.length > 5"
            @click="handleSeeMore">
            {{ viewMore }}
          </span>
        </div>  
      </ul>
    </div>
  </div>
</template>

<style scoped>
.flex {
  display: flex;
  align-items: center;
}
.main-container {
  flex-grow: 1;
  z-index: 900;
}
.search-bar-container {
background-color: var(--color-background);
position: relative;
padding: 0.4rem 0.6rem;
width: 100%;
border-radius: 30px;
border: 2px solid var(--color-border);
}
.search-bar-container:focus-within {
  border: 2px solid rgb(0, 119, 255);
}
.search-bar-container-inner {
display: flex;
align-items: center;
background-color: var(--color-background);
z-index: 990;
}
.search-icon, .back-icon {
  height: 20px;
  width: 20px;
  margin-right: 0.4rem;
}
.back-icon {
  display: none;
}
.query {
  margin-right: 0.5rem;
}
input {
  background-color: var(--color-background);
  width: 100%;
  border: none;
  outline: none;
  color: var(--color-text);
}
.filter-icon {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
}
.filter-container {
  border-radius: 10px;
  margin-left: 1rem;
  display: flex;
  align-items: center;
  padding: 0.2rem;
}
.filter-container span {
  font-weight: 600;
  margin-right: 0.1rem;
  
}
.filter-container:hover {
  background-color: var(--color-background-mute);
}
.filter-icon:hover {
  cursor: pointer;
}
.filter-legend {
  display: flex;
  padding-left: 1.5rem;
}
#filter-dropdown {
  z-index: -999;
}
.filter-dropdown-inner {
  display: flex;
}
.filter-dropdown-inner span {
  font-size: smaller;
  font-weight: 600;
}
li {
  text-align: left;
  font-weight: 500;
}
li span {
  cursor: pointer;
}
.dropdown {
position: absolute;
width: 100%;
background-color: var(--color-background);
z-index: 990;
margin-top: 1rem;
max-height: 55vh;
overflow-y: scroll;
border-radius: 10px;
/* Box shadow styling */
box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); /* horizontal offset, vertical offset, blur radius, spread radius, color */
-webkit-box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); /* For Safari */
-moz-box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); /* For old Firefox versions */
}
:root.dark .dropdown {
  background-color: var(--color-background-soft);
}
.loading-dropdown {
  padding: 1rem;
}
ul {
padding: 0;
list-style-type: none;
}
.filter-dropdown-inner ul {
  padding: 0.5rem 1.75rem;
}
.filter-dropdown-inner li {
  display: flex;
}

.filter-dropdown-inner img {
  width: 15px;
  height: 15px;
}
.loading-container {
display: flex;
flex: 1;
justify-content: flex-start;
align-items: center;
}
/* Transitions styling */
.loading-enter-active, .loading-leave-active {
  transition: opacity 0.3s;
}
.loading-enter-from, .loading-leave-to {
  opacity: 0;
}
.loading-enter-to, .loading-leave-from {
  opacity: 1;
 
}
.bold {
  color: var(--color-heading);
  font-weight: 600;
}
.search-tag-container {
  display: flex;
  align-items: center;
  background-color: var(--color-background-mute);
  border-radius: 20px;
  padding: 0.1rem 0.45rem;
}
.search-tag-inner {
  display: flex;
  align-items: center;
}
.search-tag-container span{
  font-size: smaller;
  margin-right: 0.4rem;
}


.search-tag-container img {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  margin-right: 4px;
}

.search-bar-container .cross-icon {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  margin-right: 4px;
  border: 1px solid grey;
  padding: 0.01rem;
}
.search-bar-container .cross-icon:hover {
 cursor: pointer;
}
.see-all-container {
  display: flex;
  align-items: center;
  justify-content: center;
}
.see-all {
  font-weight: 500;
  text-align: center;
  color: cornflowerblue;
  margin: 0.5rem 0
}
.see-all:hover {
  cursor: pointer;
  
}
@media (max-width: 385px) {
  .container-inner .flex img {
    display: none;
  }
}
</style>
