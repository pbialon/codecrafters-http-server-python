
CRLF = '\r\n'

from collections import namedtuple

RequestLine = namedtuple('RequestLine', 'method path protocol')
Header = namedtuple('Header', 'name value')

Request = namedtuple('Request', 'request_line headers body')

def parse_request(raw_request: str) -> Request:
    parts = raw_request.split(CRLF)
    request_line_raw = parts[0]
    body_raw = parts[-1]
    headers_raw = parts[1:-1]
    method, path, protocol = request_line_raw.split()

    req = RequestLine(method, path, protocol)
    headers = [Header(*header_raw.split(': ')) for header_raw in headers_raw[:-1]]
    
    return Request(req, headers, body_raw)