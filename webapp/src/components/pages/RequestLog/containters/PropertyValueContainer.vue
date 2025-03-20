<script setup lang="ts">
import type { NullableString } from '@/types/Nullable'

type Props = {
  title: string
  value?: NullableString
  truncateAllowed?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  value: '',
  truncateAllowed: false
})
</script>

<template>
  <div class="container-fluid mb-3 px-0 mx-0">
    <div class="row">
      <div class="col-auto">
        <span class="fs-6 fw-bold">{{ props.title }}</span>
      </div>
      <div class="col" :class="{ 'text-truncate': props.truncateAllowed }">
        <span class="font-monospace" v-if="props.value !== null">{{ props.value }}</span>
        <span v-else>-</span>
      </div>
    </div>
  </div>
</template>

<style scoped></style>