<script setup lang="ts">
import { isNotNullNorUndefined } from '@/helpers/ConditionHelper'
import type { OptionalString } from '@/types/Optional'
import type { MaybeString } from '@/types/Maybe'

type Props = {
  property?: OptionalString
  value: MaybeString
  variant?: string
}

const props = withDefaults(defineProps<Props>(), {
  property: undefined,
  value: null,
  variant: 'secondary'
})
</script>

<template>
  <div
    class="badge me-2 shadow-sm"
    :class="[`bg-${props.variant}`]"
    v-if="isNotNullNorUndefined(props.value)"
  >
    <span v-if="isNotNullNorUndefined(props.property)" class="fw-bold me-1"
      >{{ props.property }}:</span
    >
    <span class="text-nowrap">{{ props.value }}</span>
  </div>
</template>

<style scoped></style>