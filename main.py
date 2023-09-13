import os
import sys

import match
import preprocess

if __name__ == "__main__":
    dir_path = sys.argv[1] #тут был я
    black_pixel_vectors = {}

    for f in os.listdir(dir_path):
        filename, file_ext = os.path.splitext(f)
        if file_ext == '.png':
            img_trans = preprocess.get_img_trans(os.path.join(dir_path, filename + file_ext))
            black_pixel_vectors[int(filename)] = match.get_black_pixels_vector(img_trans)

    matches = match.get_matches(black_pixel_vectors)
    for i in sorted(matches)[:int(sys.argv[2])]:
        for (score, number) in matches[i]:
            print(number, end=" ")
        print()
