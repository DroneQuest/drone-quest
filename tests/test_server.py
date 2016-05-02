# -*- coding: utf-8 -*-
"""Test the drone server."""
import pytest
from tests import client as client_module


COMMAND_TESTS_PASS = [(hex(message), "OK") for message in range(16)]


@pytest.fixture(scope='function')
def client():
    """Client fixture."""
    return client_module.build_client(client_module.setup_socket())


@pytest.mark.parametrize("message,expected_response", COMMAND_TESTS_PASS)
def test_command(client, message, expected_response):
    """Test the server responds to all commands correctly."""
    client_module.send_message(client, message)
    resp = client_module.get_reply(client)
    assert resp == expected_response
    client_module.close(client)
