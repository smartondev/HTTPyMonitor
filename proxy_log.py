import hashlib
import os
import sys
import time
from enum import Enum
from multiprocessing import Queue
from queue import Empty

from multidict import CIMultiDict, CIMultiDictProxy

from http_helper import get_mime_type_from_content_type
from preview_formatter import Formatter


class ProxyLogPhase(Enum):
    REQUEST_HEAD = 'requestHead'
    REQUEST_BODY_READING = 'requestBodyReading'
    REQUEST_FORWARD = 'requestForward'
    RESPONSE_BODY_READING = 'responseBodyReading'
    RESPONSE_BODY_READ = 'responseBodyRead'


class ContentItem:
    def __init__(self, content: bytes | None = None, filepath: str | None = None, content_type: str | None = None):
        self._content = content
        self._content_type = content_type
        self._filepath = filepath
        if self._content is not None:
            self._length = len(content)
            hasher = hashlib.md5()
            hasher.update(content)
            self._hash = hasher.hexdigest()
        elif filepath is not None:
            self._length = os.path.getsize(filepath)
            # TODO fix hash
            self._hash = os.path.basename(filepath)
        else:
            self._length = 0
            self._hash = None

    def content_type(self) -> str | None:
        return self._content_type

    def content(self, take: int = sys.maxsize, skip: int = 0) -> bytes:
        if self._content is not None:
            if take == sys.maxsize and skip == 0:
                return self._content
            return self._content[skip:take]
        elif self._filepath is not None:
            with open(self._filepath, 'rb') as file:
                file.seek(skip)
                if take == sys.maxsize:
                    return file.read()
                if take == 0:
                    return b''
                return file.read(take)
        else:
            return b''

    def hash(self) -> str:
        return self._hash

    def length(self) -> int:
        return self._length

    def __eq__(self, other):
        return isinstance(other, ContentItem) and self._hash == other._hash


class ContentStorage:
    def __init__(self, path: str):
        self._path = path
        self._create_path(path)

    def store(self, content: ContentItem) -> ContentItem:
        if content.length() == 0:
            return content
        # TODO store pretty type content
        content_hash = content.hash()
        file_path = self._gen_path(content_hash)
        if not os.path.exists(file_path):
            self._create_path(os.path.dirname(file_path))
            with open(file_path, 'wb') as file:
                file.write(content.content())
        else:
            os.utime(file_path)
        return ContentItem(filepath=file_path)

    def read(self, content_hash: str, take: int = sys.maxsize, skip: int = 0) -> bytes | None:
        # TODO read pretty type content
        file_path = self._gen_path(content_hash)
        if not os.path.exists(file_path):
            return None
        with open(file_path, 'rb') as file:
            if skip > 0:
                file.seek(skip)
            if take == sys.maxsize:
                return file.read()
            if take == 0:
                return b''
            return file.read(take)

    def garbage(self):
        time_limit = 60 * 60
        counter = 0
        for root, dirs, files in os.walk(self._path):
            for file in files:
                file_path = os.path.join(root, file)
                if time.time() - os.path.getmtime(file_path) > time_limit:
                    os.remove(file_path)
                    counter = counter + 1
        print(f'Garbage collected {counter} files')

    def _gen_path(self, content_hash: str) -> str:
        # TODO use content-type
        return os.path.join(self._path, content_hash[0:2], content_hash)

    def _create_path(self, path: str):
        os.makedirs(path, exist_ok=True)


class HttpHeader:
    def __init__(self, name: str, value: str):
        self._name = name.lower()
        self._value = value

    def name(self) -> str:
        return self._name

    def value(self) -> str:
        return self._value

    def to_map(self) -> dict:
        return {'name': self._name, 'value': self._value}


class HttpHeaders(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def create_by(headers: dict | CIMultiDict | CIMultiDictProxy[str]) -> 'HttpHeaders':
        instance = HttpHeaders()
        instance.put_all(headers.items())
        return instance

    # def remove_all(self, name: str):
    #     name = name.lower()
    #     self[:] = [header for header in self if header.name() != name]
    #
    # def append(self, __object):
    #     if isinstance(__object, tuple):
    #         __object = HttpHeader(__object[0], __object[1])
    #     if not isinstance(__object, HttpHeader):
    #         raise ValueError('Only HttpHeader can be appended')
    #     super().append(__object)

    def put_all(self, items):
        for (k, v) in items:
            self.append(HttpHeader(k, v))

    def get(self, key: str) -> list | None:
        key = key.lower()
        found: bool = False
        for header in self:
            if header.name() == key:
                found = True
                yield header.value()
        if not found:
            return None

    def content_type(self) -> str | None:
        for value in self.get('content-type'):
            return value

    def to_map(self) -> list[dict]:
        return [header.to_map() for header in self]


class RequestEntry:
    def __init__(self, phase: ProxyLogPhase, id: int | None = None, start_time: float | None = None):
        now = time.time()
        self._time: float = start_time
        self._last_time: float | None = now
        self._id = id if id is not None else int(self._time * 1000)
        self._phase: ProxyLogPhase = phase
        self.request_method: str | None = None
        self.request_url: str | None = None
        self._request_headers: HttpHeaders | None = None
        self.request_query_parameters: list[tuple[str, str]] | None = None
        self._request_body: ContentItem | None = None
        self._request_body_mime_type: str | None = None
        self.forward_destination: str | None = None
        self.response_status: int | None = None
        self._response_headers: HttpHeaders | None = None
        self._response_body: ContentItem | None = None
        self._response_body_mime_type: str | None = None

    def mutate(self, phase: ProxyLogPhase) -> 'RequestEntry':
        instance = RequestEntry(
            phase=phase,
            id=self._id,
        )
        return instance

    def with_request_headers(self, headers: HttpHeaders) -> 'RequestEntry':
        self._request_headers = headers
        return self

    def with_response_headers(self, headers: HttpHeaders) -> 'RequestEntry':
        self._response_headers = headers
        return self

    def with_request_body(self, content: bytes | None, content_type: str | None) -> 'RequestEntry':
        self._request_body = ContentItem(content=content, content_type=content_type)
        self._request_body_mime_type = get_mime_type_from_content_type(content_type)
        return self

    def with_response_body(self, content: bytes | None, content_type: str | None) -> 'RequestEntry':
        self._response_body = ContentItem(content=content, content_type=content_type)
        self._response_body_mime_type = get_mime_type_from_content_type(content_type)
        return self

    def get_request_body(self) -> ContentItem | None:
        return self._request_body

    def get_response_body(self) -> ContentItem | None:
        return self._response_body

    @staticmethod
    def _encode_content(content: ContentItem | None) -> dict | str | None:
        if content is None:
            return None
        preview_content = None
        content_type = content.content_type()
        if content_type is not None:
            preview_content = Formatter().format(content_type, content.content())
        response: dict = {
            'length': content.length(),
            'hash': content.hash(),
            'contentType': content_type,
            'previewContent': preview_content,
        }
        return response

    @staticmethod
    def _encode_query_parameters(query_parameters: list[tuple[str, str]]) -> list[dict[str, str]]:
        return [{'name': k, 'value': v} for k, v in query_parameters]

    def to_map(self) -> dict:
        request: dict = {
            'method': self.request_method,
            'url': self.request_url,
            'headers': None if self._request_headers is None else self._request_headers.to_map(),
        }
        if self.request_query_parameters is not None:
            request['queryParameters'] = self._encode_query_parameters(self.request_query_parameters)
        if self._request_body is not None:
            encoded_content = self._encode_content(self._request_body)
            encoded_content.update({'mimeType': self._request_body_mime_type})
            request['body'] = self._clean_dict(encoded_content)
        response: dict = {
            'status': self.response_status,
            'headers': None if self._response_headers is None else self._response_headers.to_map(),
        }
        # print('response:', response)
        if self._response_body is not None:
            encoded_content = self._encode_content(self._response_body)
            encoded_content.update({'mimeType': self._response_body_mime_type})
            response['body'] = self._clean_dict(encoded_content)
        result = {
            'phase': self._phase.value,
            'time': self._time,
            'lastTime': self._last_time,
            'id': self._id,
            'request': self._clean_dict(request),
            'response': self._clean_dict(response),
            'forwardDestination': self.forward_destination,
        }

        result_clean = self._clean_dict(result)
        # print('result_clean:', result_clean)
        return result_clean

    @staticmethod
    def _clean_dict(obj: dict) -> dict | None:
        result = {k: v for k, v in obj.items() if v is not None}
        if len(result) == 0:
            return None
        return result

    def __eq__(self, other):
        return isinstance(other, RequestEntry) and self._id == other._id

    def __str__(self):
        return str(self.to_map())


class ProxyLog:
    def __init__(self, queue_store: Queue, content_storage: ContentStorage):
        self._queue: Queue = queue_store
        self._content_storage: ContentStorage = content_storage

    def get_content_storage(self) -> ContentStorage:
        return self._content_storage

    def new_entry(self, method: str, url: str, headers: HttpHeaders,
                  query_parameters: list[tuple[str, str]]) -> RequestEntry:
        entry = RequestEntry(
            phase=ProxyLogPhase.REQUEST_HEAD,
            start_time=time.time(),
        )
        entry.request_url = url
        entry.request_method = method
        entry.request_query_parameters = query_parameters
        entry.with_request_headers(headers)
        self.put(entry)
        return entry

    def put(self, entry: RequestEntry):
        if entry.get_request_body() is not None:
            self._content_storage.store(entry.get_request_body())
        if entry.get_response_body() is not None:
            self._content_storage.store(entry.get_response_body())
        self._queue.put_nowait(entry)

    def first_and_remove(self) -> RequestEntry | None:
        try:
            return self._queue.get_nowait()
        except Empty:
            return None
