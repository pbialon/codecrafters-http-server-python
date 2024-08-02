
from logging import Handler
from app.consts import Request, Response, ResponseCode
from app.server import app

@app.route("GET", "/")
class GetHandler(Handler):
    @classmethod
    def handle(cls, request: Request) -> Response:
        return Response(ResponseCode.OK, "")