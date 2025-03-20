import { ref } from 'vue'
import { RemoteWsClientConnectionState, RemoteWsClientItems } from '@/keys'
import type { RequestLogUiList } from '@/types/RequestLogUi'
import { RemoteWsConnectionStates } from '@/composables/useRemoteWs'

export const RemoteWsClientItemsRef = ref<RequestLogUiList>([])

export const RemoteWsClientConnectionStatedRef = ref<RemoteWsConnectionStates | null>(null)

export function createProvides(app: any) {
  app.provide(RemoteWsClientItems, RemoteWsClientItemsRef)
  app.provide(RemoteWsClientConnectionState, RemoteWsClientConnectionStatedRef)
  return app
}
