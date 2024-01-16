<script setup>
import CheckIcon from '@/assets/icons/check-icon.svg';
import crossIcon from '@/assets/icons/cross.svg';
import { useHighlightsStore } from '@/stores/highlights';
import { storeToRefs } from 'pinia';
import { ref, watch, computed } from 'vue';
import debounce from 'lodash.debounce';
import SubredditSuggestion from '../components/SubredditSuggestion.vue';
import SearchTag from '../components/SearchTag.vue';
import Loader from '../components/Loader.vue';
import HighlightService from '../services/HighlightService';

defineProps({
  subreddit: {
    type: String,
    required: true
  }
})
  
const store = useHighlightsStore()
const timeFilter  = ref('all')
const sortedByFilter = ref('top')
const subredditFilter = ref([{'subreddit': 'soccer', 'icon': 'https://styles.redditmedia.com/t5_2qi58/styles/communityIcon_fihq6rzyq7q91.png?width=256&s=3497aeefc618e652e94ba8b3e6b3318e213d0b55'}])
const { isModalShowing } = storeToRefs(store)  
const modalContent = ref(null)
const searchQuery = ref('')
const suggestions = ref([])
const isDropdownVisible = ref(false)
const isLoading = ref(null)

const setTimeFilter = (value) => {
  timeFilter.value = value
}

const setSortFilter = (value) => {
  sortedByFilter.value = value
}

const setSubredditFilter = (subredditData) => {
  subredditFilter.value.push(subredditData)
  searchQuery.value = ''
}

const emit = defineEmits(['appliedFilter'])

const applyFilter = () => {
  emit('appliedFilter', {
    'sort': sortedByFilter.value, 
    'time': timeFilter.value,
    'subreddit': subredditFilter.value
  })
  store.setModal(false)
}

const removeTag = (subreddit) => {
  subredditFilter.value = subredditFilter.value.filter(item => item !== subreddit);
  console.log(subredditFilter.value)
}

const debouncedWatch = debounce(() => {
  fetchSuggestions()
}, 500)

const fetchSuggestions = () => {
      suggestions.value = []
      isLoading.value = true
      isDropdownVisible.value = true
      HighlightService.getSubreddits(searchQuery.value)
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

</script>
<template>
  <transition name="fade">
    <div class="modal" v-if="isModalShowing">
      <div class="modal-content" ref="modalContent">
        <div class="header">
          <h3>Search Filters</h3>
          <img class="icon" :src="crossIcon" @click="store.setModal(false)">
        </div>
      
        <!-- Your filter content here -->
      <div ref="filters" class="dropdown" id="filter-dropdown">
  
      <div class="filter-dropdown-inner">
        <ul>
          <span class="legend">Upload Date</span>
          <li>
            <span @click="setTimeFilter('day')">Today</span>
            <img :src="CheckIcon" alt="" v-if="timeFilter==='day'">
          </li>
          <li>
            <span @click="setTimeFilter('week')">This week</span>
            <img :src="CheckIcon" alt="" v-if="timeFilter==='week'">
          </li>
          <li>
            <span @click="setTimeFilter('month')">This month</span>
            <img :src="CheckIcon" alt="" v-if="timeFilter==='month'">
          </li>
          <li>
            <span @click="setTimeFilter('year')">This year</span>
            <img :src="CheckIcon" alt="" v-if="timeFilter==='year'">
          </li>
          <li>
            <span @click="setTimeFilter('all')">All time</span>
            <img :src="CheckIcon" alt="" v-if="timeFilter==='all'">
          </li>
        </ul>
        
        <ul>
          <span class="legend">Sort By</span>
          <li>
            <span @click="setSortFilter('relevance')">Relevance</span>
            <img :src="CheckIcon" alt="" v-if="sortedByFilter==='relevance'">
          </li>
          <li>
            <span @click="setSortFilter('top')">Top</span>
            <img :src="CheckIcon" alt="" v-if="sortedByFilter==='top'">
          </li>
          <li>
            <span @click="setSortFilter('new')">Newest</span>
            <img :src="CheckIcon" alt="" v-if="sortedByFilter==='new'">
          </li>
        </ul>

        <ul>
          <span class="legend">Subreddits from</span>
          <div class="search-container">
            <div v-if="subreddit" class="subreddit-tags">
              <div v-for="tag in subredditFilter" class="search-tag-container">
                <div class="search-tag-inner">
                  <span>{{ tag.subreddit }}</span>
                  <span class="remove-tag" @click="removeTag(tag)">X</span>
                </div>
              </div>
            </div>
            <input
              ref="input"
              type="text"
              v-model="searchQuery"
              placeholder="subreddit name"
              @focus="handleInputFocus"
            />
            <div v-if="isLoading">
              <Loader :style="'small'" />
            </div>
          </div>
      
          <div class="subreddit-dropdown" v-if="isDropdownVisible">
            <SubredditSuggestion 
              v-for="suggestion in suggestions" 
              :key="suggestion.id" 
              :suggestion="suggestion" 
              @click="setSubredditFilter({'subreddit': suggestion.subreddit, 'icon': suggestion.community_icon})"
            />
          </div>
        </ul>
      </div>
    </div>
    <div class="btn-container">
      <button class="apply-btn" @click="applyFilter">Apply</button>
    </div>
      </div>
    </div>
  </transition>
</template>

<style scoped>
ul {
list-style-type: none;
padding: 2rem;
}
h3 {
  margin: 0;
  padding: 0;
  font-weight: 600;
}
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}
  
.modal-content {
  min-width: 40rem;
  border-radius: 10px;
  background-color: var(--color-background-mute);
  /* Add more styles as needed */
}
img {
width: 1rem;
height: 1rem;
border-radius: 50%;
margin-left: 0.25rem;
}
.icon {
width: 2rem;
height: 2rem;
border-radius: 50%;
margin-left: 0.25rem;
padding: 0.25rem;
}
.filter-container {
  border-radius: 10px;
  margin-left: 1rem;
  display: flex;
  align-items: center;
}
.filter-container:hover {
  cursor: pointer;
  background-color: var(--color-background-mute);
}
.header {
  display: flex;
  justify-content: space-between;
  padding: 1.5rem 2rem 0rem 2rem;
}
#filter-dropdown {
  z-index: -999;
}
.filter-dropdown-inner {
  display: flex;
}
li {
  text-align: left;
  display: flex;
  align-items: center;
}
.legend {
  color: var(--color-heading);
  font-weight: 600;
}
.btn-container {
  padding: 0 2rem 1rem 1rem;
  display: flex;
  justify-content: flex-end;
}
.apply-btn { 
  padding: 0.5rem 1rem;
  border-radius: 5px;
  background-color: var(--color-background);
  font-weight: 600;
  color: var(--color-text);
}
.apply-btn:hover {
  background-color: rgb(246, 246, 246);
  cursor: pointer;
}
img:hover {
  cursor: pointer;
  background-color: var(--color-background-mute);
}
li span:hover {
  cursor: pointer;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.fade-enter-to, .fade-leave-from {
  opacity: 1;
}
/* stuff for subreddit filter */
.search-container {
  background-color: var(--color-background);
  padding: 0.5rem 1rem;
  max-width: 20rem;
  border-radius: 10px;
  border: 2px solid var(--color-border);
}
input {
width: 100%;
border: none;
outline: none;
background-color: var(--color-background);
color: var(--color-text);
}
.subreddit-dropdown {
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
.subreddit-tags {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
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
.remove-tag:hover {
  cursor: pointer;
}
</style>
  