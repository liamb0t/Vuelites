<script setup>
import { RouterLink, useRoute } from 'vue-router'
import { useHighlightsStore } from '@/stores/highlights';

const store = useHighlightsStore()
const route = useRoute()

const props = defineProps({
    category: {
        type: String,
        required: true,
       
    },
})

const updateState = () => {
    store.setSubreddit(props.category.category)
    store.setSubredditImg(props.category.img_url)
    store.setSubredditDisplayText(props.category.text)
    store.setEndpoint(props.category.endpoint)
}
</script>

<template>
     <li>
        <RouterLink @click="updateState" 
            :to="{ 
                name: category.endpoint, 
                params: { subreddit: category.category},
                query: { time: route.query.time, sort: route.query.sort }  
            }">
            <div class="container">
                <div class="container-inner">
                    <img :src="category.img_url" alt="">
                    <span>{{ category.text }}</span>
                </div>
            </div>
        </RouterLink>
    </li>
</template>

<style scoped>
a {
    text-decoration: none;
}
a:visited {
    text-decoration: none;
    color: var(--color-text);
}
span {
    color: var(--color-heading);
    font-weight: 500;
}
.container {
    display: flex;
    padding: 0.75rem;
}
.container:hover {
    background-color: var(--color-background-soft);
}
.container-inner {
    display: flex;
    align-items: center;
}
img {
    width: 20px;
    height: 20px;
    margin-right: 0.5rem;
    object-fit: contain;
}
</style>