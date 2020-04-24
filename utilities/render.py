import cv2


def scale_and_trim_boxes(boxes, image_width, image_height):
    """
    Take care of scaling and trimming the boxes output from model, into something actual image can handle.
    :param boxes: Raw boxes output from tflite interpreter.
    :param image_width: Width of actual image.
    :param image_height: Height of actual image.
    :return: Scaled and trimmed boxes of coordinates.
    """
    # Just pure magic to handle the scaling.
    # Model's coordinates is not aligned well with the cv2 image handling coordinates.
    # After many trials, this is the correct version, just use this and don't question.
    scaled_boxes = []
    max_dimension = max(image_width, image_height)
    for box in boxes:
        x_min = max(0, int(box[1] * max_dimension))
        y_min = max(0, int(box[0] * max_dimension))
        x_max = min(image_width, int(box[3] * max_dimension))
        y_max = min(image_height, int(box[2] * max_dimension))
        scaled_boxes.append([x_min, y_min, x_max, y_max])
    return scaled_boxes


class Render:
    """
    A class to handle adding strings or boxes, etc., to the image.
    """
    __slots__ = 'image'

    def __init__(self):
        self.image = None

    def set_image(self, image):
        """
        :param image: Input image.
        :return: nothing
        """
        self.image = image

    def render_fps(self, fps):
        """
        FPS on image.
        :param fps: Input fps.
        :return: nothing
        """
        cv2.putText(self.image, "FPS:%4.1f" % fps, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    def render_detection(self, labels, class_ids, boxes, image_width, image_height, color, line_width):
        """
        Give a named rectangle frame around the object detected.
        :param labels: Label dictionary
        :param class_ids: Label class ids
        :param boxes: Raw boundaries from model
        :param image_width: Width of actual image.
        :param image_height: Height of actual image.
        :param color: Color of the rectangle frame around the object
        :param line_width: Line width of the rectangle frame around the object
        :return: nothing
        """
        # translate the raw boxes into something actual image can handle
        boxes = scale_and_trim_boxes(boxes, image_width, image_height)

        for i in range(len(boxes)):
            class_id = class_ids[i]
            label = labels[class_id]
            box = boxes[i]

            # render name of the object
            cv2.putText(self.image, label, (box[0] + 8, box[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # render the frame around object
            cv2.rectangle(self.image, (box[0], box[1]), (box[2], box[3]), color, line_width)
