<script setup lang="ts">

import {isNotUndefined} from "@/helpers/ConditionHelper";
import {computed, ref} from "vue";
import {getDownloadUrlPrefix} from "@/helpers/EnvironmentHelper";
import type {RequestLogBody} from "@/types/RequestLog";
import PlaceholderParagraph from "@/components/common/PlaceholderParagraph.vue";

type Props = {
  body: RequestLogBody | undefined,
  usePlaceholder: boolean,
  expandedState: boolean,
}

const props = withDefaults(defineProps<Props>(), {
  body: undefined,
  usePlaceholder: false,
  expandedState: false,
});

const TAB_KEY_PREVIEW = 'preview';
const TAB_KEY_BROWSER_PREVIEW = 'browser-preview';
const activeTab = ref(TAB_KEY_PREVIEW);

const tabs = computed(() => {
  return [
    {
      active: activeTab.value === TAB_KEY_PREVIEW,
      title: 'Preview',
      key: TAB_KEY_PREVIEW,
    }, {
      active: activeTab.value === TAB_KEY_BROWSER_PREVIEW,
      title: 'Browser preview',
      key: TAB_KEY_BROWSER_PREVIEW,
    }
  ];
})

const iframeSrc = computed(() => {
  if (props.body?.hash === null) {
    return '';
  }
  return getDownloadUrlPrefix() + `/${props.body?.hash}?content_type=${encodeURIComponent(props.body?.contentType ?? '')}`;
})

defineEmits(['toggle-expanded']);

</script>

<template>
  <div class="ps-3">
    <div class="row">
      <div class="col-12" v-if="expandedState">
        <ul class="nav nav-tabs">
          <li class="nav-item" v-for="item in tabs" :key="item.key" @click="activeTab = item.key">
            <button class="nav-link" :class="{active: item.active}"
                    v-if="!usePlaceholder" v-text="item.title"/>
            <button v-else class="nav-link bg-secondary placeholder text-secondary" href="#"
                    v-text="item.title"/>
          </li>
        </ul>
      </div>
    </div>
    <div class="row" v-if="expandedState">
      <div class="col-12">
        <PlaceholderParagraph v-if="usePlaceholder"/>
        <div v-else-if="activeTab === TAB_KEY_PREVIEW">
          <pre v-if="isNotUndefined(body?.previewContent)" v-text="body?.previewContent"/>
          <b class="d-block text-info height-fix" v-else>Preview not available</b>
        </div>
        <iframe v-else-if="activeTab === TAB_KEY_BROWSER_PREVIEW" :src="iframeSrc"
                class="w-100" height="400"/>
      </div>
    </div>
    <div class="row ps-3 cursor-pointer" v-else @click="$emit('toggle-expanded')">
      <div class="col-12 text-truncate fs-80">
        <span v-if="usePlaceholder" class="col-12 placeholder"/>
        <span v-else v-text="body?.previewContent"/>
      </div>
    </div>
  </div>
</template>

<style scoped>
pre, .height-fix {
  max-height: 400px;
  min-height: 150px;
}
</style>