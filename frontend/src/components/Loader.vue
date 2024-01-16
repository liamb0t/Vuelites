<script setup>

import { onMounted, ref, computed} from 'vue';
import { useRoute } from 'vue-router';

const props = defineProps({
    style: {
        type: String,
        required: true
    }
})

const route = useRoute()

const loaderStyle = computed(() => {
  if (props.style === 'main') {
    return `main ${route.params.subreddit}`
  }
  else {
    return props.style
  }
});
</script>

<template>
<span :class="loaderStyle">
</span>
</template>

<style scoped>
.large {
  position: absolute;
    width: 48px;
    height: 48px;
    border: 5px solid var(--color-background-mute);
    border-bottom-color: transparent;
    border-radius: 50%;
    display: inline-block;
    box-sizing: border-box;
    animation: rotation 1s linear infinite;
    }

    @keyframes rotation {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
} 
.main {
    border-radius: 50%;
    border-top: 8px solid #000;
    width: 100px;
    height: 100px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    animation: spin 2s linear infinite;
}

:root.dark .soccer {
  border-top: 8px solid #1d4169;
}

.undefined {
  border-top: 8px solid #1d4169;
}

.PremierLeague {
  border-top: 8px solid #872a85;
}

.Bundesliga {
  border-top: 8px solid #c61d1d;
}

.LaLiga {
  border-top: 8px solid orange;
}

.SerieA {
  border-top: 8px solid rgb(0, 145, 255);
}

.EFL {
  border-top: 8px solid rgb(4, 27, 85);
}
.MLS {
  border-top: 8px solid rgb(5, 103, 34);
}



@keyframes spin {
    0% { transform: translate(-50%, -50%) rotate(0deg); }
    100% { transform: translate(-50%, -50%) rotate(360deg); }
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
  margin:15px auto;
  
  color: #a5a3a3;
  box-sizing: border-box;
  animation: animloader 2s linear infinite;
}

@keyframes animloader {
  0% {
    box-shadow: 14px 0 0 -2px,  38px 0 0 -2px,  -14px 0 0 -2px,  -38px 0 0 -2px;
  }
  25% {
    box-shadow: 14px 0 0 -2px,  38px 0 0 -2px,  -14px 0 0 -2px,  -38px 0 0 2px;
  }
  50% {
    box-shadow: 14px 0 0 -2px,  38px 0 0 -2px,  -14px 0 0 2px,  -38px 0 0 -2px;
  }
  75% {
    box-shadow: 14px 0 0 2px,  38px 0 0 -2px,  -14px 0 0 -2px,  -38px 0 0 -2px;
  }
  100% {
    box-shadow: 14px 0 0 -2px,  38px 0 0 2px,  -14px 0 0 -2px,  -38px 0 0 -2px;
  }
}
</style>
