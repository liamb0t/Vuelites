<script setup>

defineProps({
  profile: {
    type: Object,
    required: true
  }
})
</script>

<template>
    <div class="profile">
        <div class="head-container">
            <div class="avatar-container">
                <img class="avatar" :src="profile.avatar" alt="">
            </div>
         
            <div class="head">
                <div class="username-container">
                    <h2 class="username">{{ profile.username }}</h2>
                    <h4 class="username-handle">u/{{ profile.username }}</h4>
                </div>

                <div class="stats">
                    <div class="stat-container">
                        <p class="stat-name">Post Karma</p>
                        <p class="stat">{{ profile.link_karma }}</p>
                     
                    </div>
                    <div class="stat-container">
                        <p class="stat-name">Comment Karma</p>
                        <p class="stat">{{ profile.comment_karma }}</p>
                      
                    </div>
                    <div class="stat-container">
                        <p class="stat-name">Joined</p>
                        <p class="stat">{{ profile.joined }}</p>
                    
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<style scoped>
.profile {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 2rem;
}
.head-container {
    display: flex;
}
.avatar {
    width: 10rem;
    height: 10rem;
    border-radius: 20px;
    margin-right: 3rem;
}
.head {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.username {
    font-weight: 600;
}
.username-handle {
    font-weight: 500;
}
.main {
    color: rgb(94, 87, 87);
}
.handle {
    color: grey;
}
.stats {
    display: flex;
}
.stat-container {
    margin-right: 4rem;
}
.stat-name {
    font-weight: 500;
}
.stat {
    font-size: 0.75rem;
}
</style>