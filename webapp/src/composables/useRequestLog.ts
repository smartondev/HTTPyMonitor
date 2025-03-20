import { computed } from 'vue'
import type { RequestLogUi } from '@/types/RequestLogUi'

export default function useRequestLogUi(model: RequestLogUi) {
  const variantByStatus = computed<string>(() => {
    if (typeof model?.response?.status === 'number') {
      if (model.response.status >= 200 && model.response.status < 300) {
        return 'variant-2xx'
      } else if (model.response.status >= 300 && model.response.status < 400) {
        return 'variant-3xx'
      } else {
        return 'variant-4xx-5xx'
      }
    }
    return 'variant-xxx'
  })
  const variantByMethod = computed<string>(() => {
    if (typeof model?.request?.method === 'string') {
      return `variant-${model.request.method.toLowerCase()}`
    }
    return ''
  })

  return {
    variantByStatus,
    variantByMethod,
  }
}
