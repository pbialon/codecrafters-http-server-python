from app.consts import Header, Request, Response, ResponseCode
from app.http_path import HttpPath
from app.server import route


@route("/echo/:message/")
class EchoHandler:
    @classmethod
    def get(cls, request: Request, message: str) -> Response:
        headers = [
            Header("Content-Type", "text/plain"),
            Header("Content-Length", str(len(message))),
        ]
        return Response(ResponseCode.OK, headers, message)
