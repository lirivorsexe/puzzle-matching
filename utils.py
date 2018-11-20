import numpy as np


def distance_to_line(point, l1, l2):
    return np.linalg.norm(np.cross(l2 - l1, l1 - point)) / np.linalg.norm(l2 - l1)


def perpendicular(a):
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b


def normalize(a):
    a = np.array(a)
    return a / np.linalg.norm(a)


def vector_length(v):
    return (v[0] ** 2 + v[1] ** 2) ** 0.5


def distance_by_coords(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return vector_length([dx, dy])


def distance_by_points(p1, p2):
    [x1, y1] = p1
    [x2, y2] = p2
    return distance_by_coords(x1, y1, x2, y2)


def dot_product(v, u):
    return v[0] * u[0] + v[1] * u[1]


def cosine_between_vectors(v, u):
    return dot_product(v, u) / vector_length(v) / vector_length(u)
