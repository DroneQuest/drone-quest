"""Set up a bottle server to accept post requests commanding the drone."""
from bottle import post, run, route
import libardrone
import os

drone = libardrone.ARDrone()

HTML_LOC = '/home/will/401d2/drone-client/dist'


@route('/')
def home():
    with open(os.path.join(HTML_LOC, 'index.html')) as html:
        return html


@route('/do/<command>')
def do(command):
    """Execute the given command from the route."""
    try:
        print('Command received: {}'.format(command))
        getattr(drone, command)()
        print('Command executed: {}'.format(command))
        return 'Command executed: {}'.format(command)
    except AttributeError:
        print('Bad Command: {}'.format(command))
        return 'Bad Command: {}'.format(command)


run(host='localhost', port=8080)
