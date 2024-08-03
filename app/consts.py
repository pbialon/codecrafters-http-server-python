from collections import namedtuple

from enum import Enum

CRLF = "\r\n"
HTTP_VERSION = "HTTP/1.1"

RequestMetadata = namedtuple("RequestMetadata", "method path protocol encoding")
Header = namedtuple("Header", "name value")

Request = namedtuple("Request", "metadata headers body")


class ResponseCode(Enum):
    OK = 200
    CREATED = 201
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    INTERNAL_SERVER_ERROR = 500


REASON_PHRASE = {
    200: "OK",
    201: "Created",
    404: "Not Found",
    405: "Method Not Allowed",
    500: "Internal Server Error",
}

class Response:
    def __init__(self, code: ResponseCode, headers: list[Header] = [], body: str = ""):
        self.code = code
        self.headers = headers
        self.body = body

