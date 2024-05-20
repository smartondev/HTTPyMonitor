<script setup lang="ts">

import type {RequestLogBody} from "@/types/RequestLog";
import useExpand from "@/services/ui/Expand";
import {computed, defineProps} from "vue";
import PlaceholderParagraph from "@/components/common/PlaceholderParagraph.vue";
import DownloadOriginalContentButton from "@/components/pages/RequestLog/components/DownloadOriginalContentButton.vue";
import CopyToClipboardButton from "@/components/pages/RequestLog/components/CopyToClipboardButton.vue";
import PlaceholderButton from "@/components/common/PlaceholderButton.vue";

type Props = {
  body?: RequestLogBody | undefined,
  title: string,
  placeholder?: boolean,
  expanded?: boolean,
}

const props = withDefaults(defineProps<Props>(), {
  body: undefined,
  title: '',
  placeholder: false,
  expanded: false,
});

const usePlaceholder = computed(() => {
  return props.placeholder && props.body === undefined;
})

const {
  expandedState,
  toggleExpanded,
} = useExpand(props.expanded);

const show = computed(() => {
  const length = props.body?.length;
  return length === undefined || length > 0 || (props.body === undefined && props.placeholder)
});

</script>

<template>
  <div class="container-fluid mb-3 px-0 mx-0 placeholder-glow" v-if="show">
    <div class="row">
      <div class="col-12 cursor-pointer" @click="toggleExpanded">
        <span class="fs-6 fw-bold me-2">{{ title }}</span>
        <span class="bi bi-caret-up-fill me-2" v-if="expandedState"/>
        <span class="bi bi-caret-down-fill me-2" v-else/>

        <span class="fs-80 fst-italic" v-if="body?.contentType">( {{ body.contentType }} )</span>
        <span class="fs-80 col-2 placeholder" v-if="usePlaceholder"/>
      </div>
      <div class="col-12 my-1" v-if="expandedState">
        <div v-if="body?.hash">
          <DownloadOriginalContentButton :body="body"/>
          <CopyToClipboardButton :content="body?.previewContent" title="Copy to clipboard"
                                 tooltip="Copy preview content to clipboard"/>
        </div>
        <div v-else-if="usePlaceholder">
          <PlaceholderButton class="btn-sm btn-primary col-1 me-2"/>
          <PlaceholderButton class="btn-sm btn-secondary col-1 me-2"/>
        </div>
      </div>
    </div>
    <div class="row ps-3" v-if="expandedState">
      <div class="col-12">
        <PlaceholderParagraph v-if="usePlaceholder"/>
        <pre v-else v-text="body?.previewContent"/>
      </div>
    </div>
    <div class="row ps-3 cursor-pointer" v-else @click="toggleExpanded">
      <div class="col-12 text-truncate fs-80">
        <span v-if="usePlaceholder" class="col-12 placeholder"/>
        <span v-else v-text="body?.previewContent"/>
      </div>
    </div>
  </div>
</template>

<style scoped>
pre {
  max-height: 400px;
}
</style>