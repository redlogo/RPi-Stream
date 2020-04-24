import time

import cv2
import imagezmq
import numpy as np

from utilities.stats import MovingAverage


def main():
    """
    main function interface
    :return: nothing
    """

    # statistics info
    moving_average_points = 50

    # initialize receiver
    image_hub = imagezmq.ImageHub()
    print('RPi Stream -> Receiver Initialized')
    time.sleep(1.0)

    # statistics
    moving_average_fps = MovingAverage(moving_average_points)
    moving_average_receive_time = MovingAverage(moving_average_points)
    moving_average_decompress_time = MovingAverage(moving_average_points)
    moving_average_reply_time = MovingAverage(moving_average_points)
    moving_average_image_show_time = MovingAverage(moving_average_points)
    image_count = 0

    # streaming
    print('RPi Stream -> Receiver Streaming')
    while True:
        start_time = time.monotonic()

        # receive image
        name, compressed = image_hub.recv_jpg()
        received_time = time.monotonic()

        # decompress image
        image = cv2.imdecode(np.frombuffer(compressed, dtype='uint8'), -1)
        decompressed_time = time.monotonic()

        # send reply
        image_hub.send_reply(b'OK')
        replied_time = time.monotonic()

        # show image
        cv2.imshow(name, image)
        image_showed_time = time.monotonic()
        if cv2.waitKey(1) == ord('q'):
            break

        # statistics
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

        # terminal prints
        if image_count % 10 == 0:
            print(" receiver's fps: %5.1f"
                  " receiver's time components: receiving %4.1f%% decompressing %4.1f%% replying %4.1f%% image show "
                  "%4.1f%% "
                  % (moving_average_fps.get_moving_average(),
                     moving_average_receive_time.get_moving_average() / total_time * 100,
                     moving_average_decompress_time.get_moving_average() / total_time * 100,
                     moving_average_reply_time.get_moving_average() / total_time * 100,
                     moving_average_image_show_time.get_moving_average() / total_time * 100), end='\r')

        # counter
        image_count += 1
        if image_count == 10000000:
            image_count = 0


if __name__ == "__main__":
    main()
