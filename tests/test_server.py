# -*- coding: utf-8 -*-
import pytest
from tests import client as client_module

@pytest.fixture(scope='module')
def client():
    return client_module.build_client(client_module.setup_socket())


client_module.close(client)
