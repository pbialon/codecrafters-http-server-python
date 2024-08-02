
from logging import Handler
from app.consts import Request, Response, ResponseCode
from app.server import route

@route("/")
class GetHandler(Handler):
    @classmethod
    def get(cls, request: Request) -> Response:
        return Response(ResponseCode.OK, "")