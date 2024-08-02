import socket

from app.handlers import *
from app.server import app

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    sock, addr = server_socket.accept()
    print("Connection from: ", addr)
    request_raw = sock.recv(1024)

    response = app.serve(request_raw.decode())
    sock.sendall(response.encode())


if __name__ == "__main__":
    main()
