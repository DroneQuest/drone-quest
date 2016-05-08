"""Mocks for a fake drone controller."""
import pytest
# from json
import numpy

print('in conftest')

class MockDrone(object):
    """
    Fake movement that the fake drone.

    Lambdas for brevity.
    """

    image = numpy.array(object)
    navdata = {"some": "json"}

    def move_right(self):
        """Fake Drone moves right."""
        return None

    def move_left(self):
        """Fake Drone moves left."""
        return None

    def move_forward(self):
        """Fake Drone moves forward."""
        return None

    def move_backward(self):
        """Fake Drone moves backward."""
        return None

    def move_up(self):
        """Fake Drone moves up."""
        return None

    def move_down(self):
        """Fake Drone moves down."""
        return None

    def turn_left(self):
        """Fake Drone turns left."""
        return None

    def turn_right(self):
        """Fake Drone turns right."""
        return None

    def hover(self):
        """Fake Drone hover."""
        return None

    def takeoff(self):
        """Fake Drone take the fuck off."""
        return None

    def land(self):
        """Fake Drone lands."""
        return None


class MockResponse(object):
    """Set a header to remove the fake CORS error."""

    headers = {'Access-Control-Allow-Origin': "default_value!"}


class MockHands(object):
    """Mock of Fake Hand method of the Leap controller."""

    class palm_velocity(object):
        """Fake palm velocity of hand to controller."""

        x = 0
        y = 0
        z = 0

    class palm_position(object):
        """Fake palm position of hand to controller."""

        x = 0
        y = 0
        z = 0

    class MockFinger(object):
        """Mock of Fake Finger method of the Leap controller."""

        is_extended = True

    fingers = [MockFinger(),
               MockFinger(),
               MockFinger(),
               MockFinger(),
               MockFinger()]

    grab_strength = 0


class MockFrame(object):
    """Fake on_frame method of the Fake Drone."""

    hands = [MockHands(), MockHands()]


class MockConfig(object):
    """Class to save the config of a fake drone instance."""

    def save(self):
        """Save the created fake drone."""
        return True


class MockFinger(object):
    """Mock of the extension of the fake fingers on the fake drone."""

    def __init__(self, is_extended):
        """Return whether a finger is extended or not."""
        self.is_extended = is_extended


class MockController(object):
    """Fake Controller."""

    _test_only_mock_frame = MockFrame()
    config = MockConfig()
    _test_only_gestures = []

    def enable_gesture(self, gesture):
        """Append the fake guesture that is passed in."""
        self._test_only_gestures.append(gesture)

    def frame(self):
        """Set a fake frame."""
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
def drone(mocker):
    """Return a configured fake drone."""
    mocker.patch('leap_motion.ar_leap.Leap', MockLeap)
    return MockDrone()


@pytest.fixture()
def response(mocker):
    """Return a fake responses for a fake drone."""
    mocker.patch('leap_motion.ar_leap.Leap', MockLeap)
    return MockResponse()


@pytest.fixture()
def controller(mocker):
    """Return a configured fake drone."""
    mocker.patch('leap_motion.ar_leap.Leap', MockLeap)
    return MockController()


@pytest.fixture()
def drone_listener(mocker):
    """"""
    from leap_motion.ar_leap import DroneListener
    mocker.patch('leap_motion.ar_leap.Leap', MockLeap)
    return DroneListener()


@pytest.fixture()
def requests(mocker):
    mocker.patch('leap_motion.ar_leap.requests')
    return Requests
