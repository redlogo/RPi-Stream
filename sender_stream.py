import time

from sender.rpi_camera import RPiCamera
from sender.sender_engine import Sender
from utilities.stats import MovingAverage


def main():
    width = 1008
    height = 512
    target_ip = '192.168.7.33'
    target_port = '5555'
    quality = 65
    moving_average_points = 50

    image_sender = Sender(target_ip, target_port)
    image_sender.set_quality(quality)
    print('RPi Stream -> Sender Initialized')

    rpi_cam = RPiCamera(width, height)
    rpi_cam.start()
    print('RPi Stream -> Camera Started')
    time.sleep(1.0)

    print('RPi Stream -> Start Streaming')
    moving_average_fps = MovingAverage(moving_average_points)
    moving_average_camera_time = MovingAverage(moving_average_points)
    moving_average_compress_time = MovingAverage(moving_average_points)
    moving_average_send_time = MovingAverage(moving_average_points)
    image_count = 0
    while True:
        start_time = time.monotonic()
        image = rpi_cam.get_image()
        camera_time = time.monotonic() - start_time
        moving_average_camera_time.add(camera_time)
        compress_time, send_time = image_sender.send_image_compressed(rpi_cam.name, image)
        moving_average_compress_time.add(compress_time)
        moving_average_send_time.add(send_time)
        total_time = moving_average_camera_time.get_moving_average() \
                     + moving_average_compress_time.get_moving_average() \
                     + moving_average_send_time.get_moving_average()
        instant_fps = 1 / (time.monotonic() - start_time)
        moving_average_fps.add(instant_fps)
        if image_count % 10 == 0:
            print(" sender's fps: %5.1f sender's time components: camera %4.1f%% compressing %4.1f%% sending %4.1f%%"
                  % (moving_average_fps.get_moving_average(),
                     moving_average_camera_time.get_moving_average() / total_time * 100,
                     moving_average_compress_time.get_moving_average() / total_time * 100,
                     moving_average_send_time.get_moving_average() / total_time * 100), end='\r')
        image_count += 1
        if image_count == 10000000:
            image_count = 0


if __name__ == '__main__':
    main()
