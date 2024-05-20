<script setup lang="ts">
import {inject} from "vue";
import {RemoteWsClientItems} from "@/keys";
import type {RequestLogUi} from "@/types/RequestLogUi";
import RequestLogContainer from "./containters/RequestLogContainer.vue";

const items = inject(RemoteWsClientItems) as RequestLogUi[];

</script>

<template>
  <RequestLogContainer v-model="items"/>
</template>

<style scoped>

</style>