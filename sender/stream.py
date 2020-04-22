import time
from .rpi_camera import RPiCamera
from .sender_engine import Sender


def main():
    width = 1000
    height = 500
    target_ip = '192.168.7.33'
    target_port = '5555'

    rpi_cam = RPiCamera(width, height)
    image_sender = Sender(target_ip, target_port)
    image_sender.set_quality(75)
    time.sleep(2.0)
    while True:
        image_sender.send_image_compressed(rpi_cam.name, rpi_cam.get_image())


if __name__ == '__main__':
    main()
