import argparse
import time

from sender.rpi_camera import RPiCamera
from sender.sender_engine import Sender
from utilities.stats import MovingAverage


def main():
    """
    main function interface
    :return: nothing
    """
    parser = argparse.ArgumentParser(description='optional inputs')
    parser.add_argument('--profiling', action='store_true')
    args = parser.parse_args()

    # video info
    width = 640
    height = 368
    quality = 65

    # host computer info
    target_ip = '192.168.7.33'
    target_port = '5555'

    # statistics info
    moving_average_points = 50

    # initialize sender
    image_sender = Sender(target_ip, target_port)
    image_sender.set_quality(quality)
    print('RPi Stream -> Sender Initialized')

    # initialize RPi camera
    rpi_cam = RPiCamera(width, height)
    rpi_cam.start()
    print('RPi Stream -> Camera Started')
    time.sleep(1.0)

    # statistics
    moving_average_fps = MovingAverage(moving_average_points)
    moving_average_camera_time = MovingAverage(moving_average_points)
    moving_average_compress_time = MovingAverage(moving_average_points)
    moving_average_send_time = MovingAverage(moving_average_points)
    image_count = 0

    # streaming
    print('RPi Stream -> Start Streaming')
    while True:
        start_time = time.monotonic()

        # capture image
        image = rpi_cam.get_image()
        camera_time = time.monotonic() - start_time
        if args.profiling:
            moving_average_camera_time.add(camera_time)

        # send compressed image (compress + send)
        compress_time, send_time = image_sender.send_image_compressed(rpi_cam.name, image, args.profiling)
        if args.profiling:
            moving_average_compress_time.add(compress_time)
            moving_average_send_time.add(send_time)

        # statistics
        instant_fps = 1 / (time.monotonic() - start_time)
        moving_average_fps.add(instant_fps)
        if args.profiling:
            total_time = moving_average_camera_time.get_moving_average() \
                         + moving_average_compress_time.get_moving_average() \
                         + moving_average_send_time.get_moving_average()

        # terminal prints
        if image_count % 10 == 0:
            if args.profiling:
                print(" sender's fps: %5.1f sender's time components: camera %4.1f%% compressing %4.1f%% sending %4.1f%%"
                      % (moving_average_fps.get_moving_average(),
                         moving_average_camera_time.get_moving_average() / total_time * 100,
                         moving_average_compress_time.get_moving_average() / total_time * 100,
                         moving_average_send_time.get_moving_average() / total_time * 100), end='\r')
            else:
                print(" sender's fps: %5.1f" % moving_average_fps.get_moving_average(), end='\r')

        # counter
        image_count += 1
        if image_count == 10000000:
            image_count = 0


if __name__ == '__main__':
    main()
