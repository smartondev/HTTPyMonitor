from urllib.parse import urlparse, parse_qs


def get_mime_type_from_content_type(content_type: str | None) -> str | None:
    if content_type is None:
        return None
    return content_type.split(';')[0].strip()


def get_host_from_url(url: str) -> str:
    return urlparse(url).hostname


def parse_query_params(url: str) -> list[tuple[str, str]] | None:
    query = urlparse(url).query
    params_dict = parse_qs(query)
    if len(params_dict) == 0:
        return None
    params_list = []
    for k, v in params_dict.items():
        params_list.extend([(k, x) for x in v])
    return params_list
