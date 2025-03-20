<script setup lang="ts">
import type { RequestLogBody } from '@/types/RequestLog'
import useExpand from '@/composables/useExpand'
import { computed, defineProps } from 'vue'
import DownloadOriginalContentButton from '@/components/pages/RequestLog/components/DownloadOriginalContentButton.vue'
import CopyToClipboardButton from '@/components/pages/RequestLog/components/CopyToClipboardButton.vue'
import PlaceholderButton from '@/components/common/PlaceholderButton.vue'
import HttpBodyTabs from '@/components/pages/RequestLog/components/HttpBodyTabs.vue'
import type { Optional } from '@/types/Optional'

type Props = {
  body?: Optional<RequestLogBody>
  title: string
  placeholder?: boolean
  expanded?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  body: undefined,
  title: '',
  placeholder: false,
  expanded: false
})

const usePlaceholder = computed(() => {
  return props.placeholder && props.body === undefined
})

const { expandedState, toggleExpanded } = useExpand(props.expanded)

const show = computed(() => {
  const length = props.body?.length
  return length === undefined || length > 0 || (props.body === undefined && props.placeholder)
})
</script>

<template>
  <div class="container-fluid mb-3 px-0 mx-0 placeholder-glow" v-if="show">
    <div class="row">
      <div class="col cursor-pointer text-truncate" @click="toggleExpanded">
        <span class="fs-6 fw-bold me-2">{{ title }}</span>
        <span class="bi bi-caret-up-fill me-2" v-if="expandedState" />
        <span class="bi bi-caret-down-fill me-2" v-else />

        <span class="fs-80 fst-italic text-nowrap" v-if="body?.contentType"
          >( {{ body.contentType }} )</span
        >
        <span class="fs-80 w-25 placeholder" v-if="usePlaceholder" />
      </div>
      <div class="col-auto text-end" v-if="expandedState">
        <div v-if="body?.hash">
          <DownloadOriginalContentButton :body="body" />
          <CopyToClipboardButton
            :content="body?.previewContent"
            tooltip="Copy preview content to clipboard"
          />
        </div>
        <div v-else-if="usePlaceholder">
          <PlaceholderButton class="btn-sm btn-primary me-2" />
          <PlaceholderButton class="btn-sm btn-secondary me-2" />
        </div>
      </div>
    </div>
    <HttpBodyTabs
      :body="body"
      :usePlaceholder="usePlaceholder"
      :expandedState="expandedState"
      @toggle-expanded="toggleExpanded"
    />
  </div>
</template>

<style scoped></style>