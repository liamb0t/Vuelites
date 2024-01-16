<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router';
import { useHighlightsStore } from '@/stores/highlights';

defineProps({
    subreddit: {
        type: Object, 
        required: true
    }
})

const store = useHighlightsStore()

</script>

<template>
    <RouterLink @click="store.setSubreddit(subreddit.name)" :to="{ name: subreddit.endpoint, params: { subreddit: subreddit.name} }">
        <div class="container">
            <div class="img-container">
                <img :src="subreddit.img_url" alt="">
            </div>
            <div class="footer">
                <p>{{ subreddit.text }}</p>
                <p>253{{ subreddit.num_subscribers }}k subscribers</p>
            </div>
        </div>
    </RouterLink>
</template>
<style scoped>  
.container {
    width: 10rem;
}
.img-container {
    width: 4rem;
}
img {
    width: 100%;
}
</style>