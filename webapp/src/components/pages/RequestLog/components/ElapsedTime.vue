<script setup lang="ts">
import useElapsedTimer from '@/composables/useElapsedTimer'
import { computed, ref, watch } from 'vue'
import type { NullableNumber } from '@/types/Nullable'

type Props = {
  startTimestamp: number
  endTimestamp: NullableNumber
}

const props = withDefaults(defineProps<Props>(), {
  endTimestamp: null
})

const endTimestampRef = ref(props.endTimestamp)
watch(
  () => props.endTimestamp,
  (value) => {
    endTimestampRef.value = value
  }
)

const { diff } = useElapsedTimer(props.startTimestamp, endTimestampRef)

const diffFormattedSeconds = computed(() => {
  return diff.value.toFixed(1)
})
const diffFormattedMilliseconds = computed(() => {
  return (diff.value * 1000).toFixed(0)
})
</script>

<template>
  <span class="font-monospace">
    <span v-if="diff < 2.0">{{ diffFormattedMilliseconds }}ms</span>
    <span v-else>{{ diffFormattedSeconds }}s&nbsp;</span>
  </span>
</template>

<style scoped></style>