
from app.consts import Request, Response, ResponseCode
from app.server import route

@route("/")
class GetHandler:
    @classmethod
    def get(cls, request: Request) -> Response:
        return Response(ResponseCode.OK, "")