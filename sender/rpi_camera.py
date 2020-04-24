import socket

from imutils.video import VideoStream


class RPiCamera:
    """
    This is a class to get video stream from RPi.
    """
    __slots__ = 'width', 'height', 'name', 'camera'

    def __init__(self, width, height):
        # image info
        self.width = width
        self.height = height

        # RPi's name
        self.name = socket.gethostname()

        # RPi's video stream class
        self.camera = VideoStream(usePiCamera=True, resolution=(width, height))

    def start(self):
        """
        Start streaming.
        :return: nothing
        """
        self.camera.start()

    def get_image(self):
        """
        Get individual image (frame) from streaming source.
        :return: An individual image
        """
        return self.camera.read()
