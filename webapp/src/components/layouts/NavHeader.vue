<script setup lang="ts">
import { getAppVersion } from '@/helpers/EnvironmentHelper'
import RemoteWsConnectionState from '@/components/layouts/components/RemoteWsConnectionState.vue'
</script>

<template>
  <nav class="sticky-top shadow-lg mb-4 py-2">
    <div class="container-fluid">
      <div class="row justify-content-center">
        <div class="col-12 d-flex align-items-center">
          <span class="fs-4 fw-bold me-3">HTT<span class="text-primary">Py</span>Monitor</span>
          <span v-text="getAppVersion()" />
          <div class="ms-auto">
            <RemoteWsConnectionState />
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped>
nav {
  background-color: #222;
  color: #ddd;
}
</style>