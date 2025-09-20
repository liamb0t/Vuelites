<script setup>
import { Trophy } from 'lucide-vue-next';
import { AnimatePresence, Motion } from 'motion-v'

const props = defineProps({
    activeLeague: {
        type: Object,
        required: true
    },
})
</script>

<template>
    <div class="fixed inset-0 top-[120px] flex items-center justify-center z-30">
        <div class="relative w-[200px] h-[200px] p-4 flex gap-4 flex-col items-center justify-center">
            <AnimatePresence mode="wait">
                <Motion :key="activeLeague.id" :initial="{ opacity: 0 }" :animate="{ opacity: 1 }"
                    :exit="{ opacity: 0 }" :transition="{ duration: 0.1 }" class="flex items-center justify-center">
                    <img v-if="activeLeague.logo" class="size-32 rounded-lg object-cover" :src="activeLeague.logo" alt="">
                    <div v-else class="flex items-center justify-center gap-x-2">
                        <Trophy class="size-24 text-emerald-400" />
                    </div>
                </Motion>
            </AnimatePresence>
            <span class="main border-t-8" :class="activeLeague.borderColor" />
        </div>
    </div>
</template>

<style scoped>
.main {
    border-radius: 50%;
    width: 250px;
    height: 250px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    animation: spin 2s linear infinite;
}

@keyframes spin {
    0% {
        transform: translate(-50%, -50%) rotate(0deg);
    }

    100% {
        transform: translate(-50%, -50%) rotate(360deg);
    }
}

.small {
    width: 24px;
    height: 24px;
    border: 4px dotted #5a5a5a;
    border-radius: 50%;
    display: inline-block;
    position: relative;
    box-sizing: border-box;
    animation: rotation 2s linear infinite;
}

@keyframes rotation {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.fancy {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: block;
    margin: 15px auto;

    color: #a5a3a3;
    box-sizing: border-box;
    animation: animloader 2s linear infinite;
}

@keyframes animloader {
    0% {
        box-shadow: 14px 0 0 -2px, 38px 0 0 -2px, -14px 0 0 -2px, -38px 0 0 -2px;
    }

    25% {
        box-shadow: 14px 0 0 -2px, 38px 0 0 -2px, -14px 0 0 -2px, -38px 0 0 2px;
    }

    50% {
        box-shadow: 14px 0 0 -2px, 38px 0 0 -2px, -14px 0 0 2px, -38px 0 0 -2px;
    }

    75% {
        box-shadow: 14px 0 0 2px, 38px 0 0 -2px, -14px 0 0 -2px, -38px 0 0 -2px;
    }

    100% {
        box-shadow: 14px 0 0 -2px, 38px 0 0 2px, -14px 0 0 -2px, -38px 0 0 -2px;
    }
}
</style>
