# -*- coding: utf-8 -*-
"""Test the leap translation code."""
import pytest
import random

INCREMENTS = list(range(-100, 100, 25)) + [1000, -1000, 1500, -1500]
HAND_POSITIONS = []

for strength in [0, 0.25, 0.5, 0.75, 1]:
    px = py = pz = 0
    for vx in INCREMENTS:
        for vy in INCREMENTS:
            for vz in INCREMENTS:
                HAND_POSITIONS.append((strength, vx, vy, vz, px, py, pz))
    vx = vy = vz = 0
    for px in INCREMENTS:
        for py in INCREMENTS:
            for pz in INCREMENTS:
                HAND_POSITIONS.append((strength, vx, vy, vz, px, py, pz))

random.shuffle(HAND_POSITIONS)
HAND_POSITIONS = HAND_POSITIONS[:300]


def test_initialization(controller, drone_listener):
    drone_listener.on_init(controller)
    assert drone_listener.start_time


def test_connect(controller, drone_listener):
    drone_listener.on_init(controller)
    assert drone_listener.start_time


def test_disconnect(controller, drone_listener):
    assert drone_listener.on_disconnect(controller) is None


def test_exit(controller, drone_listener):
    assert drone_listener.on_exit(controller) is None


def test_no_hands(controller, drone_listener, requests):
    history = []
    drone_listener._talk_to_drone = lambda self, route: history.append(route)
    drone_listener.on_frame(controller)
    assert len(history) == 0


@pytest.mark.parametrize("s, vx, vy, vz, px, py, pz", HAND_POSITIONS)
def test_hand_position(controller, drone_listener, requests, s, vx, vy, vz, px, py, pz):
# def test_hand_position(controller, drone_listener, requests):
    """
    s = grab_strength
    v(x,y,z) = velocity of palm along (x,y,z) axis
    p(x,y,z) = position of palm along (x,y,z) axis
    """
    # print(s, vx, vy, vz, px, py, pz)
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[3:])
    drone_listener.flying = False
    controller._test_only_set_grab_strength(1)
    controller._test_only_set_palm_velocity(0, 2000, 0)
    controller._test_only_set_palm_position(0, 150, 0)
    drone_listener.on_frame(controller)
    if s == 1 and vy > 1000:
        assert history == [['do', 'takeoff'], ['do', 'hover']]
