import type { RequestLog } from '@/types/RequestLog'

export type RequestLogUiStates = {
  isSticky: boolean
  isExpanded: boolean
}

export type RequestLogUi = RequestLog & RequestLogUiStates

export type RequestLogUiList = RequestLogUi[]
