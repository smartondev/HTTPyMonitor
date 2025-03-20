import type { RequestLog } from '@/types/RequestLog'
import { RequestLogPhase } from '@/types/RequestLog'
import type { RequestLogUi } from '@/types/RequestLogUi'
import { RemoteWsClientConnectionStatedRef, RemoteWsClientItemsRef } from '@/provides'
import { deepMerge } from '@/helpers/ObjectHelper'
import { findLastIndexOf } from '@/helpers/ArrayHelper'

export enum RemoteWsConnectionStates {
  DISCONNECTED = 'DISCONNECTED',
  CONNECTING = 'CONNECTING',
  CONNECTED = 'CONNECTED'
}

enum RemoteDataEndpoints {
  REQUEST_LOG = 'requestLog',
  SERVER_INFO = 'serverInfo'
}

type RemoteData = {
  endpoint: RemoteDataEndpoints
  data: RequestLog
}

type OnReceiveFunction = (event: RemoteData) => void

export class RemoteWsClient {
  private readonly url: string

  private ws: WebSocket | null = null
  private reconnectDelay: number = 5.0
  private reconnectTimer: any
  private pingDelay: number = 5.0
  private pingTimer: any
  private isConnected: boolean = false
  private isClosing: boolean = false
  private receiveFunction: OnReceiveFunction | null = null

  constructor(url: string) {
    this.url = url
  }

  public destroy() {
    this.close()
  }

  public onReceive(fn: OnReceiveFunction) {
    this.receiveFunction = fn
  }

  public connect() {
    this.isClosing = false
    this.doConnect()
  }

  private doConnect() {
    if (this.isClosing) {
      return
    }
    try {
      if (this.ws !== null) {
        try {
          this.ws.close()
        } catch {}
        this.ws = null
      }
      RemoteWsClientConnectionStatedRef.value = RemoteWsConnectionStates.CONNECTING
      const ws = new WebSocket(this.url)

      ws.onopen = () => {
        RemoteWsClientConnectionStatedRef.value = RemoteWsConnectionStates.CONNECTED
        this.isConnected = true
        this.pingTimer = setInterval(() => {
          this.send({ command: 'ping' })
        }, 1000 * this.pingDelay)
      }

      ws.onmessage = (event) => {
        if (this.receiveFunction !== null) {
          this.receiveFunction(JSON.parse(event.data))
        }
      }

      ws.onerror = (error) => {
        console.error(`WebSocket error: ${error}`)
      }

      ws.onclose = (event) => {
        console.info(`WebSocket connection closed: ${event.code}`)
        RemoteWsClientConnectionStatedRef.value = RemoteWsConnectionStates.DISCONNECTED
        this.isConnected = false
        this.delayedConnect()
      }
      this.ws = ws
    } catch (e) {
      console.error(e)
      this.delayedConnect()
    }
  }

  private delayedConnect() {
    if (this.isClosing) {
      return
    }
    this.reconnectTimer = setTimeout(() => {
      this.doConnect()
    }, this.reconnectDelay * 1000)
  }

  public send(data: any) {
    this.ws?.send(JSON.stringify(data))
  }

  public close() {
    this.isClosing = true
    clearTimeout(this.reconnectTimer)
    clearInterval(this.pingTimer)
    try {
      this.ws?.close()
    } catch {}
    this.isConnected = false
  }
}

export function useWsClient(url: string): RemoteWsClient {
  const client = new RemoteWsClient(url)
  const processRequestLog = function (model: RequestLog) {
    const index = RemoteWsClientItemsRef.value.findIndex((item) => item.id === model.id)
    if (index !== -1) {
      const existedModel = RemoteWsClientItemsRef.value[index]
      deepMerge(existedModel, model)
      return
    }
    if (model.phase !== RequestLogPhase.BEGIN) {
      return
    }
    RemoteWsClientItemsRef.value.unshift(model as RequestLogUi)
    const garbageLimitCount = 250
    const garbageLimitRange = 50
    if (RemoteWsClientItemsRef.value.length < garbageLimitCount) {
      return
    }
    const garbageCount = garbageLimitCount - garbageLimitRange
    let lastIndex = findLastIndexOf(RemoteWsClientItemsRef.value, (item) => !item.isSticky)
    while (RemoteWsClientItemsRef.value.length > garbageCount && lastIndex !== -1) {
      RemoteWsClientItemsRef.value.splice(lastIndex, 1)
      lastIndex = findLastIndexOf(
        RemoteWsClientItemsRef.value,
        (item) => !item.isSticky,
        lastIndex - 1
      )
    }
  }
  client.onReceive((event) => {
    switch (event.endpoint) {
      case RemoteDataEndpoints.REQUEST_LOG:
        processRequestLog(event.data)
        break
      case RemoteDataEndpoints.SERVER_INFO:
      default:
        console.warn('Not implemented endpoint: ', event.endpoint)
    }
  })

  return client
}
