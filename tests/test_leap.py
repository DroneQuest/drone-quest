# -*- coding: utf-8 -*-
"""Test the drone server."""
import pytest
from leap_motion.ar_leap import DroneListener


def test_initialization(controller):
    instance = DroneListener()
    instance.on_init(controller)
    assert instance.start_time
