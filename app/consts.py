from collections import namedtuple

from enum import Enum

CRLF = "\r\n"
HTTP_VERSION = "HTTP/1.1"

RequestMetadata = namedtuple("RequestMetadata", "method path protocol")
Header = namedtuple("Header", "name value")

Request = namedtuple("Request", "request_metadata headers body")


class ResponseCode(Enum):
    OK = 200
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    INTERNAL_SERVER_ERROR = 500


REASON_PHRASE = {
    200: "OK",
    404: "Not Found",
    405: "Method Not Allowed",
    500: "Internal Server Error",
}

Response = namedtuple("Response", "code body")
