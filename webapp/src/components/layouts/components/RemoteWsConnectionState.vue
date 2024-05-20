<script setup lang="ts">

import {RemoteWsConnectionStates} from "@/services/RemoteWs";
import {inject} from "vue";
import {RemoteWsClientConnectionState} from "@/keys";

const connectionState = inject(RemoteWsClientConnectionState)
</script>

<template>
  <div>
    <span v-if="connectionState === RemoteWsConnectionStates.CONNECTED " class="text-success">
      <i class="bi-check2-circle me-1 text-success"/> Connected
    </span>
    <span v-else-if="connectionState === RemoteWsConnectionStates.CONNECTING" class="text-warning">
      <i class="bi-arrow-repeat me-1 text-warning"/> Connecting
    </span>
    <span v-else class="text-danger">
      <i class="bi-circle-fill me-1"/> Disconnected
    </span>
  </div>
</template>

<style scoped>

</style>