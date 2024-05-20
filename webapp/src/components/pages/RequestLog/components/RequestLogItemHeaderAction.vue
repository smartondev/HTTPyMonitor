<script setup lang="ts">

import type {RequestLogUi} from "@/types/RequestLogUi";

const emits = defineEmits(['drop', 'toggle-sticky'])

type Props = {
  model: RequestLogUi,
  size?: string,
}

const props = withDefaults(defineProps<Props>(), {
  model: () => ({} as RequestLogUi),
})

</script>

<template>
  <div>
    <button type="button" @click="$emit('toggle-sticky', model)" class="btn btn-sm py-0">
      <i :class="{
                'bi-pin-angle': !model.isSticky,
                'bi-pin-fill': model.isSticky,
              }"/>
    </button>
    <button type="button" @click="$emit('drop', model)" class="btn btn-sm py-0">
      <i class="bi-trash"/>
    </button>
  </div>
</template>

<style scoped lang="scss">
@import "bootstrap/scss/functions";
@import "bootstrap/scss/variables";
@import "bootstrap/scss/mixins";

@include media-breakpoint-down(lg) {
  .btn {
    font-size: 1.5rem;
  }
}

</style>