from PIL import Image
from PIL import ImageFilter
import random
import os


def merge_blur(src, obj, info, composed_img_name, part_of_img_name):
    src_img = Image.open(src)
    obj_img = Image.open(obj)
    x, y = src_img.size

    resize_x = int(x * info['ratio'])
    resize_y = int(y * info['ratio'])

    obj_img = obj_img.resize((resize_x, resize_y))

    src_img_raw = src_img.load()
    obj_img_raw = obj_img.load()

    loc_x = random.randrange(0, x - resize_x)
    loc_y = random.randrange(int(x / 2), y - resize_y)

    for i in range(resize_x):
        for j in range(resize_y):
            if not check_range(obj_img_raw[i, j], info['background'], info['theta']):
                src_img_raw[loc_x + i, loc_y + j] = obj_img_raw[i, j]

    empty_img = Image.new("RGB", (resize_x, resize_y))
    empty_img_raw = empty_img.load()

    for i in range(resize_x):
        for j in range(resize_y):
            empty_img_raw[i, j] = src_img_raw[loc_x + i, loc_y + j]

    empty_img = empty_img.filter(ImageFilter.MedianFilter)

    empty_img.save(part_of_img_name)                # Apply Filter
    empty_img = Image.open(part_of_img_name)

    empty_img_raw = empty_img.load()
    for i in range(resize_x):
        for j in range(resize_y):
            src_img_raw[loc_x + i, loc_y + j] = empty_img_raw[i, j]
    src_img.save(composed_img_name)


def join(dir, file_name):
    return os.path.join(dir, file_name)


def check_range(color, background, theta):
    c_r = color[0]
    c_g = color[1]
    c_b = color[2]

    b_r = background[0]
    b_g = background[1]
    b_b = background[2]

    if b_r - theta <= c_r and c_r <= b_r + theta and b_g - theta <= c_g and c_g <= b_g + theta and b_b - theta <= c_b and c_b <= b_b + theta:
        return True
    return False


if __name__ == '__main__':
    dir = r'test'
    src = 'office.jpg'
    obj = 'fire.jpg'
    composed_img_name = 'composed.jpg'
    part_of_image_name = 'part_of_image.jpg'
    info = { 'ratio' : 0.2, 'background' : (0, 0, 0), 'theta' : 20}
    merge_blur(join(dir, src), join(dir, obj), info, join(dir, composed_img_name), join(dir, part_of_image_name))