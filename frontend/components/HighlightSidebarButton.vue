<template>
    <div class="flex flex-col items-center justify-center gap-1">
        <UiButton
            :class="`bg-gray-900 text-white size-12 hover:bg-gray-800 font-medium rounded-full text-sm px-5 py-5 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700`"
            @click="$emit('click')">
            <slot name="icon" />
        </UiButton>
        <span class="text-white text-xs">
            <slot name="text"></slot>
        </span>
    </div>
</template>