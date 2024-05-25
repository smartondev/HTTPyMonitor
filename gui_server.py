import asyncio
import os

from aiohttp import web

from environment import Environment
from gui_server_ws import broadcast, handle_ws_remote
from proxy_log import ProxyLog


def static_dir() -> str:
    return os.path.join('.', 'webapp', 'dist')


async def handle_download(request):
    hash_value = request.match_info['hash']
    proxy_log: ProxyLog = request.app.get('proxy_log')
    content = proxy_log.get_content_storage().read(hash_value)
    if content is None:
        return web.Response(status=404)
    content_type = request.query.get('content_type', 'application/octet-stream')
    return web.Response(body=content, status=200, headers={'Content-Type': content_type})


def run_gui_server(environment: Environment, proxy_log: ProxyLog):
    app = web.Application()
    app.setdefault('proxy_log', proxy_log)

    async def index(request):
        return web.FileResponse(os.path.join(static_dir(), 'index.html'))

    app.add_routes([
        web.get('/', index),
        web.get('/remote', handle_ws_remote),
        web.get('/download/{hash}.{extension}', handle_download),
        web.get('/download/{hash}', handle_download),
    ])

    app.router.add_static('/', path=static_dir(), name='static')

    async def on_startup(_app):
        _app['broadcast_task'] = asyncio.create_task(broadcast(app))

    async def on_cleanup(_app):
        _app['broadcast_task'].cancel()
        await _app['broadcast_task']

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)

    try:
        web.run_app(app, host=environment.GUI_LISTEN_HOST, port=environment.GUI_LISTEN_PORT)
    except KeyboardInterrupt:
        app.shutdown()
