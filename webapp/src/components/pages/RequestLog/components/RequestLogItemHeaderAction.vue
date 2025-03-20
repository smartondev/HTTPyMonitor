<script setup lang="ts">
import type { RequestLogUi } from '@/types/RequestLogUi'
import { computed } from 'vue'

const emits = defineEmits<{
  (e: 'toggle-sticky', model: RequestLogUi): void
  (e: 'drop', model: RequestLogUi): void
}>()

type Props = {
  model: RequestLogUi
  size?: string
}

const props = withDefaults(defineProps<Props>(), {
  model: () => ({}) as RequestLogUi
})

const clickToggleSticky = (): void => {
  emits('toggle-sticky', props.model)
}

const clickDrop = (): void => {
  emits('drop', props.model)
}

const iconClasses = computed<string[]>(() => {
  const classes = []
  if (props.model.isSticky) {
    classes.push('bi-pin-fill')
  } else {
    classes.push('bi-pin-angle')
  }
  return classes
})
</script>

<template>
  <div>
    <button type="button" @click="clickToggleSticky" class="btn btn-sm py-0">
      <i :class="iconClasses" />
    </button>
    <button type="button" @click="clickDrop" class="btn btn-sm py-0">
      <i class="bi-trash" />
    </button>
  </div>
</template>

<style scoped lang="scss">
@use 'bootstrap' as *;

@include media-breakpoint-down(lg) {
  .btn {
    font-size: 1.5rem;
  }
}
</style>
