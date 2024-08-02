from app.request import CRLF, Request
from app.response import HTTP_VERSION, REASON_PHRASE


def get(request: Request) -> str:
    if request.request_line.path == "/":
        return f"{HTTP_VERSION} 200 {REASON_PHRASE[200]}{CRLF}{CRLF}"

    return f"{HTTP_VERSION} 404 {REASON_PHRASE[404]}{CRLF}{CRLF}"
