# -*- coding: utf-8 -*-
"""Test the leap translation code."""
import pytest


def test_initialization(controller, drone_listener):
    """Test if the drone starts up correctly."""
    drone_listener.on_init(controller)
    assert drone_listener.start_time


def test_connect(controller, drone_listener):
    """Test if the drone connects properly."""
    drone_listener.on_init(controller)
    assert drone_listener.start_time


def test_disconnect(controller, drone_listener):
    """Test if the drone disconnects correctly."""
    assert drone_listener.on_disconnect(controller) is None


def test_exit(controller, drone_listener):
    """Test if the drone exits correctly."""
    assert drone_listener.on_exit(controller) is None


def test_no_hands(controller, drone_listener, requests):
    """Test if the leap motion does not send commands if no hands found."""
    history = []
    drone_listener._talk_to_drone = lambda self, route: history.append(route)
    drone_listener.on_frame(controller)
    assert len(history) == 0


@pytest.mark.parametrize("velocity_y", [vy for vy in range(1000, 5000, 1000)])
def test_try_to_take_off(controller, drone_listener, velocity_y):
    """Test if the drone takes off if hands jerk up in a fist."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = False
    controller._test_only_set_palm_velocity(0, velocity_y, 0)
    controller._test_only_set_grab_strength(1)
    drone_listener.on_frame(controller)
    assert history == ['takeoff', 'hover']


@pytest.mark.parametrize("velocity_y", [vy for vy in range(1000, 5000, 1000)])
def test_do_not_to_take_off_hand_open(controller, drone_listener, velocity_y):
    """Test if the drone does not takes off if hands jerk up while open."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = False
    controller._test_only_set_palm_velocity(0, velocity_y, 0)
    controller._test_only_set_grab_strength(0)
    drone_listener.on_frame(controller)
    assert history == []


@pytest.mark.parametrize("velocity_y", [vy for vy in range(1000, 5000, 1000)])
def test_do_not_to_take_off_is_flying(controller, drone_listener, velocity_y):
    """Test if the api does not send take off commands if the drone is already flying."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_velocity(0, velocity_y, 0)
    controller._test_only_set_grab_strength(1)
    drone_listener.on_frame(controller)
    assert history == []


@pytest.mark.parametrize("velocity_y", [vy for vy in range(0, 1000, 100)])
def test_do_not_to_take_off_is_too_slow(controller, drone_listener, velocity_y):
    """Test if the drone does not take off if the hand just moves up."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = False
    controller._test_only_set_palm_velocity(0, velocity_y, 0)
    controller._test_only_set_grab_strength(1)
    drone_listener.on_frame(controller)
    assert history == []


@pytest.mark.parametrize("velocity_y", [vy for vy in range(-5000, -1000, 1000)])
def test_try_to_land(controller, drone_listener, velocity_y):
    """Test if the drone lands if the user jerks hand down in a fist."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_velocity(0, velocity_y, 0)
    controller._test_only_set_grab_strength(1)
    drone_listener.on_frame(controller)
    assert history == ['land']


@pytest.mark.parametrize("velocity_y", [vy for vy in range(-5000, -1000, 1000)])
def test_do_not_land_hand_open(controller, drone_listener, velocity_y):
    """Test if the drone does not land if the user jerks open hand down."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_velocity(0, velocity_y, 0)
    controller._test_only_set_grab_strength(0)
    drone_listener.on_frame(controller)
    assert history == []


@pytest.mark.parametrize("velocity_y", [vy for vy in range(-5000, -1000, 1000)])
def test_do_not_land_is_on_ground(controller, drone_listener, velocity_y):
    """Test if the drone does not land if already grounded."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = False
    controller._test_only_set_palm_velocity(0, velocity_y, 0)
    controller._test_only_set_grab_strength(1)
    drone_listener.on_frame(controller)
    assert history == []


@pytest.mark.parametrize("velocity_y", [vy for vy in range(1000, 0, -100)])
def test_do_not_land_is_too_slow(controller, drone_listener, velocity_y):
    """Test if the drone does not land if the user moves hand down slowly."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_velocity(0, velocity_y, 0)
    controller._test_only_set_grab_strength(1)
    drone_listener.on_frame(controller)
    assert history == []


@pytest.mark.parametrize("velocity_y", [vy for vy in range(-10, 10)])
def test_hover(controller, drone_listener, velocity_y):
    """Test if the drone hovers if the hand is still."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_velocity(0, velocity_y, 0)
    controller._test_only_set_grab_strength(0)
    drone_listener.on_frame(controller)
    assert history == ['hover']


@pytest.mark.parametrize("velocity_y", [-20, -15, 15, 20])
def test_does_not_hover(controller, drone_listener, velocity_y):
    """Test if the drone does not hover if the user isn't staying still."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_velocity(0, velocity_y, 0)
    controller._test_only_set_grab_strength(0)
    drone_listener.on_frame(controller)
    assert history == []


@pytest.mark.parametrize("position_z", [px for px in range(-100, -50, 10)])
def test_move_forward(controller, drone_listener, position_z):
    """Test if the drone moves forward when hand is in correct position."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_position(0, 0, position_z)
    controller._test_only_set_grab_strength(0)
    drone_listener.on_frame(controller)
    assert history == ['move_forward']


@pytest.mark.parametrize("position_z", [px for px in range(-45, -10, 15)])
def test_do_not_move_forward(controller, drone_listener, position_z):
    """Test if the drone does not move forward when hand is close to correct position."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_position(0, 0, position_z)
    controller._test_only_set_grab_strength(0)
    drone_listener.on_frame(controller)
    assert history == []


@pytest.mark.parametrize("position_z", [px for px in range(-100, -50, 10)])
def test_move_forward_hand_closed(controller, drone_listener, position_z):
    """Test if the drone does not move forward when hand is closed."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_position(0, 0, position_z)
    controller._test_only_set_grab_strength(1)
    drone_listener.on_frame(controller)
    assert history == []


@pytest.mark.parametrize("position_z", [px for px in range(50, 100, 10)])
def test_move_backward(controller, drone_listener, position_z):
    """Test if the drone moves backward when hand is in correct position."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_position(0, 0, position_z)
    controller._test_only_set_grab_strength(0)
    drone_listener.on_frame(controller)
    assert history == ['move_backward']


@pytest.mark.parametrize("position_z", [px for px in range(10, 45, 15)])
def test_do_not_move_backward(controller, drone_listener, position_z):
    """Test if the drone does not move backward when hand is close to correct position."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_position(0, 0, position_z)
    controller._test_only_set_grab_strength(0)
    drone_listener.on_frame(controller)
    assert history == []


@pytest.mark.parametrize("position_z", [px for px in range(50, 100, 10)])
def test_move_backward_hand_closed(controller, drone_listener, position_z):
    """Test if the drone does not move backward when hand is closed."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_position(0, 0, position_z)
    controller._test_only_set_grab_strength(1)
    drone_listener.on_frame(controller)
    assert history == []



@pytest.mark.parametrize("position_x", [px for px in range(50, 100, 10)])
def test_move_right(controller, drone_listener, position_x):
    """Test if the drone moves right when hand is in correct position."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_position(position_x, 0, 0)
    controller._test_only_set_grab_strength(0)
    drone_listener.on_frame(controller)
    assert history == ['move_right']


@pytest.mark.parametrize("position_x", [px for px in range(10, 45, 15)])
def test_do_not_move_right(controller, drone_listener, position_x):
    """Test if the drone does not move right when hand is close to correct position."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_position(position_x, 0, 0)
    controller._test_only_set_grab_strength(0)
    drone_listener.on_frame(controller)
    assert history == []


@pytest.mark.parametrize("position_x", [px for px in range(50, 100, 10)])
def test_move_right_hand_closed(controller, drone_listener, position_x):
    """Test if the drone does not move right when hand is closed."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_position(position_x, 0, 0)
    controller._test_only_set_grab_strength(1)
    drone_listener.on_frame(controller)
    assert history == []



@pytest.mark.parametrize("position_x", [px for px in range(-100, -50, 10)])
def test_move_left(controller, drone_listener, position_x):
    """Test if the drone moves left when hand is in correct position."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_position(position_x, 0, 0)
    controller._test_only_set_grab_strength(0)
    drone_listener.on_frame(controller)
    assert history == ['move_left']


@pytest.mark.parametrize("position_x", [px for px in range(-45, -10, 15)])
def test_do_not_move_left(controller, drone_listener, position_x):
    """Test if the drone does not move left when hand is close to correct position."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_position(position_x, 0, 0)
    controller._test_only_set_grab_strength(0)
    drone_listener.on_frame(controller)
    assert history == []


@pytest.mark.parametrize("position_x", [px for px in range(-100, -50, 10)])
"""Test if the drone does not move left when hand is closed."""
def test_move_left_hand_closed(controller, drone_listener, position_x):
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = True
    controller._test_only_set_palm_position(position_x, 0, 0)
    controller._test_only_set_grab_strength(1)
    drone_listener.on_frame(controller)
    assert history == []


@pytest.mark.parametrize("positions", [position for position in [(50, 0, 0), (0, 50, 0), (0, 0, 50)]])
def test_do_not_move_is_grounded(controller, drone_listener, positions):
    """Test if the leap motion does not send any commands when drone is grounded."""
    history = []
    drone_listener._talk_to_drone = lambda route: history.append(route.split('/')[-1])
    drone_listener.flying = False
    controller._test_only_set_palm_position(positions[0], positions[1], positions[2])
    controller._test_only_set_grab_strength(0)
    drone_listener.on_frame(controller)
    assert history == []
