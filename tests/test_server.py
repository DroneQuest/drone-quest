# -*- coding: utf-8 -*-
"""Test the drone server."""
import pytest
from tests import client as client_module


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
    """Test that the client can send a message that we interpet as a take off."""
    client_module.send_message(client, b'0x00')
    resp = client_module.get_reply(client)
    assert resp == 'OK'
    client_module.close(client)


def test_land(client):
    """Test that the client can send a message that we interpet as a land command."""
    client_module.send_message(client, b'0x02')
    resp = client_module.get_reply(client)
    assert resp == 'OK'
    client_module.close(client)


"""
    LAND = 0x02
    HOVER = 0x03
    MOVE_LEFT = 0x04
    MOVE_RIGHT = 0x05
    MOVE_UP = 0x06
    MOVE_DOWN = 0x07
    MOVE_FORWARD = 0x08
    MOVE_BACKWARD = 0x09
    TURN_LEFT = 0x0A
    TURN_RIGHT = 0x0B
    RESET = 0x0C
    CALIBRATE = 0x0D
    SPEED = 0x0E
    TERMINATE = 0x10
"""
