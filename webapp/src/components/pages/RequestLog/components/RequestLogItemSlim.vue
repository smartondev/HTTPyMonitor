<script setup lang="ts">

import {defineProps} from "vue";
import useRequestLogUi from "@/components/pages/RequestLog/services/RequestLog";
import RequestLogItemHeaderAction from "./RequestLogItemHeaderAction.vue";
import type {RequestLogUi} from "@/types/RequestLogUi";
import LogTime from "@/components/pages/RequestLog/components/LogTime.vue";
import ElapsedTime from "@/components/pages/RequestLog/components/ElapsedTime.vue";
import {RequestLogPhase} from "@/types/RequestLog";

defineEmits(['drop', 'toggle-sticky', 'toggle-expanded'])
type Props = {
  model: RequestLogUi,
}

const props = withDefaults(defineProps<Props>(), {
  model: () => ({} as RequestLogUi),
})

const {
  variant_by_status,
  variant_by_method,
} = useRequestLogUi(props.model)

</script>

<template>
  <div class="log container-fluid cursor-pointer mb-lg-0" @click="$emit('toggle-expanded', model)" :class="[
      variant_by_method, variant_by_status,
  ]">
    <div class="d-grid gap-1">
      <div class="time">
        <LogTime :timestamp="model.time"/>
      </div>
      <div class="elapsed-time text-end">
        <ElapsedTime :start-timestamp="model.time"
                     :end-timestamp="model.phase !== RequestLogPhase.END? null : model.lastTime"/>
      </div>
      <div class="http-status text-center">
        {{ model.response?.status ?? '...' }}
      </div>
      <div class="text-center http-method rounded-2 text-truncate">
        {{ model.request?.method }}
      </div>
      <div class="url text-truncate">
        {{ model.request?.url }}
      </div>
      <div class="actions text-end">
        <RequestLogItemHeaderAction :model="model" @drop="$emit('drop', model)"
                                    @toggle-sticky="$emit('toggle-sticky', model)"/>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import "@/assets/colors";
@import "bootstrap/scss/functions";
@import "bootstrap/scss/variables";
@import "bootstrap/scss/mixins";

@include media-breakpoint-down(lg) {
  .d-grid {
    grid-template-areas:
    "time elapsed-time http-status http-method spacer actions"
    "url url url url url actions";
    grid-template-columns: 90px 80px 60px 150px 1fr 100px;
  }
}

@include media-breakpoint-up(lg) {
  .d-grid {
    grid-template-areas:
    "time elapsed-time http-status http-method url actions";
    grid-template-columns: 90px 80px 60px 150px 1fr 100px;
  }
  .log {
    .actions {
      display: none;
    }
    :hover .actions {
      display: block;
    }
  }
}

.http-method {
  grid-area: http-method;
}

.http-status {
  grid-area: http-status;
}

.time {
  grid-area: time;
}

.elapsed-time {
  grid-area: elapsed-time;
}

.url {
  grid-area: url;
}

.actions {
  grid-area: actions;
  display: flex;
  align-items: center;
  justify-content: center;
}

@each $method, $color in $methodVariants {
  .variant-#{$method} {


    &.log:hover {
      .http-method {
        background-color: lighten($color, 10%);
        transition: background-color 0.2s ease-in;
      }

      font-weight: bold;
      color: darken($color, 30%);
      transition: color 0.5s ease-in;

      .d-lg-block.actions {
        opacity: 1.0;
        transition: opacity 0.5s linear;
      }
    }

    &.log:not(:hover) {
      .d-lg-block.actions {
        opacity: 0.0;
      }
    }
  }

}

.card-header {
  cursor: pointer;
}
</style>