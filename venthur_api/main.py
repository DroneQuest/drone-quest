# -*-coding:utf-8-*-
"""Handle server operations of reading incoming streams and echoing them."""
import socket
import libardrone


BUFFER_LENGTH = 1024
PORT = 3000
IP = "127.0.0.1"

PING = 0x00
TAKE_OFF = "A"
LAND = "B"
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
    TAKE_OFF: 'takeoff',
    LAND: 'land',
    HOVER: 'hover',
    MOVE_LEFT: 'move_left',
    MOVE_RIGHT: 'move_right',
    MOVE_UP: 'move_up',
    MOVE_DOWN: 'move_down',
    MOVE_FORWARD: 'move_forward',
    MOVE_BACKWARD: 'move_backward',
    TURN_LEFT: 'turn_left',
    TURN_RIGHT: 'turn_right',
    RESET: 'reset',
    CALIBRATE: 'trim',
    INCREASE_SPEED: 'increase_speed',
    DECREASE_SPEED: 'decrease_speed',
    TERMINATE: 'halt',
}


# Syntatic Sugars
OK, FAIL = "OK", "FAIL"

STATUS_CODES = {
    OK: "OK",  # Drone executed command correctly
    FAIL: "FAIL",  # Unknown error occurred
}

__AUTHOR__ = ['Munir Ibrahim', 'Norton Pengra', 'Will Weatherford']


def setup_server():
    """Build a socket object on localhost and specified port."""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    server.bind((IP, PORT))
    server.listen(5)
    return server


def server_listen(server):
    """Accept connections from the client."""
    conn, addr = server.accept()
    return (conn, addr)


def server_read(connection):
    """Read and parse message from client."""
    string = ''.encode('utf-8')
    while True:
        part = connection.recv(BUFFER_LENGTH)
        string += part
        if len(part) < BUFFER_LENGTH or len(part) == 0:
            break
    return string.decode('utf-8')


def server_response(string, connection):
    """Send back specified string to specified connection."""
    if isinstance(string, bytes):
        connection.send(string)
    else:
        connection.send(string.encode('utf-8'))


def parse_command(command):
    """Convert the command to hexadecimals."""
    # command = hex(int(command, base=16))
    return COMMANDS_CENTRAL[command]


def server():
    """Main server loop."""
    drone = libardrone.ARDrone()
    print('Done setting up drone.')
    socket = setup_server()
    try:
        while True:
            connection, address = socket.accept()
            command_code = server_read(connection)
            print("received command code: {}".format(command_code))
            command_name = parse_command(command_code)
            print("Doing command name: {}".format(command_name))
            command = getattr(drone, command_name)
            command()
            server_response(str(STATUS_CODES[OK]), connection)
            connection.close()
    except KeyboardInterrupt:
        print("Closing the server!")
        try:
            connection.close()
        except NameError:
            pass
    finally:
        drone.halt()
        socket.close()

if __name__ == "__main__":
    server()
