<script setup>

defineProps({
    tag: {
        type: Object,
        required: true
    }
})
</script>

<template>
    <div class="container">
        <div class="inner">
            <span>{{ tag.subreddit }}</span>
            <span>X</span>
        </div>
    </div>
</template>

<style scoped>
.container {
  display: flex;
  align-items: center;
  background-color: var(--color-background-mute);
  border-radius: 20px;
  padding: 0.1rem 0.45rem;
}
.inner {
  display: flex;
  align-items: center;
}
.container span{
  font-size: smaller;
  margin-right: 0.4rem;
}


.container img {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  margin-right: 8px;
}
</style>