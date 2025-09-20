<script setup>

const open = defineModel()
const loading = ref(true)

const props = defineProps({
    highlight: {
        type: Object,
        required: true
    },
    activeLeague: {
        type: Object,
        required: true
    },
})
const emit = defineEmits(['toggleComments', 'updateSortedBy', 'fetchComments'])

const comments = ref(null)

const fetchComments = async () => {
    loading.value = true
    comments.value = await useFetch(`/api/comments/${props.highlight.id}/'top'`, {
        method: 'GET',
    }).then((res) => {
        return res.data.value.comments
    }).catch((err) => {
        console.error(err)
        return null
    }).finally(() => {
        loading.value = false
    })
}

watchEffect(async () => {
    if (open.value && !comments.value) {
        await fetchComments()
    }
})
</script>
<template>
    <UiDialog v-model:open="open">
        <UiDialogContent
            class="sm:max-w-[425px] border-1 bg-gray-950/10 backdrop-blur-2xl text-white grid-rows-[auto_minmax(0,1fr)_auto] p-0 max-h-[90dvh]"
            :class="activeLeague.borderColor">
            <UiDialogHeader class="p-6 pb-0">
                <UiDialogTitle>Comments</UiDialogTitle>
            </UiDialogHeader>
            <div class="overflow-y-auto px-6">
                <div v-if="loading" class="gap-y-4 flex flex-col">
                    <div v-for="n in 8" :key="n" class="flex items-center space-x-4">
                        <UiSkeleton class="h-12 w-12 rounded-full" />
                        <div class="space-y-2">
                            <UiSkeleton class="h-4 w-[250px]" />
                            <UiSkeleton class="h-4 w-[200px]" />
                        </div>
                    </div>
                </div>
                <div v-else>
                    <CommentCard v-for="comment in comments" :key="comment.id" :comment="comment" />
                </div>
            </div>
        </UiDialogContent>
    </UiDialog>
</template>