<script setup>
import { computed } from 'vue';
import { ref } from 'vue';
import { useHighlightsStore } from '@/stores/highlights';

const store = useHighlightsStore()

const props = defineProps({
  highlight: {
    type: Object,
    required: true
  }
})

const isTitleTruncated = ref(true);

const maxTitleLength = 75;  // Define the maximum length of the title before truncating

const displayedTitle = computed(() => {
  if (isTitleTruncated.value && props.highlight.title.length > maxTitleLength) {
    return `${props.highlight.title.substring(0, maxTitleLength)}...`;
  }
  return props.highlight.title;
});

function toggleTitleTruncate() {
  isTitleTruncated.value = !isTitleTruncated.value;
}

const updateState = () => {
  store.setSubreddit(props.highlight.subreddit)
  store.setSubredditImg(props.highlight.community_icon)
  store.setSubredditDisplayText(props.highlight.subreddit)
  store.endpoint('highlightsSubreddit')
}
</script>

<template>
  <div class="video-metadata">
    <div class="header">
      <div>
        <p class="date">{{ highlight.date }}</p>
        <span class="title">{{ displayedTitle }}</span>
        <span v-if="highlight.nsfw" class="nsfw-tag">nsfw</span>
        <button class="see-more-btn" v-if="highlight.title.length > maxTitleLength" @click="toggleTitleTruncate">
          {{ isTitleTruncated ? 'See More' : 'See Less' }}
        </button>
      </div>
    </div>
    <div>
    <RouterLink :to="{ name: 'profile', params: { redditor: highlight.author} }">
      <p class="author">{{ highlight.author }}</p>
    </RouterLink>

    <div class="subreddit-tag" v-if="highlight.subreddit">
      <RouterLink 
        @click="updateState"
        :to="{ name: 'highlightsSubreddit', 
        params: { subreddit: highlight.subreddit}}">
        <img class="community-icon" :src="highlight.community_icon" alt="">
        r/{{ highlight.subreddit }}
      </RouterLink>
    </div>

    </div>
  </div>
</template>

<style scoped>
a {
  text-decoration: none;
}
p {
  margin: 0;
}
.header {
    display: flex;
}
.title {
  color: white;
}
.author, .date {
  font-size: smaller;
  color: gainsboro;
}
.author:hover {
  color: rgb(244, 244, 244);
}
.subreddit-tag {
    display: flex;
    align-items: center;
    width: fit-content;
    border: 1px solid white;
    border-radius: 20px;
    padding: 0.2rem 0.4rem;
    margin-top: 0.5rem;
}
.subreddit-tag:hover {
  background-color: rgba(148, 159, 169, 0.367);
}
.subreddit-tag a {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: white    
}
.community-icon {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    margin-right: 0.3rem;
}
.see-more-btn {
  color: gainsboro;
  background-color: transparent;
  border: none;
  padding: 0;
}
.nsfw-tag {
  border: 1px solid rgb(255, 88, 91);
  color: rgb(255, 88, 91);
  padding: 0.05rem 0.2rem;
  border-radius: 5px;
  margin-left: 0.25rem;
}
</style>