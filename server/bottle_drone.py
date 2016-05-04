"""Set up a bottle server to accept post requests commanding the drone."""
from bottle import post, run, hook, get, abort
from bottle import response as response_module
import json
from venthur_api import libardrone
PORT = 3000


@hook('after_request')
def enable_cors(dependency_injection=None):
    """Allow control headers."""
    response = dependency_injection if dependency_injection else response_module
    response.headers['Access-Control-Allow-Origin'] = '*'


@get('/imgdata')
def imgdata(drone=None):
    """Return the current drone image."""
    drone = GLOBAL_DRONE if drone is None else drone
    print(type(drone.image))
    # should be type bytes, not unicode
    image = drone.image
    if image:
        print('IMGDATA HAS VALUE')
        print(drone.image)
    # else:
    #     print('IMGDATA IS NULL:')
    response_module.content_type = 'image/x-rgb'
    return drone.image


@get('/navdata')
def navdata(drone=None):
    """Return packet of navdata."""
    drone = GLOBAL_DRONE if drone is None else drone
    response_module.content_type = 'application/json'
    return json.dumps(drone.navdata, ensure_ascii=False)


@post('/do/<command>')
def do(command, drone=None):
    """Execute the given command from the route."""
    drone = GLOBAL_DRONE if drone is None else drone
    try:
        print('Command received: {}'.format(command))
        getattr(drone, command)()
        print('Command executed: {}'.format(command))
        response_module.content_type = 'application/json'
        return json.dumps(drone.navdata, ensure_ascii=False)
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
