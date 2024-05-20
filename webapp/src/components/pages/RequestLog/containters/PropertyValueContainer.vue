<script setup lang="ts">

type Props = {
  title: string,
  value?: string | null,
  truncateAllowed?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  value: '',
  truncateAllowed: false,
})

</script>

<template>
  <div class="container-fluid mb-3 px-0 mx-0">
    <div class="row">
      <div class="col-auto">
        <span class="fs-6 fw-bold">{{ title }}</span>
      </div>
      <div class="col" :class="{'text-truncate': truncateAllowed}">
        <span class="font-monospace" v-if="value !== null">{{ value }}</span>
        <span v-else>-</span>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>