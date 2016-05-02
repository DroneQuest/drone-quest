# -*-coding:utf-8-*-
"""Handle server operations of reading incoming streams and echoing them"""
import socket
from venthur_api import libardrone

DRONE = libardrone.ARDrone()
BUFFER_LENGTH = 1024
PORT = 3000
IP = "127.0.0.1"

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
INCREASE_SPEED = 0x0E
DECREASE_SPEED = 0x0F
TERMINATE = 0x10

COMMANDS_CENTRAL = {
    # PING: DRONE.ping,
    TAKE_OFF: DRONE.takeoff,
    LAND: DRONE.land,
    HOVER: DRONE.hover,
    MOVE_LEFT: DRONE.move_left,
    MOVE_RIGHT: DRONE.move_right,
    MOVE_UP: DRONE.move_up,
    MOVE_DOWN: DRONE.move_down,
    MOVE_FORWARD: DRONE.move_forward,
    MOVE_BACKWARD: DRONE.move_backward,
    TURN_LEFT: DRONE.turn_left,
    TURN_RIGHT: DRONE.turn_right,
    RESET: DRONE.reset,
    CALIBRATE: DRONE.trim,
    INCREASE_SPEED: DRONE.increase_speed,
    DECREASE_SPEED: DRONE.decrease_speed,
    TERMINATE: DRONE.halt
}


# Syntatic Sugars
OK, FAIL = "OK", "FAIL"

STATUS_CODES = {
    OK: "OK",  # Drone executed command correctly
    FAIL: "FAIL",  # Unknown error occurred
}

__AUTHOR__ = ['Munir Ibrahim', 'Norton Pengra', 'Will Weatherford']


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
        part = connection.recv(BUFFER_LENGTH)
        string += part
        if len(part) < BUFFER_LENGTH or len(part) == 0:
            break
    return string.decode('utf-8')


def server_response(string, connection):
    """Send back specified string to specified connection"""
    if isinstance(string, bytes):
        connection.send(string)
    else:
        connection.send(string.encode('utf-8'))


def parse_command(command):
    """Convert the command to hexadecimals."""
    command = hex(int(command, base=16))
    DRONE[command]()


def server():
    """Main server loop."""
    socket = setup_server()
    try:
        while True:
            connection, address = socket.accept()
            command = server_read(connection)
            print("recv:", command)
            server_response(str(STATUS_CODES[OK]), connection)
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
