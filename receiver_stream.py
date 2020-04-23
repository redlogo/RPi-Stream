import cv2
import time
import numpy as np
import imagezmq


def main():
    image_hub = imagezmq.ImageHub()

    while True:
        name, compressed = image_hub.recv_jpg()
        image = cv2.imdecode(np.frombuffer(compressed, dtype='uint8'), -1)
        image_hub.send_reply(b'OK')
        cv2.imshow(name, image)
        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == "__main__":
    main()