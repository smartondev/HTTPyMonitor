import { RequestLogPhase } from '@/types/RequestLog'

const useHttpPhaseToString = (phase: RequestLogPhase): string => {
  switch (phase) {
    case RequestLogPhase.END:
      return 'End'
    case RequestLogPhase.REQUEST_HEAD:
      return 'Request HEAD read'
    case RequestLogPhase.REQUEST_BODY_READING:
      return 'Request BODY reading'
    case RequestLogPhase.REQUEST_FORWARD:
      return 'Request FORWARD'
    case RequestLogPhase.RESPONSE_BODY_READING:
      return 'Response BODY reading'
    case RequestLogPhase.RESPONSE_BODY_READ:
      return 'Response BODY read'
    default:
      return 'Unknown'
  }
}

export default useHttpPhaseToString
