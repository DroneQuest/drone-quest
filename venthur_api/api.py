from bottle import route, run

from client import build_client, setup_socket, send_message, close
import libardrone
import time

drone = libardrone.ARDrone()


@route('/do/<command>')
def do(command):

    getattr(drone, command)()

    return 'Success'


try:
    run(host='localhost', port=8080)
except:
    drone.land()
    drone.halt()
