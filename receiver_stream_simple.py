import time

import cv2
import imagezmq
import numpy as np

from utilities.stats import MovingAverage


def main():
    moving_average_points = 50

    image_hub = imagezmq.ImageHub()
    print('RPi Stream -> Receiver Initialized')
    time.sleep(1.0)
    print('RPi Stream -> Receiver Streaming')

    moving_average_fps = MovingAverage(moving_average_points)
    moving_average_receive_time = MovingAverage(moving_average_points)
    moving_average_decompress_time = MovingAverage(moving_average_points)
    moving_average_reply_time = MovingAverage(moving_average_points)
    moving_average_image_show_time = MovingAverage(moving_average_points)
    while True:
        start_time = time.monotonic()

        name, compressed = image_hub.recv_jpg()
        received_time = time.monotonic()

        image = cv2.imdecode(np.frombuffer(compressed, dtype='uint8'), -1)
        decompressed_time = time.monotonic()

        image_hub.send_reply(b'OK')
        replied_time = time.monotonic()

        cv2.imshow(name, image)
        image_showed_time = time.monotonic()

        if cv2.waitKey(1) == ord('q'):
            break

        instant_fps = 1 / (image_showed_time - start_time)
        moving_average_fps.add(instant_fps)
        receive_time = received_time - start_time
        moving_average_receive_time.add(receive_time)
        decompress_time = decompressed_time - received_time
        moving_average_decompress_time.add(decompress_time)
        reply_time = replied_time - decompressed_time
        moving_average_reply_time.add(reply_time)
        image_show_time = image_showed_time - replied_time
        moving_average_image_show_time.add(image_show_time)

        total_time = moving_average_receive_time.get_moving_average() \
                     + moving_average_decompress_time.get_moving_average() \
                     + moving_average_reply_time.get_moving_average() \
                     + moving_average_image_show_time.get_moving_average()

        print(" receiver's fps: %.1f"
              " receiver's time components: receiving %.1f%% decompressing %.1f%% replying %.1f%% image show %.1f%%"
              % (moving_average_fps.get_moving_average(),
                 moving_average_receive_time.get_moving_average() / total_time * 100,
                 moving_average_decompress_time.get_moving_average() / total_time * 100,
                 moving_average_reply_time.get_moving_average() / total_time * 100,
                 moving_average_image_show_time.get_moving_average() / total_time * 100), end='\r')


if __name__ == "__main__":
    main()
