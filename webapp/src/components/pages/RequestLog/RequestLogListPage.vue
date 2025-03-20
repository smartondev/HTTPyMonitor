<script setup lang="ts">
import { inject } from 'vue'
import { RemoteWsClientItems } from '@/keys'
import type { RequestLogUiList } from '@/types/RequestLogUi'
import RequestLogContainer from './containters/RequestLogContainer.vue'

const items = inject<RequestLogUiList>(RemoteWsClientItems)
</script>

<template>
  <RequestLogContainer v-model="items" />
</template>

<style scoped></style>