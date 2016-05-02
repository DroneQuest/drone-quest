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
    client_module.send_message(client, '0x00')
    resp = client_module.get_reply(client)
    assert resp == 'OK'
    client_module.close(client)
