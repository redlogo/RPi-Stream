import time
from sender.rpi_camera import RPiCamera
from sender.sender_engine import Sender


def main():
    width = 1008
    height = 512
    target_ip = '192.168.7.33'
    target_port = '5555'

    image_sender = Sender(target_ip, target_port)
    image_sender.set_quality(75)

    rpi_cam = RPiCamera(width, height)
    rpi_cam.start()
    time.sleep(2.0)

    while True:
        start_time = time.monotonic()
        image_sender.send_image_compressed(rpi_cam.name, rpi_cam.get_image())
        print("sender fps: %.1f" % (1 / (time.monotonic() - start_time)))


if __name__ == '__main__':
    main()
