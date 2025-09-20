<script setup lang="ts">
import { Trophy } from 'lucide-vue-next'

const props = defineProps({
  error: Object
})

const handleError = () => clearError({ redirect: '/' })
</script>

<template>
  <div class="min-h-screen bg-gray-950 text-white flex items-center justify-center">
    <div class="text-center max-w-md mx-auto px-4">
      <!-- 404 Icon -->
      <div class="mb-8">
        <Trophy class="size-24 text-gray-600 mx-auto mb-4" />
        <h1 class="text-8xl font-bold text-gray-400 mb-2">404</h1>
        <h2 class="text-2xl font-semibold text-gray-300 mb-4">Page Not Found</h2>
      </div>

      <!-- Error Message -->
      <p class="text-gray-400 mb-8 leading-relaxed">
        The highlight you're looking for has been moved to the bench. 
        Let's get you back to the action.
      </p>

      <!-- Action Buttons -->
      <div class="space-y-4">
        <button 
          @click="handleError"
          class="w-full px-6 py-3 bg-emerald-500 hover:bg-emerald-600 text-white font-medium rounded-lg transition-colors">
          Back to Home
        </button>
        <NuxtLink 
          to="/"
          class="block w-full px-6 py-3 bg-gray-800 hover:bg-gray-700 text-gray-300 font-medium rounded-lg transition-colors">
          Browse Highlights
        </NuxtLink>
      </div>

      <!-- Additional Info -->
      <div v-if="error" class="mt-8 p-4 bg-gray-900 rounded-lg">
        <p class="text-xs text-gray-500">
          Error {{ error.statusCode }}: {{ error.statusMessage }}
        </p>
      </div>
    </div>
  </div>
</template>