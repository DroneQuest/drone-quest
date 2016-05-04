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


@pytest.fixture()
def drone():
    return MockDrone()


@pytest.fixture()
def response():
    return MockResponse()
