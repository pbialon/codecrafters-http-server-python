import inspect
from collections import namedtuple
from app.base_handler import BaseHandler
from app.consts import Header, Request, RequestLine
from app.consts import CRLF, REASON_PHRASE, Response, ResponseCode


class Server:
    def __init__(self):
        self._handlers = {}
        self._not_found_handler = NotFound404Handler()

    def serve(self, raw_request: str) -> str:
        request = self._parse_request(raw_request)
        method = request.request_line.method
        path = self._sanitize_path(request.request_line.path)

        handle = self._handler(method, path)
        response = handle(request)
        return self._to_raw_response(response)

    def register_handler(self, method: str, path: str, handler: BaseHandler) -> None:
        self._handlers[(method, path)] = handler

    def _sanitize_path(self, path: str) -> str:
        if not path.startswith("/"):
            raise ValueError("Path must start with /")
        return path if path.endswith("/") else f"{path}/"

    def _parse_request(self, raw_request: str) -> Request:
        parts = raw_request.split(CRLF)
        request_line_raw = parts[0]
        body_raw = parts[-1]
        headers_raw = parts[1:-1]
        method, path, protocol = request_line_raw.split()

        req = RequestLine(method, path, protocol)
        headers = [Header(*header_raw.split(": ")) for header_raw in headers_raw[:-1]]

        return Request(req, headers, body_raw)

    def _handler(self, method: str, path: str) -> BaseHandler:
        return self._handlers.get((method, path), self._not_found_handler)

    def _to_raw_response(self, response: Response) -> str:
        code = response.code.value  # enum
        return f"HTTP/1.1 {code} {REASON_PHRASE[code]}{CRLF}{response.body}{CRLF}"


class NotFound404Handler(BaseHandler):
    def handle(self, request: Request) -> Response:
        return Response(ResponseCode.NOT_FOUND, "")


app = Server()


def route(path: str):
    http_methods = ["GET", "POST", "PUT", "DELETE"]

    def decorator(cls: BaseHandler):
        for name, func in inspect.getmembers(cls, predicate=inspect.ismethod):
            method = name.upper()
            if method in http_methods:
                app.register_handler(method, path, func)
        return cls

    return decorator
