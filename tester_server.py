import asyncio
import json
import random
import string
import time
from multiprocessing import Process

import aiohttp
import brotli
from aiohttp import web

from environment import Environment
from random_helper import random_boolean


async def handle(request):
    request_body = None
    if request.can_read_body:
        request_body = await request.text()
    random_sleep = random.random() * 2 + 2.0
    response_data = {
        '\"': "\"",
        "űáéúő": "\nűáéúőóüö\nűáéúőóüŰÁÉÚŐÓÜÖ",
        'request': {
            'method': request.method,
            'url': str(request.url),
            'host': request.host,
            'body': request_body,
        },
        'multiline': "\n".join([string.ascii_lowercase for v in range(20)]),
        'random': random.randint(0, 100),
        'big_data': ''.join(random.choices(string.ascii_lowercase, k=1000)),
        'random_string': ''.join(random.choices(string.ascii_lowercase, k=random.randint(1, 10))),
        'random_dict': {random.choice(string.ascii_lowercase): random.randint(0, 100) for _ in
                        range(random.randint(1, 10))},
        'sleep': random_sleep,
    }
    time.sleep(random_sleep)
    status_code_rand = random.randint(0, 2)
    status_code = 200
    if status_code_rand == 0:
        status_code = random.randint(200, 210)
    elif status_code_rand == 1:
        status_code = random.randint(400, 420)
    elif status_code_rand == 2:
        status_code = random.randint(500, 520)
    if random_boolean():
        return web.json_response(response_data, status=status_code)
    json_bytes = json.dumps(response_data).encode('utf-8')
    json_bytes_brotli = brotli.compress(json_bytes)
    print('brotli compressed response size:', len(json_bytes_brotli), 'bytes')
    return web.Response(body=json_bytes_brotli, status=status_code, headers={
        'Content-Encoding': 'br',
        'Content-Type': 'application/json; charset=utf-8',
    })


def run_rest_api_server(environment: Environment):
    app = web.Application(client_max_size=environment.HTTP_MAX_REQUEST_SIZE_MB * 1024 ** 2)
    app.router.add_route('*', '/{any:.*}', handle)
    try:
        web.run_app(app, host=environment.TESTER_LISTEN_HOST, port=environment.TESTER_LISTEN_PORT)
    except KeyboardInterrupt:
        app.shutdown()


def run_rest_api_client(tester_destination: str):
    async def fetch(session, method, url, body):
        body_str = ''
        if body is str:
            body_str = body
        elif body is dict:
            body_str = json.dumps(body)
        if len(body_str) > 128:
            body_str = body_str[:128] + '...'
        print(f'Tester fetch {method} {url} {body_str}...')
        if body is dict:
            async with session.request(method, url, json=body) as response:
                return await response.text()
        else:
            headers = {
                'content-type': 'text/plain',
            }
            async with session.request(method, url, data=body, headers=headers) as response:
                return await response.text()

    async def main():
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    path = ''.join(random.choices(string.ascii_lowercase, k=random.randint(1, 10)))
                    method = random.choice(['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD', 'PATCH'])
                    body = None
                    if method in ['POST', 'PUT', 'PATCH']:
                        body = {
                            'key': ''.join(random.choices(string.ascii_lowercase, k=random.randint(1, 10))),
                            'value': random.randint(0, 100),
                        }
                    query_parameters_string = ''
                    if random_boolean():
                        query_parameters_string = '?' + '&'.join(
                            [f'key_{i}={random.randint(0, 100)}' for i in range(random.randint(1, 8))])
                    if random.randint(0, 15) < 1:
                        body = ''.join(random.choices(string.ascii_lowercase, k=2 * 1024 * 1024))
                    response = await fetch(session, method, f'{tester_destination}/{path}{query_parameters_string}',
                                           body=body)
                    if len(response) > 150:
                        response = response[:150] + '...'
                    print('... tester received response: ' + response)
                    await asyncio.sleep(random.random() * 3 + 0.1)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print('Tester exception:', e)

    asyncio.run(main())


def run_rest_api_tester(environment: Environment):
    Process(target=run_rest_api_server, args=(environment,)).start()
    time.sleep(2)
    for _ in range(1):
        Process(target=run_rest_api_client, args=(environment.TESTER_DESTINATION,)).start()
