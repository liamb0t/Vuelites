<script setup>

const props = defineProps({
    suggestion: {
        type: Object,
        required: true
    }
})

// Define the emits
const emit = defineEmits(['openedSuggestion']);

const openedSuggestion = () => {
  emit('openedSuggestion', props.suggestion)
};

</script>

<template>
<li>
  <div class="suggestion-container" @click="openedSuggestion">
    <div class="info">
        <div class="header">
          <div class="img-container">
            <img v-if="suggestion.community_icon" class="subreddit-icon" :src="suggestion.community_icon" alt="">
          </div>
          <span class="subreddit">r/{{ suggestion.subreddit }}</span>
          <span class="bull">&bull;</span>
          <span class="subscribers"> {{ suggestion.subscribers }} subscribers</span>
        </div>
    </div>
  </div>
</li>
</template>

<style scoped>
.suggestion-container {
padding: 1rem;
display: flex;
align-items: flex-start;
width: 100%;
}
.suggestion-container:hover {
cursor: pointer;
background-color: var(--color-background-soft);
}
.info {
  flex: 1;
}
.header {
  font-size: smaller;
  display: flex;
  align-items: center;
}
.header img {
  width: 20px;
  height: 20px;
  margin-right: 0.4rem;
}
.bull {
  font-size: 10px;
  margin: 0 0.3rem;
}
.title {
text-align: justify;
font-weight: 600;
margin: 0.5rem 0;
margin-right: 1rem;
}

.footer {
  display: flex;
  align-items: center;
}
.img-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  margin-right: 0.25rem;
}
img {
  width: 20px;
  height: 20px;
  margin-right: 0.2rem;
  border-radius: 50%;
  object-fit: contain;
}
.comment-icon {
  margin-left: 0.4rem;
}

.video-container {
display: flex;
width: 6rem;
height: 80px;
justify-content: center;
align-items: center;
}
video {
object-fit: cover;
width: 100%;
height: 100%;
pointer-events: none;
border-radius: 10px;
}
.subreddit {
  font-weight: 500;
}
.subscribers {
  font-size: smaller;
}
</style>