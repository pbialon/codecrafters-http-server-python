from app.consts import Request, Response, ResponseCode
from app.http_path import HttpPath
from app.server import route


@route("/echo/:message/")
class EchoHandler:
    @classmethod
    def get(cls, request: Request, message: str) -> Response:
        return Response(ResponseCode.OK, [], message)
