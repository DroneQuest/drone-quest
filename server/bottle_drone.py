"""Set up a bottle server to accept post requests commanding the drone."""
from bottle import post, run, hook, response, get

from venthur_api import libardrone


drone = libardrone.ARDrone()


@hook('after_request')
def enable_cors():
    """Allow control headers."""
    response.headers['Access-Control-Allow-Origin'] = '*'


@get('/navdata')
def navdata():
    """Return packet of navdata."""
    return "Navigational data: ..."


@post('/do/<command>')
def do(command):
    """Execute the given command from the route."""
    try:
        print('Command received: {}'.format(command))
        getattr(drone, command)()
        print('Command executed: {}'.format(command))
        return 'Command executed: {}'.format(command)
    except AttributeError:
        # return 404 instead
        print('Bad Command: {}'.format(command))
        return 'Bad Command: {}'.format(command)


run(host='127.0.0.1', port=8080)
