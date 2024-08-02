from functools import wraps
import inspect
from collections import defaultdict, namedtuple
from app.consts import Header, Request, RequestMetadata
from app.consts import CRLF, REASON_PHRASE, Response, ResponseCode
from app.http_path import HttpPath

class Server:
    def __init__(self):
        self._handlers = {}

    def serve(self, raw_request: str) -> str:
        request = self._parse_request(raw_request)
        method = request.request_metadata.method
        path = request.request_metadata.path

        handle = self._handle(method, path)
        response = handle(request)
        return self._to_raw_response(response)

    def register_handler(self, method: str, path: HttpPath, handler) -> None:
        self._handlers[(method, path)] = handler

    def _parse_request(self, raw_request: str) -> Request:
        parts = raw_request.split(CRLF)
        request_metadata_raw = parts[0]
        body_raw = parts[-1]
        headers_raw = parts[1:-1]
        method, path, protocol = request_metadata_raw.split()

        metadata = RequestMetadata(method, path, protocol)
        headers = [Header(*header_raw.split(": ")) for header_raw in headers_raw[:-1]]

        return Request(metadata, headers, body_raw)

    def _handle(self, method: str, path: str):
        for (handler_method, handler_path), handler in self._handlers.items():
            if method == handler_method and handler_path.match(path):
                return handler
        return self._not_found

    def _to_raw_response(self, response: Response) -> str:
        code = response.code.value  # enum
        return f"HTTP/1.1 {code} {REASON_PHRASE[code]}{CRLF}{response.body}{CRLF}"

    @staticmethod
    def _not_found(request: Request) -> Response:
        return Response(ResponseCode.NOT_FOUND, "")


app = Server()


def route(raw_path: str):
    http_methods = ["GET", "POST", "PUT", "DELETE"]

    def decorator(cls):
        for name, func in inspect.getmembers(cls, predicate=inspect.ismethod):
            method = name.upper()
            if method not in http_methods:
                continue
            path = HttpPath(raw_path)
            app.register_handler(method, path, func)
                
        return cls

    return decorator
