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
import struct
# import multiprocessing
from . import arvideo

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
CTRL_STATE_DICT = {
    0: 0,  # ####      0: "Not defined"
    131072: 1,  # 131072:  "Landed"
    393216: 2,  # 393216:  "Taking-off-Floor"
    393217: 3,  # 393217:  "Taking-off-Air"
    262144: 4,  # 262144:  "Hovering"
    524288: 5,  # 524288:  "Landing"
    458752: 6,  # 458752:  "Stabilizing"
    196608: 7,  # 196608:  "Moving"
    262153: 8,  # "Undefined"
    196613: 9,  # "Undefined"
    262155: 10,  # "Undefined"
    196614: 11,  # "Undefined"
    458753: 12,  # "Undefined"
}

NAVDATA_KEYS = [
    'ctrl_state',
    'battery',
    'theta',
    'phi',
    'psi',
    'altitude',
    'vx',
    'vy',
    'vz',
    'num_frames',
]


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
        self.use_video = use_video
        self.stopping = False
        if is_ar_drone_2:
            from . import ar2video
            self.ar2video = ar2video.ARVideo2(self._drone, DEBUG)
        else:
            self.ar2video = None

    def run(self):

        def _connect():
            logging.info('Connection to ardrone')
            if self.use_video:
                if self.is_ar_drone_2:
                    video_socket = socket.socket(
                        socket.AF_INET,
                        socket.SOCK_STREAM
                    )
                    video_socket.connect(ARDRONE_VIDEO_ADDR)
                    video_socket.setblocking(0)
                else:
                    video_socket = socket.socket(
                        socket.AF_INET,
                        socket.SOCK_DGRAM
                    )
                    video_socket.setblocking(0)
                    video_socket.bind(('', ARDRONE_VIDEO_PORT))
                    video_socket.sendto(INIT_BYTES, ARDRONE_VIDEO_ADDR)
            else:
                video_socket = socket.socket()
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
            inputready, outputready, exceptready = select.select(
                [nav_socket,
                 video_socket,
                 self.com_pipe,
                 control_socket],
                [],
                [],
                1.
            )
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
                    navdata, has_information = decode_navdata(data)
                    if has_information:
                        self._drone.set_navdata(navdata)
                elif i == self.com_pipe:
                    self.com_pipe.recv()
                    self.stopping = True
                    break
                elif i == control_socket:
                    reconnection_needed = False
                    while not reconnection_needed:
                        try:
                            data = control_socket.recv(65536)
                            if len(data) == 0:
                                logging.warning(
                                    'Received an empty packet on '
                                    'control socket'
                                )
                                reconnection_needed = True
                            else:
                                logging.warning(
                                    "Control Socket says : {}".format(data)
                                )
                        except IOError:
                            break
        _disconnect(video_socket, nav_socket, control_socket)

    def terminate(self):
        """Set the stopping flag to True for use elsewhere."""
        print("Terminate Called")
        self.stopping = True


###############################################################################
# navdata
###############################################################################
def decode_navdata(packet):
    """Decode a navdata packet."""
    offset = 0
    _ = struct.unpack_from("IIII", packet, offset)
    drone_state = dict()
    # FLY MASK : (0) ardrone is landed, (1) ardrone is flying
    drone_state['fly_mask'] = _[1] & 1
    # VIDEO MASK : (0) video disable, (1) video enable
    drone_state['video_mask'] = _[1] >> 1 & 1
    # VISION MASK : (0) vision disable, (1) vision enable */
    drone_state['vision_mask'] = _[1] >> 2 & 1
    # CONTROL ALGO (0) euler angles control, (1) angular speed control */
    drone_state['control_mask'] = _[1] >> 3 & 1
    # ALTITUDE CONTROL ALGO : (0) altitude control inactive (1) altitude control active */
    drone_state['altitude_mask'] = _[1] >> 4 & 1
    # USER feedback : Start button state */
    drone_state['user_feedback_start'] = _[1] >> 5 & 1
    # Control command ACK : (0) None, (1) one received */
    drone_state['command_mask'] = _[1] >> 6 & 1
    # Firmware file is good (1) */
    drone_state['fw_file_mask'] = _[1] >> 7 & 1
    # Firmware update is newer (1) */
    drone_state['fw_ver_mask'] = _[1] >> 8 & 1
    # Firmware update is ongoing (1) */
    drone_state['fw_upd_mask'] = _[1] >> 9 & 1
    drone_state['navdata_demo_mask'] = _[1] >> 10 & 1 # Navdata demo : (0) All navdata, (1) only navdata demo */
    drone_state['navdata_bootstrap'] = _[1] >> 11 & 1 # Navdata bootstrap : (0) options sent in all or demo mode, (1) no navdata options sent */
    drone_state['motors_mask'] = _[1] >> 12 & 1 # Motor status : (0) Ok, (1) Motors problem */
    drone_state['com_lost_mask'] = _[1] >> 13 & 1 # Communication lost : (1) com problem, (0) Com is ok */
    drone_state['vbat_low'] = _[1] >> 15 & 1 # VBat low : (1) too low, (0) Ok */
    drone_state['user_el'] = _[1] >> 16 & 1 # User Emergency Landing : (1) User EL is ON, (0) User EL is OFF*/
    drone_state['timer_elapsed'] = _[1] >> 17 & 1 # Timer elapsed : (1) elapsed, (0) not elapsed */
    drone_state['angles_out_of_range'] = _[1] >> 19 & 1 # Angles : (0) Ok, (1) out of range */
    drone_state['ultrasound_mask'] = _[1] >> 21 & 1 # Ultrasonic sensor : (0) Ok, (1) deaf */
    drone_state['cutout_mask'] = _[1] >> 22 & 1 # Cutout system detection : (0) Not detected, (1) detected */
    drone_state['pic_version_mask'] = _[1] >> 23 & 1 # PIC Version number OK : (0) a bad version number, (1) version number is OK */
    drone_state['atcodec_thread_on'] = _[1] >> 24 & 1 # ATCodec thread ON : (0) thread OFF (1) thread ON */
    drone_state['navdata_thread_on'] = _[1] >> 25 & 1 # Navdata thread ON : (0) thread OFF (1) thread ON */
    drone_state['video_thread_on'] = _[1] >> 26 & 1 # Video thread ON : (0) thread OFF (1) thread ON */
    drone_state['acq_thread_on'] = _[1] >> 27 & 1 # Acquisition thread ON : (0) thread OFF (1) thread ON */
    drone_state['ctrl_watchdog_mask'] = _[1] >> 28 & 1 # CTRL watchdog : (1) delay in control execution (> 5ms), (0) control is well scheduled */
    drone_state['adc_watchdog_mask'] = _[1] >> 29 & 1 # ADC Watchdog : (1) delay in uart2 dsr (> 5ms), (0) uart2 is good */
    drone_state['com_watchdog_mask'] = _[1] >> 30 & 1 # Communication Watchdog : (1) com problem, (0) Com is ok */
    drone_state['emergency_mask'] = _[1] >> 31 & 1 # Emergency landing : (0) no emergency, (1) emergency */
    data = dict()
    data['drone_state'] = drone_state
    data['header'] = _[0]
    data['seq_nr'] = _[2]
    data['vision_flag'] = _[3]
    offset += struct.calcsize("IIII")
    has_flying_information = False
    while 1:
        try:
            id_nr, size = struct.unpack_from("HH", packet, offset)
            offset += struct.calcsize("HH")
        except struct.error:
            break
        values = []
        for i in range(size - struct.calcsize("HH")):
            values.append(struct.unpack_from("c", packet, offset)[0])
            offset += struct.calcsize("c")
        # navdata_tag_t in navdata-common.h
        if id_nr == 0:
            has_flying_information = True
            values = struct.unpack_from("IIfffifffI", "".join(values))
            values = dict(zip(NAVDATA_KEYS, values))
            # convert the millidegrees into degrees and round to int, as they
            values['ctrl_state'] = CTRL_STATE_DICT[values['ctrl_state']]
            # are not so precise anyways
            for i in 'theta', 'phi', 'psi':
                values[i] = int(values[i] / 1000)
        data[id_nr] = values
    return data, has_flying_information
