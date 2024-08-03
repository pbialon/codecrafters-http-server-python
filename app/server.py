import inspect
from app.consts import Header, Request, RequestMetadata
from app.consts import CRLF, REASON_PHRASE, Response, ResponseCode
from app.encoders.gzip import GzipEncoder
from app.encoders.utf8 import Utf8Encoder
from app.http_path import HttpPath


class Server:
    def __init__(self):
        self._handlers = {}

    def process(self, raw_request: bytes) -> str:
        request = self._parse_request(raw_request.decode())

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

        encoding = Encodings.get(headers)
        metadata = RequestMetadata(method, path, protocol, encoding)

        return Request(metadata, headers, body_raw)

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
        
        body = Encodings.encode(body, encoding)
        if body:
            headers += f"Content-Length: {len(body)}{CRLF}"
            
        response_without_body = (
            f"{status_line}"
            f"{CRLF}"
            f"{headers}"
            f"{CRLF}"
        ).encode()
        
        return response_without_body + body

    @staticmethod
    def _not_found(request: Request) -> Response:
        return Response(ResponseCode.NOT_FOUND)
    
    
class Encodings:
    SUPPORTED_ENCODINGS = {"gzip": GzipEncoder()}
    DEFAULT_ENCODER = Utf8Encoder()
    ACCEPT_ENCODING_HEADER = "Accept-Encoding"

    @classmethod
    def get(cls, headers: list[Header]) -> str | None:
        header = cls._find_header(headers, cls.ACCEPT_ENCODING_HEADER)
        if not header:
            return None

        accepted_encodings = header.value.split(", ")
        return cls._find_supported_encoding(accepted_encodings)
    
    @classmethod
    def encode(cls, body: str, encoding: str) -> str:
        encoder = cls.SUPPORTED_ENCODINGS.get(encoding, cls.DEFAULT_ENCODER)
        return encoder(body)

    @classmethod
    def _find_supported_encoding(cls, client_encodings: str) -> str | None:
        for encoding in client_encodings:
            if encoding in cls.SUPPORTED_ENCODINGS:
                return encoding
        return None

    @classmethod
    def _find_header(cls, headers: list[Header], name: str) -> Header | None:
        for header in headers:
            if header.name == name:
                return header
        return None

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
