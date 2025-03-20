<script setup lang="ts">
import NameValueListContainer from '@/components/pages/RequestLog/containters/NameValueListContainer.vue'
import useRequestLogUi from '@/composables/useRequestLog'
import { computed, defineProps } from 'vue'
import type { RequestLogUi } from '@/types/RequestLogUi'
import RequestLogItemSlim from './RequestLogItemSlim.vue'
import HttpBody from '@/components/pages/RequestLog/components/HttpBody.vue'
import PropertyValueContainer from '@/components/pages/RequestLog/containters/PropertyValueContainer.vue'
import Tag from '@/components/pages/RequestLog/components/Tag.vue'
import TagHttpStatus from '@/components/pages/RequestLog/components/TagHttpStatus.vue'
import TagBodySize from '@/components/pages/RequestLog/components/TagBodySize.vue'
import ExceptionView from '@/components/pages/RequestLog/components/ExceptionView.vue'
import { isNotUndefined } from '@/helpers/ConditionHelper'
import { RequestLogPhase } from '@/types/RequestLog'
import useHttpPhaseToString from '@/composables/useHttpPhaseToString'

const emits = defineEmits<{
  (e: 'toggle-sticky', model: RequestLogUi): void
  (e: 'drop', model: RequestLogUi): void
  (e: 'toggle-expanded', model: RequestLogUi): void
}>()

type Props = {
  model: RequestLogUi
}

const props = withDefaults(defineProps<Props>(), {
  model: () => ({}) as RequestLogUi
})
const { variantByStatus, variantByMethod } = useRequestLogUi(props.model)

const isPhaseEnd = computed<boolean>(() => props.model.phase === RequestLogPhase.END)

const clickDrop = (): void => {
  emits('drop', props.model)
}

const clickToggleSticky = (): void => {
  emits('toggle-sticky', props.model)
}

const clickToggleExpanded = (): void => {
  emits('toggle-expanded', props.model)
}
</script>

<template>
  <div
    class="card rounded-2 border-0 opened shadow mb-2"
    :class="[variantByMethod, variantByStatus]"
  >
    <div class="card-header border-0 cursor-pointer px-0" @click="clickToggleExpanded">
      <RequestLogItemSlim :model="model" @drop="clickDrop" @toggle-sticky="clickToggleSticky" />
    </div>
    <div class="card-body pt-1" v-if="model.isExpanded">
      <div class="row">
        <div class="col-12 mb-2">
          <Tag property="Phase" :value="useHttpPhaseToString(model.phase)" />
          <TagHttpStatus :status="model.response?.status" />
          <TagBodySize property="Request body size" :length="model.request?.body?.length" />
          <TagBodySize property="Response body size" :length="model.response?.body?.length" />
        </div>
        <div class="col-12">
          <PropertyValueContainer title="URL" :value="model.request?.url" />
        </div>
      </div>
      <div class="row">
        <div class="col-lg-4 col-md-6 col-sm-12" v-if="model.request?.headers">
          <NameValueListContainer title="Request headers" :list="model.request?.headers" />
        </div>
        <div class="col-lg-4 col-md-6 col-sm-12" v-if="model.request?.queryParameters">
          <NameValueListContainer title="Query parameters" :list="model.request?.queryParameters" />
        </div>
        <div
          class="col-lg-4 col-md-6 col-sm-12"
          v-if="isNotUndefined(model.response?.headers) || !isPhaseEnd"
        >
          <NameValueListContainer
            title="Response headers"
            :list="model.response?.headers"
            :placeholder="true"
          />
        </div>
      </div>
      <div class="row">
        <div class="col-12" v-if="isNotUndefined(model.request?.body)">
          <HttpBody :body="model.request?.body" title="Request body" :placeholder="true" />
        </div>
        <div class="col-12" v-if="isNotUndefined(model.response?.body) || !isPhaseEnd">
          <HttpBody
            :body="model.response?.body"
            title="Response body"
            :placeholder="true"
            :expanded="true"
          />
        </div>
        <div class="col-12">
          <ExceptionView :exception="model.exception" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use 'sass:color';
@use '@/assets/colors' as *;

@each $method, $color in $methodVariants {
  .variant-#{$method} {
    .card-header {
      color: color.adjust($color, $lightness: -30%);
      background-color: color.adjust($color, $lightness: 10%);
    }
  }
}
</style>
