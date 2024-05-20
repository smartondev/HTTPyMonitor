<script setup lang="ts">
import type {RequestLogUi, RequestLogUiStates} from "@/types/RequestLogUi";
import RequestLogItem from "../components/RequestLogItemDetailed.vue";
import RequestLogItemSlim from "../components/RequestLogItemSlim.vue";

type Props = {
  title: string,
  models: RequestLogUi[],
}

const props = withDefaults(defineProps<Props>(), {
  title: () => '',
  model: () => [],
});

defineEmits(['drop'])

const componentByModel = function (model: RequestLogUiStates) {
  return model.isExpanded ? RequestLogItem : RequestLogItemSlim;
}

const toggleSticky = function (item: RequestLogUiStates) {
  item.isSticky = !item.isSticky
}

const toggleExpanded = function (item: RequestLogUiStates) {
  item.isExpanded = !item.isExpanded
}

</script>

<template>
  <div class="log-container mb-5 py-2 rounded-4 border-3 px-2">
    <div class="mt-1 mb-2 text-center title fw-bold fs-5">{{ title }}</div>
    <component
        :is="componentByModel(model)"
        :model="model" @drop="$emit('drop', model)"
        @toggle-sticky="toggleSticky" @toggle-expanded="toggleExpanded"
        v-for="model in models" :key="model.id"/>
  </div>
</template>

<style scoped>
.title {
  color: #aaa;
}

.log-container {
  border-color: #ccc;
  border-style: dashed;
}
</style>