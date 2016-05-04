# -*- coding: utf-8 -*-
"""Test the leap translation code."""
import pytest
import random

INCREMENTS = list(range(-100, 100, 25)) + [1000, -1000, 1500, -1500]
HAND_POSITIONS = []

for flying in [True, False]:
    for strength in [0, 0.25, 0.5, 0.75, 1]:
        px = py = pz = 0
        for vy in INCREMENTS:
            HAND_POSITIONS.append((strength, 0, 0, 0, px, py, pz, flying))
        for px in INCREMENTS:
            for py in INCREMENTS:
                for pz in INCREMENTS:
                    HAND_POSITIONS.append((strength, 0, vy, 0, 0, 0, 0, flying))

# random.shuffle(HAND_POSITIONS)
# HAND_POSITIONS = HAND_POSITIONS[:1000]


LANDING_TESTS = []
for flying in [True, False]:
    for strength in [0, 1]:
        for vy in range(-2000, 2000, 100):
            LANDING_TESTS.append((strength, vy, flying))


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


@pytest.mark.parametrize("velocity_y", [vy for vy in range(1000, 5000, 1000)])
def test_try_to_take_off(controller, drone_listener, velocity_y):
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = False
    controller._test_only_set_palm_velocity(0, velocity_y, 0)
    controller._test_only_set_grab_strength(1)
    drone_listener.on_frame(controller)
    assert history == ['takeoff', 'hover']


@pytest.mark.parametrize("velocity_y", [vy for vy in range(1000, 5000, 1000)])
def test_do_not_to_take_off_hand_open(controller, drone_listener, velocity_y):
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = False
    controller._test_only_set_palm_velocity(0, velocity_y, 0)
    controller._test_only_set_grab_strength(0)
    drone_listener.on_frame(controller)
    assert history == []


@pytest.mark.parametrize("velocity_y", [vy for vy in range(1000, 5000, 1000)])
def test_do_not_to_take_off_is_flying(controller, drone_listener, velocity_y):
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_velocity(0, velocity_y, 0)
    controller._test_only_set_grab_strength(1)
    drone_listener.on_frame(controller)
    assert history == []


@pytest.mark.parametrize("velocity_y", [vy for vy in range(0, 1000, 100)])
def test_do_not_to_take_off_is_too_slow(controller, drone_listener, velocity_y):
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = False
    controller._test_only_set_palm_velocity(0, velocity_y, 0)
    controller._test_only_set_grab_strength(1)
    drone_listener.on_frame(controller)
    assert history == []


@pytest.mark.parametrize("velocity_y", [vy for vy in range(-5000, -1000, 1000)])
def test_try_to_land(controller, drone_listener, velocity_y):
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_velocity(0, velocity_y, 0)
    controller._test_only_set_grab_strength(1)
    drone_listener.on_frame(controller)
    assert history == ['land']


@pytest.mark.parametrize("velocity_y", [vy for vy in range(-5000, -1000, 1000)])
def test_do_not_land_hand_open(controller, drone_listener, velocity_y):
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_velocity(0, velocity_y, 0)
    controller._test_only_set_grab_strength(0)
    drone_listener.on_frame(controller)
    assert history == []


@pytest.mark.parametrize("velocity_y", [vy for vy in range(-5000, -1000, 1000)])
def test_do_not_land_is_on_ground(controller, drone_listener, velocity_y):
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = False
    controller._test_only_set_palm_velocity(0, velocity_y, 0)
    controller._test_only_set_grab_strength(1)
    drone_listener.on_frame(controller)
    assert history == []


@pytest.mark.parametrize("velocity_y", [vy for vy in range(1000, 0, -100)])
def test_do_not_land_is_too_slow(controller, drone_listener, velocity_y):
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_velocity(0, velocity_y, 0)
    controller._test_only_set_grab_strength(1)
    drone_listener.on_frame(controller)
    assert history == []


@pytest.mark.parametrize("velocity_y", [vy for vy in range(-10, 10)])
def test_hover(controller, drone_listener, velocity_y):
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_velocity(0, velocity_y, 0)
    controller._test_only_set_grab_strength(0)
    drone_listener.on_frame(controller)
    assert history == ['hover']


@pytest.mark.parametrize("velocity_y", [-20, -15, 15, 20])
def test_hover(controller, drone_listener, velocity_y):
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_velocity(0, velocity_y, 0)
    controller._test_only_set_grab_strength(0)
    drone_listener.on_frame(controller)
    assert history == []


# @pytest.mark.parametrize("position_x", [px for px in range(50, 100, 10)])
# def test_move_forward(controller, drone_listener, position_x):
#     history = []
#     drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
#     drone_listener.flying = True
#     controller._test_only_set_palm_velocity(0, velocity_y, 0)
#     controller._test_only_set_grab_strength(1)
#     drone_listener.on_frame(controller)
#     assert history == []

# @pytest.mark.parametrize("s, vx, vy, vz, px, py, pz, f", LANDING_TESTS)
# def test_hand_position_for_landing(controller, drone_listener, s, vx, vy, vz, px, py, pz, f):
# # def test_hand_position(controller, drone_listener, requests):
#     """
#     s = grab_strength
#     f = flying boolean
#     v(x,y,z) = velocity of palm along (x,y,z) axis
#     p(x,y,z) = position of palm along (x,y,z) axis
#     """
#     # print(s, vx, vy, vz, px, py, pz)
#     history = []
#     drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[3:])
#
#     drone_listener.flying = f
#     assert drone_listener.flying is f, drone_listener.flying
#     controller._test_only_set_grab_strength(s)
#     controller._test_only_set_palm_velocity(vx, vy, vz)
#     controller._test_only_set_palm_position(px, py, pz)
#     drone_listener.on_frame(controller)
#     if s == 0:
#         if f is False:
#             assert history == []
#         else:
#             if vy <= 10 and vy >= -10:
#                 assert history == [['do', 'hover']]
#             else:
#                 assert history == []
#     elif s == 1:
#         if vy >= 1000:  # if hand is closed and moving up
#             if f is False:  # if it's not flying
#                 assert history == [['do', 'takeoff'], ['do', 'hover']]
#             else:  # if it's flying
#                 assert history == []
#         elif vy <= -1000:  # if hand is closed and moving down
#             if f is False:  # if it's not flying:
#                 assert history == []
#             else:  # if it's flying
#                 assert history == [['do', 'land']]
#         else:
#             assert history == []
#
#     else:
#         assert False, "Should never get here"
