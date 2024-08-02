# Uncomment this to pass the first stage
import socket

CRLF = '\r\n'

HTTP_VERSION = 'HTTP/1.1'
STATUS_CODE = 200
REASON_PHRASE = 'OK'

def create_response():
    return f'{HTTP_VERSION} {STATUS_CODE} {REASON_PHRASE}{CRLF}{CRLF}'


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    sock, addr = server_socket.accept()
    print("Connection from: ", addr)
    _ = sock.recv(1024)
    
    response = create_response()
    sock.sendall(response.encode())


if __name__ == "__main__":
    main()
