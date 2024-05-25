from urllib.parse import urlparse, parse_qs

from multidict import CIMultiDict, CIMultiDictProxy


def get_mime_type_from_content_type(content_type: str | None) -> str | None:
    if content_type is None:
        return None
    return content_type.split(';')[0].strip()


def get_host_with_port_from_url(url: str) -> str:
    parsed = urlparse(url)
    port = ''
    if parsed.port is not None:
        port = f':{parsed.port}'
    return f'{parsed.hostname}{port}'


def url_replace_host(url: str, new_host: str | None) -> str:
    if new_host is None:
        return url
    parsed = urlparse(url)
    return parsed._replace(netloc=new_host).geturl()


def parse_query_params(url: str) -> list[tuple[str, str]] | None:
    query = urlparse(url).query
    params_dict = parse_qs(query)
    if len(params_dict) == 0:
        return None
    params_list = []
    for k, v in params_dict.items():
        params_list.extend([(k, x) for x in v])
    return params_list


def http_remove_not_forwardable_headers(headers: CIMultiDict | CIMultiDictProxy):
    keys = ['content-encoding', 'content-length', 'transfer-encoding']
    for key in keys:
        try:
            del headers[key]
        except KeyError:
            pass
