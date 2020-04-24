import time

import cv2
import imagezmq
import numpy as np

from utilities.stats import MovingAverage
from object_detection.object_detection import Model
from utilities.render import Render


def main():
    model = Model()
    model.load_model('models_edgetpu/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')
    model.load_labels('labels_edgetpu/coco_labels.txt')

    image_hub = imagezmq.ImageHub()
    print('RPi Stream -> Receiver Initialized')
    time.sleep(1.0)
    render = Render()
    print('RPi Stream -> Render Ready')

    moving_average_fps = MovingAverage(50)
    moving_average_receive_time = MovingAverage(50)
    moving_average_decompress_time = MovingAverage(50)
    moving_average_model_load_image_time = MovingAverage(50)
    moving_average_model_inference_time = MovingAverage(50)
    moving_average_reply_time = MovingAverage(50)
    moving_average_image_show_time = MovingAverage(50)
    image_count = 0
    print('RPi Stream -> Receiver Streaming')
    while True:
        start_time = time.monotonic()

        name, compressed = image_hub.recv_jpg()
        received_time = time.monotonic()

        image = cv2.imdecode(np.frombuffer(compressed, dtype='uint8'), -1)
        decompressed_time = time.monotonic()

        model.load_image_pil_backend(image)
        model_loaded_image_time = time.monotonic()

        class_ids, scores, boxes = model.inference()
        model_inferenced_time = time.monotonic()

        image_hub.send_reply(b'OK')
        replied_time = time.monotonic()

        render.set_image(image)
        render.render_detection(class_ids, scores, boxes, image.shape[1], image.shape[0], model.image_scale, (45, 227, 227), 3)
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
        model_load_image_time = model_loaded_image_time - decompressed_time
        moving_average_model_load_image_time.add(model_load_image_time)
        model_inference_time = model_inferenced_time - model_loaded_image_time
        moving_average_model_inference_time.add(model_inference_time)
        reply_time = replied_time - model_inferenced_time
        moving_average_reply_time.add(reply_time)
        image_show_time = image_showed_time - replied_time
        moving_average_image_show_time.add(image_show_time)

        total_time = moving_average_receive_time.get_moving_average() \
                     + moving_average_decompress_time.get_moving_average() \
                     + moving_average_model_load_image_time.get_moving_average() \
                     + moving_average_model_inference_time.get_moving_average() \
                     + moving_average_reply_time.get_moving_average() \
                     + moving_average_image_show_time.get_moving_average()
        if image_count % 10 == 0:
            print(" receiver's fps: %4.1f"
                  " receiver's time components: "
                      "receiving %4.1f%% "
                      "decompressing %4.1f%% "
                      "model load image %4.1f%% "
                      "model inference %4.1f%% "
                      "replying %4.1f%% "
                      "image show %4.1f%%"
                  % (moving_average_fps.get_moving_average(),
                     moving_average_receive_time.get_moving_average() / total_time * 100,
                     moving_average_decompress_time.get_moving_average() / total_time * 100,
                     moving_average_model_load_image_time.get_moving_average() / total_time * 100,
                     moving_average_model_inference_time.get_moving_average() / total_time * 100,
                     moving_average_reply_time.get_moving_average() / total_time * 100,
                     moving_average_image_show_time.get_moving_average() / total_time * 100), end='\r')
        image_count += 1
        if image_count == 10000000:
            image_count = 0


if __name__ == "__main__":
    main()
