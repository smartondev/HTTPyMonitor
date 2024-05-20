<script setup lang="ts">

import {isNotNullNorUndefined} from "@/helpers/ConditionHelper";

type Props = {
  property?: string | undefined,
  value: string | null | undefined,
  variant?: string
}

const props = withDefaults(defineProps<Props>(), {
  property: undefined,
  value: null,
  variant: 'secondary'
})

</script>

<template>
  <div class="badge me-2 shadow-sm" :class="[`bg-${variant}`]" v-if="isNotNullNorUndefined(value)">
    <span v-if="isNotNullNorUndefined(property)" class="fw-bold me-1">{{ property }}:</span>
    <span class="text-nowrap">{{ value }}</span>
  </div>
</template>

<style scoped>

</style>