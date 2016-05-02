# -*-coding:utf-8-*-
"""Handle server operations of reading incoming streams and echoing them"""
import socket

buffer_length = 1024
PORT = 3000
IP = "0.0.0.0"

PING = 0x00
TAKE_OFF = 0x01
LAND = 0x02
HOVER = 0x03
MOVE_LEFT = 0x04
MOVE_RIGHT = 0x05
MOVE_UP = 0x06
MOVE_DOWN = 0x07
MOVE_FORWARD = 0x08
MOVE_BACKWARD = 0x09
TURN_LEFT = 0x0A
TURN_RIGHT = 0x0B
RESET = 0x0C
CALIBRATE = 0x0D
SPEED = 0x0E
TERMINATE = 0x10


def setup_server():
    """Build a socket object on localhost and specified port"""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    server.bind((IP, PORT))
    server.listen(5)
    return server


def server_listen(server):
    """Accept connections from the client"""
    conn, addr = server.accept()
    return (conn, addr)


def server_read(connection):
    """Read and parse message from client"""

    string = ''.encode('utf-8')
    while True:
        part = connection.recv(buffer_length)
        string += part
        if len(part) < buffer_length or len(part) == 0:
            break
    return string.decode('utf-8')


def server_response(string, connection):
    """Send back specified string to specified connection"""
    if isinstance(string, bytes):
        connection.send(string)
    else:
        connection.send(string.encode('utf-8'))


def server():
    """Main server loop."""
    try:
        socket = setup_server()
        while True:
            connection, address = socket.accept()
            command = server_read(connection)
            print("recv:", command)
            connection.close()
    except KeyboardInterrupt:
        print("Closing the server!")
        try:
            connection.close()
        except NameError:
            pass
    finally:
        socket.close()

if __name__ == "__main__":
    server()
