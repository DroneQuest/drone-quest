# -*- coding: utf-8 -*-
"""Dummy Test Client."""
import socket
from main import PORT, BUFFER_LENGTH


def setup_socket():
    """Gather required information for building a socket object."""
    info = socket.getaddrinfo('127.0.0.1', PORT)
    return [i for i in info if i[1] == socket.SOCK_STREAM][0]


def build_client(socket_details):
    """Use given information to build a socket object."""
    client = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    client.settimeout(1)
    return client


def close(socket):
    """Close socket gracefully."""
    socket.close()


def send_message(socket, message):
    """Send a scrubbed message to the server."""
    socket.connect(('127.0.0.1', PORT))
    if hasattr(message, 'encode'):
        socket.sendall(message.encode('utf-8'))
    else:
        socket.sendall(bytes(message))


def get_reply(client):
    """Get reply from the server."""
    chunks = []
    while True:
        chunk = client.recv(BUFFER_LENGTH)
        chunks.append(chunk)
        if len(chunk) < BUFFER_LENGTH or len(chunk) == 0:
            return (b''.join(chunks)).decode('utf-8').replace('\r', '')


if __name__ == "__main__":
    client = build_client(setup_socket())
    while True:
        send_message(client, input("Command: "))
    close(client)
