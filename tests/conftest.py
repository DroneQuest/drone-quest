import pytest
from json import dumps


class MockDrone(object):
    # lambdas for brevity
    navdata = dumps({"some": "json"})
    move_left = lambda self: None
    move_right = lambda self: None
    move_forward = lambda self: None
    move_backward = lambda self: None
    move_up = lambda self: None
    move_down = lambda self: None
    turn_left = lambda self: None
    turn_right = lambda self: None
    hover = lambda self: None
    takeoff = lambda self: None
    land = lambda self: None


class MockResponse(object):
    headers = {'Access-Control-Allow-Origin': "default_value!"}


class MockHands(object):
    class palm_velocity(object):
        x = 0
        y = 0
        z = 0

    class palm_position(object):
        x = 0
        y = 0
        z = 0

    grab_strength = 0


class MockFrame(object):
    hands = [MockHands(), MockHands()]


class MockController(object):

    class config(object):
        def save(self):
            return None

    def enable_gesture(self, *args):
        return None

    def frame(self):
        return MockFrame()


class MockLeap(object):
    class Listener(object):
        pass
    class Gesture(object):
        TYPE_SWIPE = "swipe"
        TYPE_KEY_TAP = "key tap"


class Requests(object):

    def get(url):
        return None

    def post(url):
        return None


@pytest.fixture()
def drone():
    return MockDrone()


@pytest.fixture()
def response():
    return MockResponse()


@pytest.fixture()
def controller():
    return MockController()


@pytest.fixture()
def drone_listener():
    from leap_motion.ar_leap import DroneListener
    DroneListener._talk_to_drone = lambda self, route: "Mock Object"
    return DroneListener()


@pytest.fixture()
def requests():
    return Requests


@pytest.fixture()
def history():
    return []
