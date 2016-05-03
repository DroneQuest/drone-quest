
try:
    from venthur_api import libardrone
except ImportError:
    import libardrone
import time
import Leap
import sys
import requests
# from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

NET_LOC = "http://127.0.0.1:8083"
# drone = libardrone.ARDrone()


class DroneListener(Leap.Listener):
    flying = False

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
        # controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)

        # controller.config.set("Gesture.Circle.MinRadius", 100.0)

        controller.config.save()

    def on_disconnect(self, controller):
        """Disconnect from drone."""
        pass

    def on_exit(self, controller):
        """Exit."""
        pass

    def on_frame(self, controller):
        """Read frames from the drone."""
        # Preven leap from reading GARBAGE BITCHES
        if (time.time() - self.start_time) < 1.5:
            return

        frame = controller.frame()

        # for gesture in frame.gestures():
        #     pass
        #     # don't have circle yet...BICTCHES

        hand = frame.hands[0]

        # if len(hand.fingers) <= 1:
        #     self.hand_closed(hand)
        # else:
        #     self.hand_opened(hand)

        #     if len(hands.fingers) <= 1:
        # if hand.palm_velocity.y > 100:
        if self.flying is False:
            if hand.grab_strength == 0:
                requests.get(NET_LOC + "/do/takeoff")
                requests.get(NET_LOC + "/do/hover")
                self.flying = True

        if hand.palm_velocity.y <= -100:
            requests.get(NET_LOC + "/do/land")
            self.flying = False


if __name__ == '__main__':
    listener = DroneListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    sys.stdin.readline()

    controller.remove_listener(listener)
