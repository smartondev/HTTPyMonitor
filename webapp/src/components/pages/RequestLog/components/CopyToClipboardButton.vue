<script setup lang="ts">

import {copyToClipboard} from "@/helpers/Clipboard";
import {isNotNullNorUndefined} from "@/helpers/ConditionHelper";

type Props = {
  title: string,
  content: string | undefined | null,
  tooltip?: string | null,
}

const props = withDefaults(defineProps<Props>(), {
  title: 'Copy to clipboard',
  content: null,
  tooltip: null,
});
</script>

<template>
  <button v-if="isNotNullNorUndefined(content)" class="btn btn-sm btn-outline-secondary me-2"
          @click="copyToClipboard(content)"
          :title="tooltip ?? undefined">
    <span class="bi bi-clipboard"/> {{ title }}
  </button>
</template>

<style scoped>

</style>