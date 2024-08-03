from app.consts import Header, Request, Response, ResponseCode
from app.server import route

from os.path import exists, join


@route("/files/:filename/")
class FilesHandler:
    @classmethod
    def set_directory(cls, directory: str) -> None:
        cls._directory = directory

    @classmethod
    def get(cls, request: Request, filename: str) -> Response:
        filepath = join(cls._directory, filename)
        if not exists(filepath):
            return Response(ResponseCode.NOT_FOUND, [], "")

        # todo: read file content
        with open(filepath, "r") as f:
            content = f.read()

        headers = [
            Header("Content-Type", "application/octet-stream"),
            Header("Content-Length", str(len(content))),
        ]

        return Response(ResponseCode.OK, headers, content)
