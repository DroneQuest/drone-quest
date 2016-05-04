"""Set up a bottle server to accept post requests commanding the drone."""
from bottle import post, run, hook, get, abort

from venthur_api import libardrone
from server.socket_drone import PORT


@hook('after_request')
def enable_cors(dependency_injection=None):
    """Allow control headers."""
    if dependency_injection:
        response = dependency_injection
    response.headers['Access-Control-Allow-Origin'] = '*'


@get('/navdata')
def navdata(drone=None):
    """Return packet of navdata."""
    drone = GLOBAL_NAME if drone is None else drone
    return drone.navdata


@post('/do/<command>')
def do(command, drone=None):
    """Execute the given command from the route."""
    drone = GLOBAL_DRONE if drone is None else drone
    try:
        print('Command received: {}'.format(command))
        getattr(drone, command)()
        print('Command executed: {}'.format(command))
        return 'Command executed: {}'.format(command)
    except AttributeError:
        print('Bad Command: {}'.format(command))
        abort(404, 'Bad Command: {}'.format(command))


if __name__ == "__main__":
    GLOBAL_DRONE = libardrone.ARDrone()
    try:
        run(host='127.0.0.1', port=PORT)
    finally:
        GLOBAL_DRONE.land()
        GLOBAL_DRONE.halt()
