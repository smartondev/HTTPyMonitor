<script setup lang="ts">
import { computed } from 'vue'
import type { RequestLogUiList } from '@/types/RequestLogUi'
import LogPlace from './LogPlace.vue'
import type { RequestLog } from '@/types/RequestLog'

const models = defineModel<RequestLogUiList>({
  default: []
})

const stickyModels = computed<RequestLogUiList>(() => {
  return models.value.filter((model) => model.isSticky)
})
const nonStickyModels = computed<RequestLogUiList>(() => {
  return models.value.filter((model) => !model.isSticky)
})

const drop = function (item: RequestLog) {
  models.value = models.value.filter((model) => model.id !== item.id)
}

const hasStickyLogs = computed(() => {
  return stickyModels.value.length > 0
})
</script>

<template>
  <div>
    <LogPlace v-if="hasStickyLogs" :title="'Sticky logs'" :models="stickyModels" @drop="drop" />
    <LogPlace :title="'Request logs'" :models="nonStickyModels" @drop="drop" />
  </div>
</template>

<style scoped></style>