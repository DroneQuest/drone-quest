"""Set up a bottle server to accept post requests commanding the drone."""
from bottle import post, run, hook, get, abort
from bottle import response as response_module
import json
import webbrowser
from adetaylor_api.libardrone import libardrone

HTTP = 'http://'
IP = '127.0.0.1'
PORT = 3001

# Need to startup on page served by node at port 8080
DRONE_SERVER_ADDRESS = HTTP + ':'.join((IP, str(PORT)))


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
    if image.any():
        print('IMGDATA HAS VALUE')
        print(drone.image)
    else:
        print('IMGDATA IS NULL:')
    # response.content_type = 'image/x-rgb'
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


def main():
    global GLOBAL_DRONE
    GLOBAL_DRONE = libardrone.ARDrone2()
    try:
        run(host=IP, port=PORT)
        webbrowser.open_new_tab(DRONE_SERVER_ADDRESS)
    finally:
        GLOBAL_DRONE.land()
        GLOBAL_DRONE.halt()


if __name__ == "__main__":
    main()
