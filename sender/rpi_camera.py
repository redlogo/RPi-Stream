import socket

from imutils.video import VideoStream


class RPiCamera:
    __slots__ = 'width', 'height', 'name', 'camera'

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.name = socket.gethostname()
        self.camera = VideoStream(usePiCamera=True, resolution=(width, height))

    def start(self):
        self.camera.start()

    def get_image(self):
        return self.camera.read()
