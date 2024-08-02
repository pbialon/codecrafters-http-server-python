
from app.request import Request


CRLF = '\r\n'
HTTP_VERSION = 'HTTP/1.1'


REASON_PHRASE = {
    200: 'OK',
    404: 'Not Found',
    405: 'Method Not Allowed',
    500: 'Internal Server Error'
}

def create_response(request: Request) -> str:
    if request.request_line.method != 'GET':
        # no support for other methods now
        return f'{HTTP_VERSION} 405 {REASON_PHRASE[405]}{CRLF}{CRLF}'
    
    return handle_get(request)
    

def handle_get(request: Request) -> str:
    return f'{HTTP_VERSION} 200 {REASON_PHRASE[200]}{CRLF}{CRLF}'