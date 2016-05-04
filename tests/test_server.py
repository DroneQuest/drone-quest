# -*- coding: utf-8 -*-
"""Test the drone server."""
import pytest
from server.bottle_drone import navdata, do

NET_LOC = "http://127.0.0.1:3000/"

VALID_COMMANDS = (
    "move_left move_right move_forward move_backward move_up move_down "
    "turn_left turn_right hover takeoff land"
).split()

COMMAND_TESTS_PASS = [(message, "Command executed: {}".format(message)) for message in VALID_COMMANDS]


@pytest.mark.parametrize("message,expected_response", COMMAND_TESTS_PASS)
def test_functional_command(drone, message, expected_response):
    response = do(message, drone=drone)
    assert response == expected_response


def test_nav_data(drone):
    response = navdata(drone=drone)
    assert response == drone.navdata
