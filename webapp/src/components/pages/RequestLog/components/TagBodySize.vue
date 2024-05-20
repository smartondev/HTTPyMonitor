<script setup lang="ts">

import {toBytes} from "@/helpers/NumberHelper";
import Tag from "@/components/pages/RequestLog/components/Tag.vue";

type Props = {
  length: number | undefined,
  property: string
}

const props = withDefaults(defineProps<Props>(), {
  length: 0,
})
</script>

<template>
  <Tag v-if="props.length > 0" :property="property" :value="toBytes(props.length)"/>
</template>

<style scoped>

</style>