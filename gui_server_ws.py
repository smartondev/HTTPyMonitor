import asyncio
import json
import traceback
from enum import Enum

from aiohttp import web

from proxy_log import ProxyLog


class WebsocketDataEndpoints(Enum):
    REQUEST_LOG = 'requestLog'
    SYSTEM_INFO = 'systemInfo'


connected_ws_clients = set()


async def handle_ws_remote(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    connected_ws_clients.add(ws)

    async for msg in ws:
        # if msg.type == web.WSMsgType.text:
        #     await ws.send_str("Hello, {}".format(msg.data))
        # elif msg.type == web.WSMsgType.binary:
        #     await ws.send_bytes(msg.data)
        if msg.type == web.WSMsgType.close:
            connected_ws_clients.remove(ws)
            break

    return ws


async def broadcast_send_client(ws, message):
    try:
        if ws.closed:
            return
        await ws.send_str(message)
    except asyncio.CancelledError as e:
        raise e
    except Exception as e:
        print('Exception:', e)
        traceback.print_exc()


async def broadcast(app):
    task = asyncio.current_task()
    while task.cancelled() is False:
        await broadcast_logs(app)
        await asyncio.sleep(0.1)


async def broadcast_data(endpoint: WebsocketDataEndpoints, data: dict):
    try:
        data = {
            "endpoint": endpoint.value,
            "data": data
        }
        json_data = json.dumps(data)
        dead_clients = set()
        for ws in connected_ws_clients:
            if ws.closed:
                dead_clients.add(ws)
                continue
            # TODO async task per client
            await broadcast_send_client(ws, json_data)
        for dead_client in dead_clients:
            connected_ws_clients.remove(dead_client)
    except asyncio.CancelledError as e:
        raise e
    except Exception as e:
        print('Exception:', e)
        traceback.print_exc()


async def broadcast_logs(app):
    proxy_log: ProxyLog = app.get('proxy_log')
    while True:
        try:
            log_entry = proxy_log.first_and_remove()
            if log_entry is None:
                return

            await broadcast_data(WebsocketDataEndpoints.REQUEST_LOG, log_entry.to_map())
        except asyncio.CancelledError as e:
            raise e
        except Exception as e:
            print('Exception:', e)
            traceback.print_exc()
