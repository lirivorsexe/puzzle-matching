import cv2
import numpy as np

MAX_WIDTH = 210
MAX_HEIGHT = 100
MARGIN_WIDTH = 5


def four_point_transform(img, rect):
    dst = np.array([
        [0, 0],
        [MAX_WIDTH - 1, 0],
        [MAX_WIDTH - 1, MAX_HEIGHT - 1],
        [0, MAX_HEIGHT - 1]], dtype="float32")

    m = cv2.getPerspectiveTransform(rect, dst)

    img_trans = cv2.warpPerspective(img, m, (MAX_WIDTH, MAX_HEIGHT))

    return img_trans[:, MARGIN_WIDTH:-MARGIN_WIDTH]
