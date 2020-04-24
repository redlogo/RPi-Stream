import cv2


def scale_and_trim_boxes(boxes, image_width, image_height, scale):
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
    __slots__ = 'image'

    def __init__(self):
        self.image = None

    def set_image(self, image):
        self.image = image

    def render_detection(self, class_ids, scores, boxes, image_width, image_height, scale, color, line_width):
        print(boxes)
        boxes = scale_and_trim_boxes(boxes, image_width, image_height, scale)
        print(boxes)
        for box in boxes:
            cv2.rectangle(self.image, (box[0], box[1]), (box[2], box[3]), color, line_width)
