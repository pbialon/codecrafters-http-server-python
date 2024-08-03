import socket
import threading
from typing import Any
import click
from concurrent.futures import ThreadPoolExecutor

from app.handlers import *
from app.server import app


def handle_client(client_socket, client_address):
    try:
        while True:
            request_raw = client_socket.recv(1024)
            if not request_raw:
                break
            response = app.process(request_raw)
            client_socket.sendall(response)
    finally:
        client_socket.close()


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

                executor.submit(handle_client, client_socket, client_address)
        except KeyboardInterrupt:
            print("\nServer is shutting down.\n")
        finally:
            stop_event.set()
            server_socket.close()


if __name__ == "__main__":
    main()
