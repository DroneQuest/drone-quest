"""Set up a bottle server to accept post requests commanding the drone."""
from bottle import post, run, hook, response, get, abort

from venthur_api import libardrone
from server.socket_drone import PORT




@hook('after_request')
def enable_cors():
    """Allow control headers."""
    response.headers['Access-Control-Allow-Origin'] = '*'


@get('/navdata')
def navdata():
    """Return packet of navdata."""
    return drone.navdata


@post('/do/<command>')
def do(command):
    """Execute the given command from the route."""
    try:
        print('Command received: {}'.format(command))
        getattr(drone, command)()
        print('Command executed: {}'.format(command))
        return 'Command executed: {}'.format(command)
    except AttributeError:
        print('Bad Command: {}'.format(command))
        abort(404, 'Bad Command: {}'.format(command))


if __name__ == "__main__":
    drone = libardrone.ARDrone()
    try:
        run(host='127.0.0.1', port=PORT)
    finally:
        drone.land()
        drone.halt()
