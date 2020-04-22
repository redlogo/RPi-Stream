import cv2
import imagezmq


class Sender:
    __slots__ = 'target_ip', 'target_port', 'sender', 'quality'

    def __init__(self, target_ip, target_port):
        self.target_ip = target_ip
        self.target_port = target_port
        self.sender = imagezmq.ImageSender(connect_to='tcp://' + self.target_ip + ':' + self.target_port)
        self.quality = 95

    def send_image_raw(self, name, image):
        self.sender.send_image(name, image)

    def set_quality(self, quality):
        self.quality = quality

    def send_image_compressed(self, name, image):
        _, compressed_image = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), self.quality])
        self.sender.send_jpg(name, compressed_image)
