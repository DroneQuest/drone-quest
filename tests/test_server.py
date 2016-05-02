# -*- coding: utf-8 -*-
"""Test the drone server."""
import pytest
from tests import client as client_module
from server.main import (
    PING,
    TAKE_OFF,
    LAND,
    HOVER,
    MOVE_LEFT,
    MOVE_RIGHT,
    MOVE_UP,
    MOVE_DOWN,
    MOVE_FORWARD,
    MOVE_BACKWARD,
    TURN_LEFT,
    TURN_RIGHT,
    RESET,
    CALIBRATE,
    SPEED,
    TERMINATE
)


@pytest.fixture(scope='function')
def client():
    """Client fixture."""
    return client_module.build_client(client_module.setup_socket())


def test_ping(client):
    """Test that the client can send a message that we interpet as a ping."""
    client_module.send_message(client, b'0x00')
    resp = client_module.get_reply(client)
    assert resp == 'OK'
    client_module.close(client)


def test_take_off(client):
    """Test that the client can send a message that we interpet as a ping."""
    client_module.send_message(client, b'0x00')
    resp = client_module.get_reply(client)
    assert resp == 'OK'
    client_module.close(client)
