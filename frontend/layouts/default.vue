<script setup lang="ts">
</script>
<template>
    <div class="min-h-screen relative bg-gray-950">
        <!-- Header -->
        <BackgroundGradient />
        <div class="sticky top-0 bg-gray-950 z-40">
            <NavBar />
            <LeagueFilter />
        </div>
        <!-- Main content -->
        <slot />
    </div>
</template>