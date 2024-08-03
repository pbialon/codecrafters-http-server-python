
from app.consts import Request, Response, ResponseCode
from app.server import route


@route("/files/:filename/")
class FilesHandler:
    @classmethod
    def get(cls, request: Request, filename: str) -> Response:
        return Response(ResponseCode.NOT_FOUND, [], "")