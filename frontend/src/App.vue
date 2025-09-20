<script setup>
import { ref, onBeforeMount, onMounted, onUnmounted } from 'vue';
import SearchBar from './components/SearchBar.vue';
import SubredditFilter from './components/SubredditFilter.vue';
import HighlightFilter from './components/HighlightFilter.vue';
import { RouterLink, RouterView} from 'vue-router'
import menuIcon from '@/assets/icons/menu.svg';
import searchIcon from '@/assets/icons/search-icon.svg';
import backIcon from '@/assets/icons/back.svg';

let theme;
const isSearchBarOpen = ref(false);
const documentBody = document.documentElement.classList

function toggleTheme() {
  // Initialize theme to 'light' if it's undefined
  theme = theme === undefined ? 'light' : theme;
  // Toggle between 'light' and 'dark' classes
  theme === 'dark' ? theme = 'light' : theme = 'dark';
  documentBody.toggle('light', theme === 'light');
  documentBody.toggle('dark', theme === 'dark');
  localStorage.setItem('theme', theme);
}

function openSearchBar() {
  document.querySelector('.search-bar').style.display = 'flex'
  document.querySelector('.search-bar .search-icon').style.display = 'none'
  document.querySelector('.search-bar .back-icon').style.display = 'block'
  isSearchBarOpen.value = true;
}

function closeSearchBar() {
  document.querySelector('.search-bar').style.display = 'none'
  document.querySelector('.search-bar .search-icon').style.display = 'block'
  document.querySelector('.search-bar .back-icon').style.display = 'none'
  isSearchBarOpen.value = false;
}

onMounted(() => {
  document.querySelector('.search-bar .back-icon').addEventListener('click', function() {
    closeSearchBar()
  })
})

onBeforeMount(() => {
  theme = localStorage.getItem('theme');
  if (theme) {
    documentBody.toggle(theme, true);
  }
})

onUnmounted(() => {
  // Clean up back button event listener
  const backIcon = document.querySelector('.search-bar .back-icon');
  if (backIcon) {
    backIcon.removeEventListener('click', closeSearchBar);
  }
})
</script>

<template>
  <nav>
    <div class="nav-container">
      <div class="logo-container">
        <RouterLink to='/'>
            <div>
              <span class="logo">Vuelites</span>
            </div>  
        </RouterLink>
        <div class="nav-filters-container" v-show="!isSearchBarOpen">
          <div class="filters">
            <SubredditFilter />
            <HighlightFilter/>
            <div class="search-bar-icon-container" @click="openSearchBar" v-show="!isSearchBarOpen">
              <img class="search-icon" :src="searchIcon" alt="">
            </div>
          </div>
        </div>
        <div class="search-bar">
          <SearchBar />
        </div>
        <div class="color-theme-container">
          <label class="switch">
            <input type="checkbox"  @click="toggleTheme" :checked="theme==='dark'">
            <span class="slider round"></span>
          </label>
        </div>
      </div>
    </div>
  </nav>
  <RouterView />
</template>

<style scoped>
#layout {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
nav {
  top: 0;
  background-color: var(--color-background);
  position: sticky;
  margin-bottom: 2rem;
  padding-top: 1rem;
  padding-bottom: 1rem;
  z-index: 1000;
}
.logo-container {
  display: flex;
  align-items: center;
  white-space: nowrap;
  flex-wrap: nowrap;
}
.logo {
  color: var(--color-heading);
  font-weight: 700;
  font-size: 1.25rem;
}
.search-bar {
  display: none;
  position: relative;
  width: 100%;      /* Takes up 100% of available space */
  min-width: 25rem; /* Minimum width of 200 pixels */
  max-width: 36rem; /* Maximum width of 500 pixels */
}

.search-bar-icon-container {
  display: none;
  margin-top: 4px;
}
.search-icon {
  height: 20px;
  width: 20px;
  margin-right: 0.4rem;
}
.search-icon:hover {
  cursor: pointer;
}
.filters {
  display: flex;
  align-items: center;
}
nav a, .container, .button-container {
  margin-right: 1rem;
}

nav a {
  font-weight: bold;
  color: var(--color-text);
}

.logo-container img {
  width: 1.5rem;
  height: 1.5rem;
  margin-right: 0.5rem
}
.nav-filters-container, .color-theme-container, .search-bar-icon {
  flex-basis: 50%;
}
.color-theme-container {
  text-align: right;
}

.nav-filters-container {
  display: flex;
  align-items: center;
}

/* dark mode switch css */

/* The switch - the box around the slider */
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

/* Hide default HTML checkbox */
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

/* The slider */
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

.back-btn-container {
  cursor: pointer;
  display: block;
}

:root.dark input:checked + .slider {
  background-color: #2196F3;
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}


@media (min-width: 898px) {
  .search-bar {
    display: flex;
  }
}
@media (max-width: 966px) {
  .switch {
    display: none;
  }
}
@media (max-width: 898px) {
  .search-bar-icon-container {
    display: block;
  }
}

@media (max-width: 534px) {
  .logo-container {
    flex-direction: column;
  }
  #app {
    padding: 0;
  }
}
</style>

