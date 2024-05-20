<script setup lang="ts">

import {computed} from "vue";

const props = defineProps({
  timestamp: Number,
})

const dateObject = computed(() => new Date((props.timestamp ?? 0) * 1000))

const time = computed(() => {
  return {
    hours: dateObject.value.getHours().toString().padStart(2, '0'),
    minutes: dateObject.value.getMinutes().toString().padStart(2, '0'),
    seconds: dateObject.value.getSeconds().toString().padStart(2, '0'),
  }
});
</script>

<template>
<span v-if="timestamp" class="font-monospace" :title="dateObject.toLocaleString()">
  [{{ time.hours }}:{{ time.minutes }}:{{ time.seconds }}]
</span>
</template>

<style scoped>
</style>