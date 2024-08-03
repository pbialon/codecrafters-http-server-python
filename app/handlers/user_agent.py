

from app.consts import Header, Request, Response, ResponseCode
from app.server import route


@route("/user-agent")
class UserAgentHandler:
    @classmethod
    def get(cls, request: Request) -> Response:
        user_agent = cls._get_user_agent(request)
        headers = [
            Header("Content-Type", "text/plain"),
        ]
        return Response(ResponseCode.OK, headers, user_agent)
    
    @classmethod
    def _get_user_agent(cls, request: Request) -> str:
        for header in request.headers:
            if header.name == "User-Agent":
                return header.value