<script setup>
import { CalendarDaysIcon } from 'lucide-vue-next';

const props = defineProps({
    activeLeague: {
        type: Object,
        required: true
    }
})

const value = defineModel()

const items = [
    { value: "day", label: "Past Day" },
    { value: "week", label: "Past Week" },
    { value: "month", label: "Past Month" },
    { value: "year", label: "Past Year" },
    { value: "all", label: "All Time" },
]
</script>

<template>
    <UiSelect v-model:model-value="value">
        <UiSelectTrigger class="w-[150px] border-gray-800 bg-gray-900 text-white">
            <CalendarDaysIcon class="h-4 w-4" :class="activeLeague.color" />
            <UiSelectValue />
        </UiSelectTrigger>
        <UiSelectContent class="bg-gray-900 text-white border-none">
            <UiSelectGroup>
                <UiSelectItem class="focus:bg-gray-800 focus:text-white" v-model="value" v-for="item in items"
                    :key="item.value" :value="item.value">
                    {{ item.label }}
                </UiSelectItem>
            </UiSelectGroup>
        </UiSelectContent>
    </UiSelect>
</template>