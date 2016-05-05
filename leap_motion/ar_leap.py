import time
# try:
# import Leap
# except ImportError:
from tests.conftest import MockLeap as Leap
import sys
import requests
# from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

from server.bottle_drone import DRONE_SERVER_ADDRESS

NET_LOC = DRONE_SERVER_ADDRESS


class DroneListener(Leap.Listener):
    flying = False
    last = None

    def on_init(self, controller):
        """Initialize the leap motion."""
        print("LEAP IS ON")
        self.start_time = time.time()
        # self.last_flip_time = time.time() - 10

    def on_connect(self, controller):
        """Make a connection with the leap."""
        print("LEAP IS CONNECTED")

        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        # controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        assert type(Leap.Gesture.TYPE_KEY_TAP) == str
        # controller.config.set("Gesture.Circle.MinRadius", 100.0)

        controller.config.save()

    def on_disconnect(self, controller):
        """Disconnect from drone."""
        pass

    def on_exit(self, controller):
        """Exit."""
        pass

    def _talk_to_drone(self, route):
        if route != self.last:
            self.last = route
            print(route)
            # return requests.post(route)

    def _turning_direction(self, hand):
        var = True
        for i in range(1, 4):
            var = var and hand.fingers[i].is_extended
        if var and not hand.fingers[0].is_extended:
            return 'left'
        var = True
        for i in range(0, 2):
            var = var and hand.fingers[i].is_extended
        if var and not hand.fingers[4].is_extended:
            return 'right'
        return 'center'

        # if hand.fingers[0].is_extended is False and all(hand.fingers[0].is_extended is False):

    def on_frame(self, controller):
        """Read frames from the drone."""
        # if (time.time() - self.start_time) < 1.5:
        # return

        frame = controller.frame()

        # for gesture in frame.gestures():
        #     pass
        #     # don't have circle yet...

        hand = frame.hands[0]

        # if len(hand.fingers) <= 1:
        #     self.hand_closed(hand)
        # else:
        #     self.hand_opened(hand)

        #     if len(hands.fingers) <= 1:
        # if hand.palm_velocity.y > 100:
        if self.flying is False:
            if hand.grab_strength == 1:
                if hand.palm_velocity.y >= 1000:
                    # print("TAKEOFF AND HOVER")
                    self._talk_to_drone(NET_LOC + "/do/takeoff")
                    self._talk_to_drone(NET_LOC + "/do/hover")
                    self.flying = True

        elif self.flying is True:
            if hand.grab_strength == 1:
                if hand.palm_velocity.y <= -1000:
                    # print("LAND N STUFF")
                    self._talk_to_drone(NET_LOC + '/do/land')
                    self.flying = False
            elif hand.grab_strength < 0.2:
                if hand.palm_position.z <= -50:
                    # print("MOVE FORWARD")
                    self._talk_to_drone(NET_LOC + '/do/move_forward')
                elif hand.palm_position.z >= 50:
                    # print("MOVE BACKWARD")
                    self._talk_to_drone(NET_LOC + '/do/move_backward')
                elif hand.palm_position.x >= 50:
                    # print("MOVE RIGHT")
                    self._talk_to_drone(NET_LOC + '/do/move_right')
                elif hand.palm_position.x <= -50:
                    # print("MOVE LEFT")
                    self._talk_to_drone(NET_LOC + '/do/move_left')
                elif hand.palm_velocity.y <= 10 and hand.palm_velocity.y >= -10:
                    if self._turning_direction(hand) == 'left':
                        self._talk_to_drone(NET_LOC + '/do/turn_left')
                    elif self._turning_direction(hand) == 'right':
                        self._talk_to_drone(NET_LOC + '/do/turn_right')
                    else:
                        self._talk_to_drone(NET_LOC + '/do/hover')


if __name__ == '__main__':
    listener = DroneListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    sys.stdin.readline()

    controller.remove_listener(listener)
