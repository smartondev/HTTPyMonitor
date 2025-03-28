import asyncio
import traceback

import aiohttp
from aiohttp import web
from multidict import CIMultiDict

from environment import Environment
from http_helper import parse_query_params, get_host_with_port_from_url, http_remove_not_forwardable_headers, url_replace_host
from proxy_log import ProxyLog, ProxyLogPhase, HttpHeaders, ContentStorage, RequestEntry


async def handle_proxy(request: aiohttp.web.Request):
    proxy_log: ProxyLog = request.app.get('proxy_log')
    log: RequestEntry | None = None
    try:
        environment: Environment = request.app.get('environment')
        destination = environment.PROXY_DESTINATION
        host_from_destination = get_host_with_port_from_url(destination)
        forward_headers = CIMultiDict(request.headers)
        if environment.PROXY_OVERRIDE_HOST_HEADER:
            forward_headers['host'] = host_from_destination
        request_headers = HttpHeaders.create_by(forward_headers)
        http_remove_not_forwardable_headers(forward_headers)
        request_query_params = request.query_string
        if request_query_params:
            request_query_params = f'?{request_query_params}'
        destination_url = f'{destination}{request.path}{request_query_params}'
        log = proxy_log.new_entry(
            method=request.method,
            url=url_replace_host(str(destination_url), forward_headers['host']), headers=request_headers,
            query_parameters=parse_query_params(str(request.url))
        )
        async with (aiohttp.ClientSession() as session):
            # if random.randint(1, 4) == 1:
            #     raise RuntimeError('Random error!')
            data = None
            if request.can_read_body:
                log = log.mutate(ProxyLogPhase.REQUEST_BODY_READING)
                proxy_log.put(log)
                data = await request.read()
            print(f'{request.method} {request.url} -> {destination_url}...')
            log = log.mutate(ProxyLogPhase.REQUEST_FORWARD)
            log.forward_destination = destination_url
            log.with_request_body(data, request_headers.content_type())
            proxy_log.put(log)
            async with session.request(
                    request.method, destination_url, headers=forward_headers, data=data
            ) as response:
                return await handel_proxy_response(response, log, proxy_log)
    except Exception as e:
        print(f"Exception: {e}")
        if log is not None:
            log = log.mutate(ProxyLogPhase.END)
            log.exception_type = str(type(e))
            log.exception_message = str(e)
            log.exception_traceback = traceback.format_exc()
            proxy_log.put(log)
    finally:
        if log is not None and not log.phase_is_end():
            log = log.mutate(ProxyLogPhase.END)
            proxy_log.put(log)


async def handel_proxy_response(response: aiohttp.ClientResponse, log: RequestEntry, proxy_log: ProxyLog):
    log = log.mutate(ProxyLogPhase.RESPONSE_BODY_READING)
    forward_headers = CIMultiDict(response.headers)
    response_headers = HttpHeaders.create_by(forward_headers)
    http_remove_not_forwardable_headers(forward_headers)
    log.with_response_headers(response_headers)
    log.response_status = response.status
    proxy_log.put(log)
    body = await response.read()
    log = log.mutate(ProxyLogPhase.RESPONSE_BODY_READ)
    log.with_response_body(body, response_headers.content_type())
    proxy_log.put(log)
    return web.Response(
        body=body,
        status=response.status,
        headers=forward_headers,
    )


async def storage_garbage_task(app):
    print('Starting storage garbage task...')
    content_storage: ContentStorage = app.get('proxy_log').get_content_storage()
    while True:
        content_storage.garbage()
        await asyncio.sleep(600)


def run_proxy_server(environment: Environment, proxy_log: ProxyLog):
    app = web.Application(client_max_size=environment.HTTP_MAX_REQUEST_SIZE_MB * 1024 ** 2)
    app.setdefault('environment', environment)
    app.setdefault('proxy_log', proxy_log)
    app.router.add_route('*', '/{any:.*}', handle_proxy)

    async def on_startup(_app):
        _app['storage_garbage_task'] = asyncio.create_task(storage_garbage_task(app))

    async def on_cleanup(_app):
        _app['storage_garbage_task'].cancel()
        await _app['storage_garbage_task']

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)

    try:
        web.run_app(app, host=environment.PROXY_LISTEN_HOST, port=environment.PROXY_LISTEN_PORT)
    except KeyboardInterrupt:
        app.shutdown()
