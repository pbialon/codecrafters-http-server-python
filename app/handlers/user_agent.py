

from app.consts import Request, Response, ResponseCode
from app.server import route


@route("/user-agent")
class UserAgentHandler:
    @classmethod
    def get(cls, request: Request) -> Response:
        user_agent = request.headers.get("User-Agent")
        headers = [
            ("Content-Type", "text/plain"),
            ("Content-Length", str(len(user_agent))),
        ]
        return Response(ResponseCode.OK, headers, user_agent)