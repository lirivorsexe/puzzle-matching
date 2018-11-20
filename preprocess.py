import cv2
import numpy as np

import persp
import utils


def get_img_trans(file_path):
    img = cv2.imread(file_path)

    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgray = np.float32(imgray)

    corners = get_corners(imgray)
    hull = np.squeeze(cv2.convexHull(corners))

    [c1, b1, b2, c2] = get_significant_points(imgray, hull)
    top, top_vector = get_top(b1, b2, hull)

    cut_point_1 = get_cut_point(b1, c1, top_vector)
    cut_point_2 = get_cut_point(b2, c2, top_vector)

    rect = np.array([cut_point_1, cut_point_2, b2, b1], dtype='float32')
    img_trans = persp.four_point_transform(imgray, rect)
    return img_trans


def get_corners(imgray):
    dst = cv2.cornerHarris(imgray, 2, 3, 0.01)
    dst = cv2.dilate(dst, None)

    ret, dst = cv2.threshold(dst, 0.01 * dst.max(), 255, 0)
    dst = np.uint8(dst)

    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(imgray, np.float32(centroids), (5, 5), (-1, -1), criteria)

    return np.int0(corners)


def get_sections(hull):
    sections = []
    for i in range(-1, len(hull) - 1):
        sections.append(utils.distance_by_points(hull[i], hull[i + 1]))
    return sections


def get_top(b1, b2, hull):
    max_distance = 0
    top = np.array([], dtype=np.int)

    for p in hull:
        distance = utils.distance_to_line(p, b1, b2)
        if distance > max_distance:
            max_distance = distance
            top = p

    top_vector = max_distance * utils.perpendicular(utils.normalize(b2 - b1))
    return top, top_vector


def get_check_points(bottom1, bottom2, top1, top2):
    num_check_poits = 50
    offset = 2
    p1 = [int(bottom1[0] + offset * np.sign(top1[0] - bottom1[0])),
          int(bottom1[1] + offset * np.sign(top1[1] - bottom1[1]))]
    p2 = [int(bottom2[0] + offset * np.sign(top2[0] - bottom2[0])),
          int(bottom2[1] + offset * np.sign(top2[1] - bottom2[1]))]
    return np.array([np.linspace(p1[0], p2[0], num=num_check_poits, dtype=np.int16),
                     np.linspace(p1[1], p2[1], num=num_check_poits, dtype=np.int16)]).T


def is_edge(imgray, bottom1, bottom2, top1, top2, offset):
    max_black_count = 5
    check_points = get_check_points(bottom1, bottom2, top1, top2)
    black_count = 0
    for [x, y] in check_points[offset:]:
        if imgray[y][x] == 0:
            black_count += 1
    return black_count < max_black_count


def are_edges(points, imgray):
    [c1, b1, b2, c2] = points
    return is_edge(imgray, b1, b2, c1, c2, 1) and is_edge(imgray, c1, b1, c2, b2, 20) and is_edge(imgray, c2, b2, c1,
                                                                                                  b1, 20)


def get_significant_points_candidates(sections, hull):
    max_index = sections.index(max(sections))
    points = [np.int0(hull[(max_index + i) % len(hull)]) for i in range(-2, 2)]
    return max_index, points


def get_significant_points(imgray, hull):
    sections = get_sections(hull)
    max_index, points = get_significant_points_candidates(sections, hull)
    while not are_edges(points, imgray):
        sections[max_index] = 0
        max_index, points = get_significant_points_candidates(sections, hull)
    return points


def get_cut_point(b, c, top_vector):
    if top_vector[1] == 0:
        return [b[0] + top_vector[0], b[1]]
    else:
        base_to_corner_vector = [c[0] - b[0], c[1] - b[1]]
        cosine = utils.cosine_between_vectors(base_to_corner_vector, top_vector)
        ratio = utils.vector_length(top_vector) / utils.vector_length(base_to_corner_vector) / cosine
        cut_point_vector = [base_to_corner_vector[0] * ratio, base_to_corner_vector[1] * ratio]
        return np.int0([b[0] + cut_point_vector[0], b[1] + cut_point_vector[1]])
