"""Set up a bottle server to accept post requests commanding the drone."""
from bottle import post, run
import libardrone

drone = libardrone.ARDrone()


@post('/do/<command>')
def do(command):
    """Execute the given command from the route."""
    try:
        getattr(drone, command)()
        return 'Command executed'
    except AttributeError:
        return 'Bad Command'


run(host='localhost', port=8080)
