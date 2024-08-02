from app.base_handler import BaseHandler
from app.consts import Request, Response, ResponseCode
from app.server import app


@app.route("GET", "/echo")
class EchoHandler(BaseHandler):
    def handle(self, request: Request) -> Response:
        return Response(ResponseCode.OK, request.body)
