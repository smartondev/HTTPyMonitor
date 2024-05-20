<script setup lang="ts">

import Tag from "@/components/pages/RequestLog/components/Tag.vue";
import {computed} from "vue";
import {httpReasonByStatusCode} from "@/helpers/HttpHelper";
import {isNotNullNorUndefined} from "@/helpers/ConditionHelper";

type Props = {
  status: number | undefined,
}

const props = withDefaults(defineProps<Props>(), {
  status: undefined,
})

const variant = computed(() => {
  if (props.status === undefined) {
    return 'secondary';
  }
  if (props.status >= 200 && props.status < 300) {
    return 'success';
  }
  if (props.status >= 300 && props.status < 400) {
    return 'warning';
  }
  if (props.status >= 400 && props.status < 500) {
    return 'info';
  }
  if (props.status >= 500) {
    return 'danger';
  }
  return 'secondary';
})

const value = computed(() => {
  if (props.status === undefined) {
    return null;
  }
  return props.status + ' ' + httpReasonByStatusCode(props.status);
})
</script>

<template>
  <Tag :value="value" :variant="variant" v-if="isNotNullNorUndefined(status)"/>
</template>

<style scoped>

</style>