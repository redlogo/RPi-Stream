import time

import cv2
import imagezmq


class Sender:
    """
    Sender class to do actual sending related process
    """
    __slots__ = 'target_ip', 'target_port', 'sender', 'quality'

    def __init__(self, target_ip, target_port):
        self.target_ip = target_ip
        self.target_port = target_port
        self.quality = 95

        # imagezmq backend
        self.sender = imagezmq.ImageSender(connect_to='tcp://' + self.target_ip + ':' + self.target_port)

    def set_quality(self, quality):
        """
        Image compressing quality.
        The lower, the better networking efficiency.
        Lower image quality may impact deep learning quality.
        :param quality: Image quality.
        :return: nothing
        """
        self.quality = quality

    def send_image_raw(self, name, image):
        """
        Send raw image (numpy array), low efficiency.
        :param name: Name.
        :param image: Image input as numpy array.
        :return: nothing
        """
        self.sender.send_image(name, image)

    def send_image_compressed(self, name, image, profiling):
        """
        Send compressed image (jpg), high efficiency
        :param name: Name.
        :param image: Image input as numpy array.
        :return: statistics of how long time it takes to compress, and to send image
        """
        if profiling:
            start_time = time.monotonic()

        # compress image
        _, compressed_image = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), self.quality])
        if profiling:
            compress_finish_time = time.monotonic()

        # send image
        self.sender.send_jpg(name, compressed_image)
        if profiling:
            send_finish_time = time.monotonic()

        if profiling:
            return compress_finish_time - start_time, send_finish_time - compress_finish_time
        else:
            return 0, 0
