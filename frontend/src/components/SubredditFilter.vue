<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import SubredditCard from '../components/SubredditCard.vue';
import Arrow from '@/assets/icons/arrow-down.svg';
import PremIcon from '@/assets/icons/prem-logo2.png'
import LaLigaIcon from '@/assets/icons/la-liga-logo.jpeg'
import BundesligaLogo from '@/assets/icons/bundesliga-logo.png'
import SerieALogo from '@/assets/icons/serie-a-logo.png'
import Ligue1Logo from '@/assets/icons/ligue-1-logo.png'
import eflLogo from '@/assets/icons/efl-logo.png'
import mlsLogo from '@/assets/icons/mls-logo.gif'
import eredivisieLogo from '@/assets/icons/eredivisie.png'
import soccerIcon from '@/assets/icons/soccer-icon.png'
import { useRoute } from 'vue-router';
import HighlightService from '../services/HighlightService';
import Utils from '../services/Utils';

const categories = [
  { category: 'soccer', endpoint: 'highlightsSubreddit', text: 'All', img_url: soccerIcon },
  { category: 'PremierLeague', endpoint: 'highlightsLeague', text: 'Premier League', img_url: PremIcon },
  { category: 'LaLiga', endpoint: 'highlightsLeague', text: 'La Liga', img_url: LaLigaIcon },
  { category: 'Bundesliga', endpoint: 'highlightsLeague', text: 'Bundesliga', img_url: BundesligaLogo },
  { category: 'SerieA', endpoint: 'highlightsLeague', text: 'Serie A', img_url: SerieALogo },
  { category: 'Ligue1', endpoint: 'highlightsLeague', text: 'Ligue 1', img_url: Ligue1Logo },
  { category: 'Eredivisie', endpoint: 'highlightsLeague', text: 'Eredivisie', img_url: eredivisieLogo },
  { category: 'EFL', endpoint: 'highlightsLeague', text: 'Championship', img_url: eflLogo },
  { category: 'MLS', endpoint: 'highlightsLeague', text: 'MLS', img_url: mlsLogo },
];

const route = useRoute()
const showOptions = ref(false)
const container = ref(null)
const imgUrl= ref(soccerIcon)

const toggleOptions = () => {
    showOptions.value = !showOptions.value
}

const updateimg = () => { 
  const subreddit = route.params.subreddit
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

watch(() => route.params.subreddit, updateimg);

const handleClickOutside = (event) => {
  if (container.value && !container.value.contains(event.target)) {
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
<div @click="toggleOptions" ref="container" :class="{ 'container-active': showOptions, 'container': !showOptions }">
    <div class="container-inner">
        <div class="flex">
            <img v-show="imgUrl" :src="imgUrl" alt="">
            <span>{{ route.params.subreddit || 'soccer' }}</span>
        </div>
        <div class="arrow-container">
          <img :src="Arrow" alt="">
        </div>
       
    </div>
    <div v-show="showOptions" class="options">
      <ul>
          <li class="legend">
              <span>Browse Highlights</span>
          </li>
          <SubredditCard 
          v-for="category in categories" 
          :key="category.name"
          :category="category"
          />
      </ul>
    </div>
</div>
</template>
<style scoped>
.container, .container-active {
    position: relative;
    width: 100%;
    min-width: 11.5rem;
    max-width: 15rem;
    border: 1px solid var(--color-border);
    border-radius: 10px;
}

.container-active {
  margin-right: 1rem;
  border-radius: 0px;
  border-bottom: none;
  border-top-right-radius: 10px;
  border-top-left-radius: 10px;
  border: 1px solid var(--color-border-strong);
}

.container, .container-active:hover {
  cursor: pointer;
}
.container:hover {
  border: 1px solid var(--color-border-strong);
}

.container-inner{ 
   display: flex;
   align-items: center;
   padding: 0.5rem 1rem;
   height: 100%;
}
.arrow-container {
  width: 100%;
  text-align: right;
}
.flex {
    display: flex;
    align-items: center;
}
.container-inner .flex img {
  height: 20px;
  width: 20px;
  margin-right: 0.5rem;
  object-fit: contain;
}
span {
  color: var(--color-heading);
  font-weight: 600;
}
.options {
  background-color: var(--color-background);
  position: absolute;
  width: 101%;
  border: 1px solid var(--color-border-strong);
  border-top: none;
  z-index: 999;
  left: -1px;
  border-bottom-right-radius: 10px;
  border-bottom-left-radius: 10px;
}
:root.dark .options {
  background-color: var(--color-background-mute);
}
.legend {
    padding: 0.5rem 1rem;
    text-align: left;
}
.options span {
    color: var(--color-text);
    font-size: smaller;
    text-align: left;
}
ul {
list-style-type: none;
padding: 0;
}
img {
  height: 10px;
  width: 10px;;
}
@media (max-width: 385px) {
  .container-inner .flex img {
    display: none;
  }
}
</style>

