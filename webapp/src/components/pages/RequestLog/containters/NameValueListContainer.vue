<script setup lang="ts">

import useExpand from "@/services/ui/Expand";
import {computed, defineProps, onMounted, ref} from "vue";
import type {NameValuePairs} from "@/types/common";

import {randomInt} from "@/helpers/RandomHelper";

type Props = {
  list?: NameValuePairs | undefined,
  title: string,
  placeholder?: boolean,
  placeholderValueMin?: number,
  placeholderValueMax?: number,
}

const props = withDefaults(defineProps<Props>(), {
  list: undefined,
  placeholder: false,
  placeholderValueMin: 4,
  placeholderValueMax: 6,
})

const {
  expandedState,
  toggleExpanded,
} = useExpand()

const placeholderList = ref<NameValuePairs>([]);
onMounted(() => {
  const placeholderValueCount: number = randomInt(props.placeholderValueMin, props.placeholderValueMin);
  placeholderList.value = Array.from({length: placeholderValueCount}, (_, __) => ({
    name: 'col-' + randomInt(1, 3),
    value: 'col-' + randomInt(2, 5),
  }))
})

const usePlaceholder = computed(() => {
  return props.placeholder && props.list === undefined;
})

const itemList = computed(() => {
  return usePlaceholder.value ? placeholderList.value : (props.list ?? []);
})

</script>

<template>
  <div class="container-fluid mb-3 ms-0 ps-0 placeholder-glow">
    <div class="row">
      <div class="col-lg-12 cursor-pointer" @click="toggleExpanded">
        <span class="fs-6 fw-bold me-2">{{ title }}</span>
        <span class="bi bi-caret-up-fill" v-if="expandedState"/>
        <span class="bi bi-caret-down-fill" v-else/>
      </div>
    </div>
    <div class="key-values" :class="{
        expanded: expandedState,
       'text-truncate': !expandedState,
    }">
      <div class="row gap-2 font-monospace ps-3" v-for="(item, idx) in itemList" :key="idx">
        <div class="col-12 fs-90" v-if="usePlaceholder">
          <span class="placeholder me-1 bg-primary" :class="[item.name]"/><span class="placeholder"
                                                                                :class="[item.value]"/>
        </div>
        <div class="col-12 fs-90" v-else>
          <span class="fw-bold text-primary">{{ item.name }}</span>: {{ item.value }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.key-values:not(.expanded) {
  .row, .col-12 {
    display: inline;
  }
}
</style>