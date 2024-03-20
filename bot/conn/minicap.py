import socket
import sys
import struct

import cv2
from collections import OrderedDict

import numpy

# Banner类用于存储minicap的banner信息。banner信息是在与minicap建立连接时发送的一些关于设备屏幕的信息。
# 例如，它包括设备屏幕的宽度和高度，以及设备屏幕的方向。
class Banner:
    def __init__(self):
        self.__banner = OrderedDict(
            [('version', 0),
             ('length', 0),
             ('pid', 0),
             ('realWidth', 0),
             ('realHeight', 0),
             ('virtualWidth', 0),
             ('virtualHeight', 0),
             ('orientation', 0),
             ('quirks', 0)
             ])

    def __setitem__(self, key, value):
        self.__banner[key] = value

    def __getitem__(self, key):
        return self.__banner[key]

    def keys(self):
        return self.__banner.keys()

    def __str__(self):
        return str(self.__banner)

# Minicap使用套接字连接从设备接收数据，处理数据，并将其转换为Python可以使用的图像格式。用于捕获设备的屏幕。
class Minicap:

    # 用于存储当前屏幕图像的变量。
    cur_image = None

    # 使用套接字连接的主机和端口以及一个Banner对象来初始化类。
    def __init__(self, host, port, banner):
        self.__socket = None
        self.buffer_size = 4096
        self.host = host
        self.port = port
        self.banner = banner

    # 启动。此方法启动屏幕捕获过程。它建立套接字连接并开始捕获屏幕。
    def start(self):
        self.connect()
        self.start_cap()

    # 停止，关闭套接字连接。
    def stop(self):
        self.__socket.close()

    # 获取屏幕。此方法返回当前屏幕的图像。如果没有图像可用，则返回None。
    def get_screen(self):
        if self.cur_image is None:
            return None
        # 以BGR格式返回当前的屏幕图像
        return cv2.imdecode(numpy.array(self.cur_image, dtype=numpy.uint8), cv2.COLOR_RGBA2BGR)

    # 连接。此方法建立套接字连接。
    def connect(self):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print(e)
            sys.exit(1)
        self.__socket.connect((self.host, self.port))

    # 开始捕获。此方法开始捕获屏幕。它从套接字接收数据并将其转换为图像。
    def start_cap(self):
        read_banner_bytes = 0
        banner_length = 24
        read_frame_bytes = 0
        frame_body_length = 0
        data = []
        # thread = threading.Thread(target=self.debugFrame)
        # thread.start()
        # 获取self.__socket（即套接字连接）的_closed属性。_closed属性表示套接字连接是否已关闭，如果已关闭则为True，否则为False。
        while not getattr(self.__socket, '_closed'):
            try:
                # 从套接字接收数据
                chunk = self.__socket.recv(self.buffer_size)
            except socket.error as e:
                print(e)
                sys.exit(1)

            # cursor用于跟踪chunk中的位置
            cursor = 0
            # buf_len用于跟踪chunk的长度
            buf_len = len(chunk)
            while cursor < buf_len:
                # 如果read_banner_bytes小于banner_length，则将chunk中的数据解包并存储在banner中。
                if read_banner_bytes < banner_length:
                    # map一个lambda表达式，它接受两个参数i和val，并调用self.banner.__setitem__方法将val存储在self.banner的第i个键对应的值中。
                    # struct.unpack()函数解包数据。它的第一个参数是格式字符串，它指定了如何解包数据。第二个参数是要解包的数据。
                    # 例如，"<2b5ibB"是一个格式字符串，它指定了如何解包数据。它指定了数据的类型和顺序。
                    # map()函数将一个函数应用于一个或多个序列的每个元素。它的第一个参数是一个函数，它的第二个参数是一个或多个序列。
                    # 例如，self.banner.__setitem__(self.banner.keys()[i], val)将解包的数据存储在banner中。
                    # 例如，self.banner.keys()返回一个包含banner的键的列表。
                    map(lambda i, val: self.banner.__setitem__(self.banner.keys()[i], val),
                        [i for i in range(len(self.banner.keys()))], struct.unpack("<2b5ibB", chunk))
                    cursor = buf_len
                    read_banner_bytes = banner_length
                # 如果read_frame_bytes小于4，则将chunk中的数据解包并存储在frame_body_length中。
                elif read_frame_bytes < 4:
                    # TODO 为什么这么做？
                    frame_body_length += (chunk[cursor] << (read_frame_bytes * 8)) >> 0
                    cursor += 1
                    read_frame_bytes += 1
                else:
                    if buf_len - cursor >= frame_body_length:
                        data.extend(chunk[cursor:cursor + frame_body_length])
                        # save img
                        self.cur_image = data
                        # self.cur_image = cv2.imdecode(numpy.array(data, dtype=numpy.uint8), cv2.COLOR_RGBA2BGR)
                        cursor += frame_body_length
                        frame_body_length = read_frame_bytes = 0
                        data = []
                    else:
                        data.extend(chunk[cursor:buf_len])
                        frame_body_length -= buf_len - cursor
                        read_frame_bytes += buf_len - cursor
                        cursor = buf_len
        print("socket closed")
