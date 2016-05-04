"""
This module provides access to the data provided by the AR.Drone.
"""
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
import logging

import threading
import select
import socket
# import multiprocessing
from . import libardrone, arvideo

INIT_BYTES = b'\x01\x00\x00\x00'
ARDRONE_IP = '192.168.1.1'
ARDRONE_NAVDATA_PORT = 5554
ARDRONE_VIDEO_PORT = 5555
ARDRONE_COMMAND_PORT = 5556
ARDRONE_CONTROL_PORT = 5559

ARDRONE_NAVDATA_ADDR = (ARDRONE_IP, ARDRONE_NAVDATA_PORT)
ARDRONE_VIDEO_ADDR = (ARDRONE_IP, ARDRONE_VIDEO_PORT)
ARDRONE_COMMAND_ADDR = (ARDRONE_IP, ARDRONE_COMMAND_PORT)
ARDRONE_CONTROL_ADDR = (ARDRONE_IP, ARDRONE_CONTROL_PORT)
DEBUG = False


class ARDroneNetworkProcess(threading.Thread):
    """ARDrone Network Process.

    This process collects data from the video and navdata port, converts the
    data and sends it to the IPCThread.
    """

    def __init__(self, com_pipe, is_ar_drone_2, drone, use_video=True):
        threading.Thread.__init__(self)
        self._drone = drone
        self.com_pipe = com_pipe
        self.is_ar_drone_2 = is_ar_drone_2
        self.stopping = False
        if is_ar_drone_2:
            from . import ar2video
            self.ar2video = ar2video.ARVideo2(self._drone, DEBUG)
        else:
            self.ar2video = None

    def run(self):

        def _connect():
            logging.warn('Connection to ardrone')
            if self.is_ar_drone_2:
                video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                video_socket.connect(ARDRONE_VIDEO_ADDR)
                video_socket.setblocking(0)
            else:
                video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                video_socket.setblocking(0)
                video_socket.bind(('', ARDRONE_VIDEO_PORT))
                video_socket.sendto(INIT_BYTES, ARDRONE_VIDEO_ADDR)

            nav_socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_DGRAM,
                socket.IPPROTO_UDP,
            )
            nav_socket.setblocking(0)
            nav_socket.bind(('', ARDRONE_NAVDATA_PORT))
            nav_socket.sendto(INIT_BYTES, ARDRONE_NAVDATA_ADDR)

            control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            control_socket.connect(ARDRONE_CONTROL_ADDR)
            control_socket.setblocking(0)
            logging.warn('Connection established')
            return video_socket, nav_socket, control_socket

        def _disconnect(video_socket, nav_socket, control_socket):
            logging.warn('Disconnection to ardrone streams')
            video_socket.close()
            nav_socket.close()
            control_socket.close()

        video_socket, nav_socket, control_socket = _connect()

        self.stopping = False
        connection_lost = 1
        reconnection_needed = False
        while not self.stopping:
            if reconnection_needed:
                _disconnect(video_socket, nav_socket, control_socket)
                video_socket, nav_socket, control_socket = _connect()
                reconnection_needed = False
            inputready, outputready, exceptready = select.select([nav_socket, video_socket, self.com_pipe, control_socket], [], [], 1.)
            if len(inputready) == 0:
                connection_lost += 1
                reconnection_needed = True
            for i in inputready:
                if i == video_socket:
                    while 1:
                        try:
                            data = video_socket.recv(65536)
                            if self.is_ar_drone_2:
                                self.ar2video.write(data)
                        except IOError:
                            # we consumed every packet from the socket and
                            # continue with the last one
                            break
                        # Sending is taken care of by the decoder
                    if not self.is_ar_drone_2:
                        w, h, image, t = arvideo.read_picture(data)
                        self._drone.set_image(image)
                elif i == nav_socket:
                    while 1:
                        try:
                            data = nav_socket.recv(500)
                        except IOError:
                            # we consumed every packet from the socket and
                            # continue with the last one
                            break
                    navdata, has_information = libardrone.decode_navdata(data)
                    if (has_information):
                        self._drone.set_navdata(navdata)
                elif i == self.com_pipe:
                    _ = self.com_pipe.recv()
                    self.stopping = True
                    break
                elif i == control_socket:
                    reconnection_needed = False
                    while not reconnection_needed:
                        try:
                            data = control_socket.recv(65536)
                            if len(data) == 0:
                                logging.warning('Received an empty packet on control socket')
                                reconnection_needed = True
                            else:
                                logging.warning("Control Socket says : %s", data)
                        except IOError:
                            break
        _disconnect(video_socket, nav_socket, control_socket)

    def terminate(self):
        self.stopping = True
