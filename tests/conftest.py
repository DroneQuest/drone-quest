import pytest
from json import dumps
import numpy


class MockDrone(object):
    # lambdas for brevity
    navdata = {"some": "json"}
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
    image = numpy.array(object)


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

    class MockFinger(object):
        is_extended = True

    fingers = [MockFinger(),
               MockFinger(),
               MockFinger(),
               MockFinger(),
               MockFinger()]

    grab_strength = 0


class MockFrame(object):
    hands = [MockHands(), MockHands()]


class MockConfig(object):
    def save(self):
        return True


class MockFinger(object):

    def __init__(self, is_extended):
        self.is_extended = is_extended


class MockController(object):

    _test_only_mock_frame = MockFrame()
    config = MockConfig()
    _test_only_gestures = []


    def enable_gesture(self, gesture):
        self._test_only_gestures.append(gesture)

    def frame(self):
        return self._test_only_mock_frame

    def _test_only_set_grab_strength(self, strength):
        self._test_only_mock_frame.hands[0].grab_strength = strength

    def _test_only_set_palm_velocity(self, x, y, z):
        self._test_only_mock_frame.hands[0].palm_velocity.x = x
        self._test_only_mock_frame.hands[0].palm_velocity.y = y
        self._test_only_mock_frame.hands[0].palm_velocity.z = z

    def _test_only_set_palm_position(self, x, y, z):
        self._test_only_mock_frame.hands[0].palm_position.x = x
        self._test_only_mock_frame.hands[0].palm_position.y = y
        self._test_only_mock_frame.hands[0].palm_position.z = z

    def _test_only_set_finger_positions(self, thumb, index, middle, ring, pinky):
        self._test_only_mock_frame.hands[0].fingers[0] = MockFinger(thumb)
        self._test_only_mock_frame.hands[0].fingers[1] = MockFinger(index)
        self._test_only_mock_frame.hands[0].fingers[2] = MockFinger(middle)
        self._test_only_mock_frame.hands[0].fingers[3] = MockFinger(ring)
        self._test_only_mock_frame.hands[0].fingers[4] = MockFinger(pinky)


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
