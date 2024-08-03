import inspect
from app.consts import Header, Request, RequestMetadata
from app.consts import CRLF, REASON_PHRASE, Response, ResponseCode
from app.encoders.gzip import GzipEncoder
from app.http_path import HttpPath


class Server:
    SUPPORTED_ENCODINGS = {"gzip": GzipEncoder()}

    def __init__(self):
        self._handlers = {}

    def process(self, raw_request: str) -> str:
        request = self._parse_request(raw_request)

        response = self._handle_request(request)
        return self._to_raw_response(response, request.metadata.encoding)

    def register_handler(self, method: str, path: HttpPath, handler) -> None:
        self._handlers[(method, path)] = handler

    def _parse_request(self, raw_request: str) -> Request:
        parts = raw_request.split(CRLF)
        request_metadata_raw = parts[0]
        body_raw = parts[-1]
        headers_raw = parts[1:-1]
        method, path, protocol = request_metadata_raw.split()

        headers = [Header(*header_raw.split(": ")) for header_raw in headers_raw[:-1]]

        encoding = self._get_encoding(headers)
        metadata = RequestMetadata(method, path, protocol, encoding)

        return Request(metadata, headers, body_raw)

    def _get_encoding(self, headers: list[Header]) -> str | None:
        header = self._find_header(headers, "Accept-Encoding")
        if not header:
            return None

        accepted_encodings = header.value.split(", ")
        return self._find_supported_encoding(accepted_encodings)

    def _find_supported_encoding(self, client_encodings: str) -> str | None:
        for encoding in client_encodings:
            if encoding in self.SUPPORTED_ENCODINGS:
                return encoding
        return None

    def _find_header(self, headers: list[Header], name: str) -> Header | None:
        for header in headers:
            if header.name == name:
                return header
        return None

    def _handle_request(self, request: Request):
        method = request.metadata.method
        path = request.metadata.path
        for (handler_method, handler_path), handler in self._handlers.items():
            if method == handler_method and handler_path.match(path):
                dynamic_kwargs = handler_path.parse(path)
                return handler(request, **dynamic_kwargs)
        return self._not_found(request)

    def _to_raw_response(self, response: Response, encoding: str = None) -> str:
        code = response.code.value  # enum
        status_line = f"HTTP/1.1 {code} {REASON_PHRASE[code]}"
        headers = "".join(
            [f"{header.name}: {header.value}{CRLF}" for header in response.headers]
        )
        body = response.body

        if encoding:
            headers += f"Content-Encoding: {encoding}{CRLF}"
            body = self.SUPPORTED_ENCODINGS[encoding](body)
        
        if body:
            headers += f"Content-Length: {len(body)}{CRLF}"

        return (
            f"{status_line}"
            f"{CRLF}"
            f"{headers}"
            f"{CRLF}"
            f"{body}"
        )

    @staticmethod
    def _not_found(request: Request) -> Response:
        return Response(ResponseCode.NOT_FOUND)

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
