<script setup lang="ts">
import { computed } from 'vue'
import { getDownloadUrlPrefix } from '@/helpers/EnvironmentHelper'
import type { RequestLogBody } from '@/types/RequestLog'
import { isNotUndefined, isNullOrUndefined } from '@/helpers/ConditionHelper'
import type { Optional } from '@/types/Optional'

type Props = {
  body: Optional<RequestLogBody>
}

const props = defineProps<Props>()

const mimeTypeRefExtension: Record<string, string> = {
  'application/json': 'json',
  'application/xml': 'xml',
  'text/plain': 'txt'
}

const downloadUrl = computed(() => {
  let url = getDownloadUrlPrefix() + '/' + props.body?.hash
  if (isNullOrUndefined(props.body?.mimeType)) {
    return url
  }
  const extension = mimeTypeRefExtension[props.body?.mimeType ?? ''] ?? null
  if (extension) {
    url += '.' + extension
  }
  return url
})
</script>

<template>
  <a
    :href="downloadUrl"
    target="_blank"
    class="btn btn-sm btn-outline-primary me-2"
    v-if="isNotUndefined(body?.hash)"
    title="Download original content"
  >
    <span class="bi bi-download" />
  </a>
</template>

<style scoped></style>