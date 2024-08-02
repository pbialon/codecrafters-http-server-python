from app.consts import Request, Response


class BaseHandler:
    @classmethod
    def handle(cls, request: Request) -> Response:
        raise NotImplementedError
