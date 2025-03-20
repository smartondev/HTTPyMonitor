<script setup lang="ts">
import { RouterView } from 'vue-router'
import NavHeader from '@/components/layouts/NavHeader.vue'
import Footer from '@/components/layouts/Footer.vue'
</script>

<template>
  <NavHeader />
  <main class="container-fluid m-auto my-1 flex-grow-1">
    <RouterView />
  </main>
  <Footer />
</template>

<style scoped>
main {
  max-width: 1400px;
}
</style>
