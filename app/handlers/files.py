
from app.consts import Request, Response, ResponseCode
from app.server import route

from os.path import exists


@route("/files/:filename/")
class FilesHandler:
    @classmethod
    def get(cls, request: Request, filename: str) -> Response:
        if not exists(filename):
            return Response(ResponseCode.NOT_FOUND, [], "")
        
        #todo: read file content
        
        return Response(ResponseCode.NOT_FOUND, [], "")