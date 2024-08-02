from app.handlers.get import get
from app.request import CRLF, Request
from app.response import HTTP_VERSION, REASON_PHRASE


ALLOWED_METHODS = {"GET"}
ALLOWED_PATHS = {"/"}


def prepare_response(request: Request) -> str:
    if request.request_line.method not in ALLOWED_METHODS:
        return f"{HTTP_VERSION} 405 {REASON_PHRASE[405]}{CRLF}{CRLF}"

    return get(request)
