# -*- coding: utf-8 -*-
"""Test the drone server."""
import pytest
from server.bottle_drone import navdata, do, enable_cors
from bottle import HTTPError

NET_LOC = "http://127.0.0.1:3000/"

VALID_COMMANDS = (
    "move_left move_right move_forward move_backward move_up move_down "
    "turn_left turn_right hover takeoff land"
).split()

COMMAND_TESTS_PASS = [(message, "Command executed: {}".format(message)) for message in VALID_COMMANDS]
COMMAND_TESTS_FAIL = [("invalid_method", "Bad Command: invalid_method")]


@pytest.mark.parametrize("message,expected_response", COMMAND_TESTS_PASS)
def test_functional_command(drone, message, expected_response):
    response = do(message, drone=drone)
    assert response == expected_response


@pytest.mark.parametrize("message, expected_response", COMMAND_TESTS_FAIL)
def test_dysfunctional_command(drone, message, expected_response):
    with pytest.raises(HTTPError):
        response = do(message, drone=drone)


def test_nav_data(drone):
    response = navdata(drone=drone)
    assert response == drone.navdata


def test_enable_cors(response):
    enable_cors(response)
    assert response.headers['Access-Control-Allow-Origin'] == '*'
