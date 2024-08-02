# Uncomment this to pass the first stage
import socket

from app.request import parse_request
from app.response import create_response



def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    sock, addr = server_socket.accept()
    print("Connection from: ", addr)
    data = sock.recv(1024)
    request = parse_request(data.decode())
    
    response = create_response(request)
    sock.sendall(response.encode())


if __name__ == "__main__":
    main()
