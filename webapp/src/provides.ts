import {ref} from "vue";
import {RemoteWsClientConnectionState, RemoteWsClientItems} from "@/keys";
import type {RequestLogUi} from "@/types/RequestLogUi";
import {RemoteWsConnectionStates} from "@/services/RemoteWs";

export const RemoteWsClientItemsRef = ref<RequestLogUi[]>([])

console.log(RemoteWsConnectionStates)
export const RemoteWsClientConnectionStatedRef = ref<RemoteWsConnectionStates | null>(null)

export function createProvides(app: any) {
    app.provide(RemoteWsClientItems, RemoteWsClientItemsRef)
    app.provide(RemoteWsClientConnectionState, RemoteWsClientConnectionStatedRef)
    return app
}
