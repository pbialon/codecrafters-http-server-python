from app.consts import Request, Response, ResponseCode
from app.server import route


@route("/echo")
class EchoHandler:
    @classmethod
    def get(cls, request: Request) -> Response:
        return Response(ResponseCode.OK, request.body)
