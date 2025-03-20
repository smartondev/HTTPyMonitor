<script setup lang="ts">
import Tag from '@/components/pages/RequestLog/components/Tag.vue'
import useToBytesFormatter from '@/composables/useToBytesFormatter'
import type { OptionalNumber } from '@/types/Optional'

type Props = {
  length: OptionalNumber
  property: string
}

const props = withDefaults(defineProps<Props>(), {
  length: 0
})
</script>

<template>
  <Tag v-if="props.length > 0" :property="property" :value="useToBytesFormatter(props.length)" />
</template>

<style scoped></style>