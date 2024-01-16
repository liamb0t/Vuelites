<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
    comment: {
        type: Object,
        required: true
    }
})
const isCommentTruncated = ref(true);

const maxCommentLength = 125;  // Define the maximum length of the title before truncating

const displayedBody = computed(() => {
  if (isCommentTruncated.value && props.comment.body.length > maxCommentLength) {
    return `${props.comment.body.substring(0, maxCommentLength)}...`;
  }
  return props.comment.body;
});

function toggleCommentTruncate() {
  isCommentTruncated.value = !isCommentTruncated.value;
}
</script>

<template>
    <div class="comment-card">
      <div class="header">
        <span class="author">{{ comment.author }}</span>
        <span class="date">{{ comment.date }}</span>
      </div>
   
      <span class="body">{{ displayedBody }}</span>
      <button class="see-more-btn" v-if="comment.body.length > maxCommentLength" @click="toggleCommentTruncate">
        {{ isCommentTruncated ? 'See More' : 'See Less' }}
      </button>
      <div class="comment-likes">
        <img class="thumbs-icon" src="@/assets/icons/thumbs-up.svg" alt="">
        <span class="score">{{ comment.ups }}</span>
      </div>
    </div>
</template>
<style scoped>  

.comment-card {
  margin-bottom: 1rem;
  padding-right: 1rem;
}
.author {
  color: var(--color-heading);
  margin-right: 0.4rem;
  font-weight: 600;
}
.date {
  font-size: smaller;
}
.body {
  color: var(--color-heading);
}
.see-more-btn {
  color: gainsboro;
  background-color: transparent;
  border: none;
  padding: 0;
}
.comment-likes {
  margin-top: 0.4rem;
  display: flex;
  align-items: center;
}
.thumbs-icon {
  height: 20px;
  width: 20px;
  margin-right: 0.2rem;
}
.score {
  font-size: smaller;
}
</style>