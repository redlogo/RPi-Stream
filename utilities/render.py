import cv2


class Render:
    __slots__ = 'image'

    def __init__(self):
        self.image = None

    def set_image(self, image):
        self.image = image

    def render_box(self, box, color, line_width):
        print(box)
        print(color)
        print(line_width)
        cv2.rectangle(self.image, (box[0], box[1]), (box[2], box[3]), color, line_width)

    def render_boxes(self, boxes, color, line_width):
        for box in boxes:
            self.render_box(box, color, line_width)

    def scale_and_trim_boxes(self, boxes, image_width, image_height, scale):
        scaled_boxes = []
        for box in boxes:
            y_min = max(0, int(box[0] * image_height / scale))
            x_min = max(0, int(box[1] * image_width))
            y_max = min(int(image_height / scale), int(box[2] * image_height / scale))
            x_max = min(image_width, int(box[3] * image_width))
            scaled_boxes.append([x_min, y_min, x_max, y_max])
        return scaled_boxes

    def render_detection(self, class_ids, scores, boxes, image_width, image_height, scale, color, line_width):
        self.render_boxes(self.scale_and_trim_boxes(boxes, image_width, image_height, scale), color, line_width)
