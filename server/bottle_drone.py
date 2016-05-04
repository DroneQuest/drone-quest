"""Set up a bottle server to accept post requests commanding the drone."""
from bottle import post, run, hook, response, get, abort
import json
from adetaylor_api.libardrone import libardrone


drone = libardrone.ARDrone2()


@hook('after_request')
def enable_cors():
    """Allow control headers."""
    response.headers['Access-Control-Allow-Origin'] = '*'


@get('/imgdata')
def imgdata():
    """Return the current drone image."""
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
def navdata():
    """Return packet of navdata."""
    # print('NAVDATA:')
    # print(drone.navdata)
    response.content_type = 'application/json'
    return json.dumps(drone.navdata, ensure_ascii=False)


@post('/do/<command>')
def do(command):
    """Execute the given command from the route."""
    try:
        print('Command received: {}'.format(command))
        getattr(drone, command)()
        print('Command executed: {}'.format(command))
        response.content_type = 'application/json'
        return json.dumps(drone.navdata, ensure_ascii=False)
    except AttributeError:
        print('Bad Command: {}'.format(command))
        abort(404, 'Bad Command: {}'.format(command))


try:
    run(host='127.0.0.1', port=8080)
finally:
    drone.land()
    drone.halt()
