import socket
import threading
import click
from concurrent.futures import ThreadPoolExecutor

from app.handlers import *
from app.server import app


def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    try:
        while True:
            request_raw = client_socket.recv(1024)
            if not request_raw:
                break
            response = app.serve(request_raw.decode())
            client_socket.sendall(response.encode())
    finally:
        client_socket.close()
        print(f"Connection with {client_address} closed.")


@click.command()
@click.option("--directory", help="Directory to serve files from.")
def main(directory):
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    if directory:
        FilesHandler.set_directory(directory)

    stop_event = threading.Event()
    max_workers = 5

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        try:
            while not stop_event.is_set():
                client_socket, client_address = server_socket.accept()
                print(f"Connection from: {client_address}")

                executor.submit(handle_client, client_socket, client_address)
        except KeyboardInterrupt:
            print("\nServer is shutting down.\n")
        finally:
            stop_event.set()
            server_socket.close()


if __name__ == "__main__":
    main()
