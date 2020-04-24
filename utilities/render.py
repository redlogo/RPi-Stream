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

    def render_fps(self, fps):
        cv2.putText(self.image, "FPS:%4.1f" % fps, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    def render_detection(self, labels, class_ids, boxes, image_width, image_height, scale, color, line_width):
        boxes = scale_and_trim_boxes(boxes, image_width, image_height, scale)
        for i in range(len(boxes)):
            class_id = class_ids[i]
            label = labels[class_id]
            box = boxes[i]
            cv2.putText(self.image, label, (box[0] + 8, box[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.rectangle(self.image, (box[0], box[1]), (box[2], box[3]), color, line_width)
