import socket

from app.handlers.router import prepare_response
from app.request import parse_request



def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    sock, addr = server_socket.accept()
    print("Connection from: ", addr)
    data = sock.recv(1024)
    request = parse_request(data.decode())
    
    response = prepare_response(request)
    sock.sendall(response.encode())


if __name__ == "__main__":
    main()
