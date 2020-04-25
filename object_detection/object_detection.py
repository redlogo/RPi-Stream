import platform

import cv2
import numpy as np
import tflite_runtime.interpreter as tflite_interpreter
from PIL import Image


def pil_resize_image(image, size):
    """
    Resize a image with PIL backend.
    :param image: Input image.
    :param size: Input size.
    :return: Resized image.
    """
    return image.resize(size, Image.ANTIALIAS)


def cv2_resize_image(image, size):
    """
    Resize a image with cv2 backend.
    :param image: Input image.
    :param size: Input size.
    :return: Resized image.
    """
    return cv2.resize(image, size, interpolation=cv2.INTER_AREA)


class Model:
    """
    This is a class to hold tflite model / interpreter, load image into model, and do inference.
    """
    __slots__ = 'labels', \
                'model_interpreter', \
                'image_scale', \
                'model_width', \
                'model_height', \
                'update_tensor', \
                'model_channel', \
                'confidence_level', \
                'edgetpu_lib'

    def __init__(self):
        self.labels = {}
        self.model_interpreter = None
        self.image_scale = 1
        self.model_width = 0
        self.model_height = 0
        self.update_tensor = None
        self.model_channel = 0
        self.confidence_level = 0.8
        # Darwin means macOS...
        self.edgetpu_lib = {'Linux': 'libedgetpu.so.1',
                            'Darwin': 'libedgetpu.1.dylib',
                            'Windows': 'edgetpu.dll'
                            }[platform.system()]

    def set_confidence_level(self, confidence_level):
        """
        :param confidence_level: For example, 0.8 means model believes 80% chance it is correct.
        :return: nothing
        """
        self.confidence_level = confidence_level

    def load_model(self, model_file_path):
        """
        Load a model into tflite interpreter.
        Tricky part:
            self.update_tensor is a local numpy array that holds image, which is to be updated into the model.
        :param model_file_path: Path of the pre-trained model used.
        :return: nothing
        """

        self.model_interpreter = tflite_interpreter.Interpreter(
            model_path=model_file_path,
            experimental_delegates=[tflite_interpreter.load_delegate(self.edgetpu_lib, {})])
        self.model_interpreter.allocate_tensors()
        _, self.model_height, self.model_width, _ = self.model_interpreter.get_input_details()[0]['shape']
        self.update_tensor = self.model_interpreter.get_tensor(self.model_interpreter.get_input_details()[0]['index'])
        _, _, _, self.model_channel = self.update_tensor.shape
        print('RPi Stream -> Coral TPU Model Loaded: ' + model_file_path)

    def load_labels(self, label_file_path):
        """
        Load labels into tflite interpreter.
        :param label_file_path: Path of the labels corresponding to the pre-trained model used.
        :return: nothing
        """
        with open(label_file_path, 'r') as opened_file:
            line = opened_file.readline()
            while line and len(line) != 0:
                splits = line.strip().split('  ', 2)
                self.labels[int(splits[0])] = splits[1]
                line = opened_file.readline()
        print('RPi Stream -> Labels Loaded: ' + label_file_path)

    def load_image_pil_backend(self, image):
        """
        Load image into the model.
        :param image: Image to be loaded in PIL.Image format
        :return: nothing
        """
        # translate into numpy array
        image = Image.fromarray(image, 'RGB')
        input_width, input_height = image.size

        # scaling
        self.image_scale = min(self.model_width / input_width, self.model_height / input_height)
        scaled_input_width = int(input_width * self.image_scale)
        scaled_input_height = int(input_height * self.image_scale)
        image = pil_resize_image(image, (scaled_input_width, scaled_input_height))

        # update the self.update_tensor (numpy array)
        self.update_tensor[0, :scaled_input_height, :scaled_input_width, :] = np.reshape(
            image, (scaled_input_height, scaled_input_width, self.model_channel))
        self.update_tensor[0, scaled_input_height:, scaled_input_width:, :] = 0

        # set model input with new values
        self.model_interpreter.set_tensor(self.model_interpreter.get_input_details()[0]['index'], self.update_tensor)

    def load_image_cv2_backend(self, image):
        """
        Load image into the model.
        :param image: Image to be loaded in numpy array format
        :return: nothing
        """
        input_height, input_width, _ = image.shape

        # scaling
        self.image_scale = min(self.model_width / input_width, self.model_height / input_height)
        scaled_input_width = int(input_width * self.image_scale)
        scaled_input_height = int(input_height * self.image_scale)
        image = cv2_resize_image(image, (scaled_input_width, scaled_input_height))

        # update the self.update_tensor (numpy array)
        self.update_tensor[0, :scaled_input_height, :scaled_input_width, :] = np.reshape(
            image, (scaled_input_height, scaled_input_width, self.model_channel))
        self.update_tensor[0, scaled_input_height:, scaled_input_width:, :] = 0

        # set model input with new values
        self.model_interpreter.set_tensor(self.model_interpreter.get_input_details()[0]['index'], self.update_tensor)

    def inference(self):
        """
        Model inference.
        :return:
            class_ids: a list holds label ids
            scores: confidence levels
            boxes: the boundaries of the detections
        """
        # actual inference just in one line
        self.model_interpreter.invoke()

        # get inference results
        boxes = self.model_interpreter.get_tensor(self.model_interpreter.get_output_details()[0]['index'])[0]
        class_ids = self.model_interpreter.get_tensor(self.model_interpreter.get_output_details()[1]['index'])[0]
        scores = self.model_interpreter.get_tensor(self.model_interpreter.get_output_details()[2]['index'])[0]

        # only return the equal or above confidence_level results
        compare = scores >= self.confidence_level
        indexes = [i for i, val in enumerate(compare) if val]
        return class_ids[indexes], scores[indexes], boxes[indexes]
