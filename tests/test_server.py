# -*- coding: utf-8 -*-
"""Test the drone server."""
import pytest
from requests import post, get

NET_LOC = "http://127.0.0.1:3000/"

VALID_COMMANDS = (
    "move_left move_right move_forward move_backward move_up move_down "
    "turn_left turn_right hover takeoff land"
).split()

COMMAND_TESTS_PASS = [(message, "Command executed: {}".format(message)) for message in VALID_COMMANDS]


@pytest.mark.parametrize("message,expected_response", COMMAND_TESTS_PASS)
def test_command(message, expected_response):
    """Test the server responds to all commands correctly."""
    location = NET_LOC + "do/" + message
    # import pdb; pdb.set_trace()

    assert post(location).text == expected_response


def test_navdata():
    location = NET_LOC + 'navdata'
    assert get(location).ok
