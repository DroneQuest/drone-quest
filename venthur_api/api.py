"""Set up a bottle server to accept post requests commanding the drone."""
from bottle import post, run, hook, response
# import os
try:
    from venthur_api import libardrone
except ImportError:
    import libardrone

drone = libardrone.ARDrone()


# @route('/')
# def home():
#     with open(os.path.join(HTML_LOC, 'index.html')) as html:
#         return html


@hook('after_request')
def enable_cors():
    """Allow control headers."""
    response.headers['Access-Control-Allow-Origin'] = '*'


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


run(host='localhost', port=8080)
