from app.base_handler import BaseHandler
from app.consts import Request, Response, ResponseCode
from app.server import route


@route("/echo")
class EchoHandler(BaseHandler):
    @classmethod
    def get(cls, request: Request) -> Response:
        return Response(ResponseCode.OK, request.body)
