<script setup>
import { TrendingUpIcon } from 'lucide-vue-next';

const props = defineProps({
    activeLeague: {
        type: Object,
        required: true
    }
})

const value = defineModel()

const items = [
    { value: "best", label: "Best" },
    { value: "top", label: "Top" },
    { value: "new", label: "Newest" },
    { value: "hot", label: "Hot" },
]
</script>

<template>
    <UiSelect v-model:model-value="value">
        <UiSelectTrigger class="w-[120px] border-gray-800 bg-gray-900 text-white">
            <TrendingUpIcon class="h-4 w-4" :class="activeLeague.color" />
            <UiSelectValue placeholder="Time" />
        </UiSelectTrigger>
        <UiSelectContent class="bg-gray-900 text-white border-none">
            <UiSelectGroup>
                <UiSelectItem class="focus:bg-gray-800 focus:text-white" v-model="value" v-for="item in items" :key="item.value" :value="item.value">
                    {{ item.label }}
                </UiSelectItem>
            </UiSelectGroup>
        </UiSelectContent>
    </UiSelect>
</template>