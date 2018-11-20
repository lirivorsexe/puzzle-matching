import bisect

import numpy as np


def get_black_pixels_vector(img):
    maximum = 0
    black_pixels_vector = np.ndarray([img.shape[1]], dtype=np.float)
    for j in np.arange(img.shape[1]):
        i = 0
        while i < img.shape[0] and img[i][j] < 127:
            i += 1
        black_pixels_vector[j] = i
        if i > maximum:
            maximum = i
    return black_pixels_vector


def get_matches(black_pixel_vectors):
    matches = {}
    for i, curr in black_pixel_vectors.items():
        matches[i] = []
        for j, temp in black_pixel_vectors.items():
            if i != j:
                vectors_sum = curr + temp[::-1]
                std = np.std(vectors_sum)
                bisect.insort_left(matches[i], (std, j))
    return matches
