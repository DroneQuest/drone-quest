# Copyright (c) 2011 Bastian Venthur
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


"""
Python library for the AR.Drone.

This module was tested with Python 2.6.6 and AR.Drone vanilla firmware 1.5.1.
"""

from __future__ import unicode_literals
import socket
import struct
import sys
import threading
import multiprocessing

from venthur_api import arnetwork


__author__ = "Bastian Venthur"

ARDRONE_ADDRESS = arnetwork.ARDRONE_ADDRESS
ARDRONE_NAVDATA_PORT = arnetwork.ARDRONE_NAVDATA_PORT
ARDRONE_VIDEO_PORT = arnetwork.ARDRONE_VIDEO_PORT
ARDRONE_COMMAND_PORT = arnetwork.ARDRONE_COMMAND_PORT


class ARDrone(object):
    """ARDrone Class.

    Instanciate this class to control your drone and receive decoded video and
    navdata.
    """

    def __init__(self):
        """Connect to the drone and initialize the Python representation."""
        self.seq_nr = 1
        self.timer_t = 0.2
        self.com_watchdog_timer = threading.Timer(self.timer_t, self.commwdg)
        self.lock = threading.Lock()
        self.speed = 0.2
        self.at(at_config, "general:navdata_demo", "TRUE")
        self.video_pipe, video_pipe_other = multiprocessing.Pipe()
        self.nav_pipe, nav_pipe_other = multiprocessing.Pipe()
        self.com_pipe, com_pipe_other = multiprocessing.Pipe()
        self.network_process = arnetwork.ARDroneNetworkProcess(
            nav_pipe_other,
            video_pipe_other,
            com_pipe_other
        )
        self.network_process.start()
        self.ipc_thread = arnetwork.IPCThread(self)
        self.ipc_thread.start()
        self.image = b''
        self.navdata = dict()
        self.time = 0

    def takeoff(self):
        """Make the drone takeoff."""
        self.at(at_ftrim)
        self.at(at_config, "control:altitude_max", "20000")
        self.at(at_ref, True)

    def land(self):
        """Make the drone land."""
        self.at(at_ref, False)

    def hover(self):
        """Make the drone hover."""
        self.at(at_pcmd, False, 0, 0, 0, 0)

    def move_left(self):
        """Make the drone move left."""
        self.at(at_pcmd, True, -self.speed, 0, 0, 0)

    def move_right(self):
        """Make the drone move right."""
        self.at(at_pcmd, True, self.speed, 0, 0, 0)

    def move_up(self):
        """Make the drone rise upwards."""
        self.at(at_pcmd, True, 0, 0, self.speed, 0)

    def move_down(self):
        """Make the drone decent downwards."""
        self.at(at_pcmd, True, 0, 0, -self.speed, 0)

    def move_forward(self):
        """Make the drone move forward."""
        self.at(at_pcmd, True, 0, -self.speed, 0, 0)

    def move_backward(self):
        """Make the drone move backwards."""
        self.at(at_pcmd, True, 0, self.speed, 0, 0)

    def turn_left(self):
        """Make the drone rotate left."""
        self.at(at_pcmd, True, 0, 0, 0, -self.speed)

    def turn_right(self):
        """Make the drone rotate right."""
        self.at(at_pcmd, True, 0, 0, 0, self.speed)

    def reset(self):
        """Toggle the drone's emergency state."""
        self.at(at_ref, False, True)
        self.at(at_ref, False, False)

    def trim(self):
        """Flat trim the drone."""
        self.at(at_ftrim)

    def set_speed(self, speed):
        """Set the drone's speed.

        Valid values are floats from [0..1]
        """
        self.speed = speed

    def increase_speed(self):
        """Increase the speed by an increment of 0.1."""
        if (self.speed + 0.1) <= 1:
            self.speed += 0.1

    def decrease_speed(self):
        """Decrease the speed by an increment of 0.1."""
        if (self.speed - 0.1) >= 0:
            self.speed -= 0.1

    def at(self, cmd, *args, **kwargs):
        """Wrapper for the low level at commands.

        This method takes care that the sequence number is increased after each
        at command and the watchdog timer is started to make sure the drone
        receives a command at least every second.
        """
        self.lock.acquire()
        self.com_watchdog_timer.cancel()
        cmd(self.seq_nr, *args, **kwargs)
        self.seq_nr += 1
        self.com_watchdog_timer = threading.Timer(self.timer_t, self.commwdg)
        self.com_watchdog_timer.start()
        self.lock.release()

    def commwdg(self):
        """Communication watchdog signal.

        This needs to be send regulary to keep the communication w/ the drone
        alive.
        """
        self.at(at_comwdg)

    def halt(self):
        """Shutdown the drone.

        This method does not land or halt the actual drone, but the
        communication with the drone. You should call it at the end of your
        application to close all sockets, pipes, processes and threads related
        with this object.
        """
        self.lock.acquire()
        self.com_watchdog_timer.cancel()
        self.com_pipe.send('die!')
        self.network_process.terminate()
        self.network_process.join()
        self.ipc_thread.stop()
        self.ipc_thread.join()
        self.lock.release()

    def move(self, lr, fb, vv, va):
        """Make the drone move: translate/rotate.

        Parameters:
        lr -- left-right tilt: float [-1..1] negative: left, positive: right
        rb -- front-back tilt: float [-1..1] negative: forwards, positive:
            backwards
        vv -- vertical speed: float [-1..1] negative: go down, positive: rise
        va -- angular speed: float [-1..1] negative: spin left, positive: spin
            right
        """
        self.at(at_pcmd, True, lr, fb, vv, va)


###############################################################################
# Low level AT Commands
###############################################################################

def at_ref(seq, takeoff, emergency=False):
    """Basic behaviour of the drone: take-off/landing, emergency stop/reset).

    Parameters:
    seq -- sequence number
    takeoff -- True: Takeoff / False: Land
    emergency -- True: Turn of the engines
    """
    p = 0b10001010101000000000000000000
    if takeoff:
        p += 0b1000000000
    if emergency:
        p += 0b0100000000
    at("REF", seq, [p])


def at_pcmd(seq, progressive, lr, fb, vv, va):
    """Make the drone move (translate/rotate).

    Parameters:
    seq -- sequence number
    progressive -- True: enable progressive commands, False: disable (i.e.
        enable hovering mode)
    lr -- left-right tilt: float [-1..1] negative: left, positive: right
    rb -- front-back tilt: float [-1..1] negative: forwards, positive:
        backwards
    vv -- vertical speed: float [-1..1] negative: go down, positive: rise
    va -- angular speed: float [-1..1] negative: spin left, positive: spin
        right

    The above float values are a percentage of the maximum speed.
    """
    p = 1 if progressive else 0
    at("PCMD", seq, [p, float(lr), float(fb), float(vv), float(va)])


def at_ftrim(seq):
    """Tell the drone it's lying horizontally.

    Parameters:
    seq -- sequence number
    """
    at("FTRIM", seq, [])


def at_zap(seq, stream):
    """Select which video stream to send on the video UDP port.

    Parameters:
    seq -- sequence number
    stream -- Integer: video stream to broadcast
    """
    # FIXME: improve parameters to select the modes directly
    at("ZAP", seq, [stream])


def at_config(seq, option, value):
    """Set configuration parameters of the drone."""
    at("CONFIG", seq, [str(option), str(value)])


def at_comwdg(seq):
    """Reset communication watchdog."""
    # FIXME: no sequence number
    at("COMWDG", seq, [])


def at_aflight(seq, flag):
    """Make the drone fly autonomously.

    Parameters:
    seq -- sequence number
    flag -- Integer: 1: start flight, 0: stop flight
    """
    at("AFLIGHT", seq, [flag])


def at_pwm(seq, m1, m2, m3, m4):
    """Send control values directly to the engines, overriding control loops.

    Parameters:
    seq -- sequence number
    m1 -- front left command
    m2 -- fright right command
    m3 -- back right command
    m4 -- back left command
    """
    # FIXME: what type do mx have?
    pass


def at_led(seq, anim, f, d):
    """Control the drone's LED.

    Parameters:
    seq -- sequence number
    anim -- Integer: animation to play
    f -- ?: frequence in HZ of the animation
    d -- Integer: total duration in seconds of the animation
    """
    pass


def at_anim(seq, anim, d):
    """Make the drone execute a predefined movement (animation).

    Parameters:
    seq -- sequcence number
    anim -- Integer: animation to play
    d -- Integer: total duration in sections of the animation
    """
    at("ANIM", seq, [anim, d])


def at(command, seq, params):
    """Send command directly to the drone.

    Parameters:
    command -- the command
    seq -- the sequence number
    params -- a list of elements which can be either int, float or string
    """
    param_str = ''
    for p in params:
        if isinstance(p, int):
            param_str += ",%d" % p
        elif isinstance(p, float):
            param_str += ",%d" % f2i(p)
        elif isinstance(p, str):
            param_str += ',"' + p + '"'
    msg = "AT*%s=%i%s\r" % (command, seq, param_str)
    # try:
    #     msg.encode('utf-8')
    # except AttributeError:
    #     pass
    msg = bytes(msg, 'utf-8')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg, (ARDRONE_ADDRESS, ARDRONE_COMMAND_PORT))


def f2i(f):
    """Interpret IEEE-754 floating-point value as signed integer.

    Arguments:
    f -- floating point value
    """
    return struct.unpack('i', struct.pack('f', f))[0]


if __name__ == "__main__":

    import termios
    import fcntl
    import os

    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    drone = ARDrone()

    try:
        while 1:
            try:
                c = sys.stdin.read(1)
                c = c.lower()
                print("Got character", c)
                if c == 'a':
                    drone.move_left()
                if c == 'd':
                    drone.move_right()
                if c == 'w':
                    drone.move_forward()
                if c == 's':
                    drone.move_backward()
                if c == ' ':
                    drone.land()
                if c == '\n':
                    drone.takeoff()
                if c == 'q':
                    drone.turn_left()
                if c == 'e':
                    drone.turn_right()
                if c == '1':
                    drone.move_up()
                if c == '2':
                    drone.hover()
                if c == '3':
                    drone.move_down()
                if c == 't':
                    drone.reset()
                if c == 'x':
                    drone.hover()
                if c == 'y':
                    drone.trim()
            except IOError:
                pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
        drone.halt()
