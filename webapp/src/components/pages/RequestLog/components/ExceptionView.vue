<script setup lang="ts">
import useExpand from '@/composables/useExpand'
import type { RequestLogException } from '@/types/RequestLog'
import { isNotUndefined } from '@/helpers/ConditionHelper'
import { computed } from 'vue'
import type { Optional } from '@/types/Optional'

type Props = {
  exception: Optional<RequestLogException>
}

const props = withDefaults(defineProps<Props>(), {
  exception: undefined
})

const { expandedState, toggleExpanded } = useExpand(true)

const show = computed(() => {
  return isNotUndefined(props.exception)
})
</script>

<template>
  <div class="container-fluid mb-3 px-0 mx-0" v-if="show">
    <div class="row">
      <div class="col-12 cursor-pointer" @click="toggleExpanded">
        <span class="fs-6 fw-bold me-2">Exception</span>
        <span class="bi bi-caret-up-fill me-2" v-if="expandedState" />
        <span class="bi bi-caret-down-fill me-2" v-else />
      </div>
    </div>
    <div class="row ps-3" v-if="expandedState">
      <div class="col-12">
        <span class="fw-bold font-monospace">{{ exception?.message }} {{ exception?.type }}</span>
        <pre v-text="exception?.traceback" />
      </div>
    </div>
    <div class="row ps-3 cursor-pointer" v-else @click="toggleExpanded">
      <div class="col-12 text-truncate fs-80">
        <span v-text="exception?.message" class="me-2" />
        <span v-text="exception?.type" class="me-2" />
        <span v-text="exception?.traceback" />
      </div>
    </div>
  </div>
</template>

<style scoped>
pre {
  max-height: 400px;
}
</style>