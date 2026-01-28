<script setup lang="ts">
import Tag from '@/components/pages/RequestLog/components/Tag.vue'
import bytesFormatter from '@/formatters/bytesFormatter'
import type {OptionalNumber} from '@/types/Optional'

type Props = {
  length: OptionalNumber
  property: string
}

const props = withDefaults(defineProps<Props>(), {
  length: 0
})
</script>

<template>
  <Tag v-if="props.length > 0" :property="property" :value="bytesFormatter(props.length)" />
</template>

<style scoped></style>