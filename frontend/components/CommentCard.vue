<script setup>
import { ThumbsUp } from 'lucide-vue-next'

const props = defineProps({
  comment: {
    type: Object,
    required: true
  }
})

const isCommentTruncated = ref(true)
const maxCommentLength = 125

const displayedBody = computed(() => {
  if (isCommentTruncated.value && props.comment.body.length > maxCommentLength) {
    return `${props.comment.body.substring(0, maxCommentLength)}...`
  }
  return props.comment.body
})

function toggleCommentTruncate() {
  isCommentTruncated.value = !isCommentTruncated.value
}
</script>
<template>
  <div class="mb-4 pr-4">
    <!-- Header -->
    <div class="flex items-center">
      <span class="text-heading font-semibold mr-2">{{ comment.author }}</span>
      <span class="text-sm text-gray-500">{{ comment.date }}</span>
    </div>

    <!-- Body -->
    <span class="text-heading block">{{ displayedBody }}</span>

    <!-- See More / Less Button -->
    <button v-if="comment.body.length > maxCommentLength" @click="toggleCommentTruncate"
      class="text-gray-400 bg-transparent border-none p-0 hover:underline mt-1">
      {{ isCommentTruncated ? 'See More' : 'See Less' }}
    </button>

    <!-- Likes -->
    <div class="flex items-center mt-2">
      <ThumbsUp alt="" class="h-5 w-5 mr-1" />
      <span class="text-sm text-heading">{{ comment.ups }}</span>
    </div>
  </div>
</template>
