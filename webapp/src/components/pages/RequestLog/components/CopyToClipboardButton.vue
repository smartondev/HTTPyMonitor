<script setup lang="ts">
import { isNotNullNorUndefined } from '@/helpers/ConditionHelper'
import useCopyToClipboard from '@/composables/useCopyToClipboard'
import type { OptionalString } from '@/types/Optional'
import type { MaybeString } from '@/types/Maybe'

type Props = {
  title?: MaybeString
  content: OptionalString
  tooltip?: OptionalString
}

const props = withDefaults(defineProps<Props>(), {
  title: undefined,
  tooltip: undefined
})
</script>

<template>
  <button
    v-if="isNotNullNorUndefined(content)"
    class="btn btn-sm btn-outline-secondary me-2"
    @click="useCopyToClipboard(content)"
    :title="props.tooltip"
  >
    <span class="bi bi-clipboard" /> {{ title }}
  </button>
</template>

<style scoped></style>
