from PIL import Image
from PIL import ImageFilter
import random
import os
import copy


def composite_with_blend(src, obj, info, composed_img_name, part_of_img_name, part_of_composite_img_name):
    src_img = Image.open(src)
    obj_img = Image.open(obj)
    x, y = src_img.size

    size_ratio = random.randrange(15, 30) / 100
    obj_x = int(info['src_size'][0] * size_ratio)
    obj_y = int(info['src_size'][1] * size_ratio)

    obj_img = obj_img.resize((obj_x, obj_y))
    obj_img_raw = obj_img.load()

    loc_x = random.randrange(0, x - obj_x)
    loc_y = random.randrange(0, y - obj_y)

    part_of_img = src_img.crop((loc_x, loc_y, loc_x + obj_x, loc_y + obj_y)) # crop src image
    part_of_img.save(part_of_img_name)

    copy_img = copy.deepcopy(part_of_img)                                          # copy croped image

    part_of_img_raw = part_of_img.load()
    for i in range(obj_x):
        for j in range(obj_y):
            if not check_range(obj_img_raw[i, j], info['background'], info['theta']):
                part_of_img_raw[i, j] = obj_img_raw[i, j]                          # composite part_of_image, fire
    blend_img = Image.blend(copy_img, part_of_img, info['alpha'])                 # composite part_of_image, part_of_composite_image with alpha

    src_img.paste(blend_img, (loc_x, loc_y))                                       # composite src_image, composite final part_of_image

    blend_img.save(part_of_composite_img_name)                                     # save
    src_img.save(composed_img_name)


def composite_imgs(src_img, obj_img, info, composed_img_name, part_of_img_name, part_of_composite_img_name):
    x, y = src_img.size

    resize_x, resize_y = info['size']

    obj_img = obj_img.resize((resize_x, resize_y))
    obj_img_raw = obj_img.load()

    loc_x = random.randrange(0, x - resize_x)
    loc_y = random.randrange(int(y / 2), y - resize_y)

    part_of_img = src_img.crop((loc_x, loc_y, loc_x + resize_x, loc_y + resize_y)) # crop src image
    part_of_img.save(part_of_img_name)

    copy_img = copy.deepcopy(part_of_img)                                          # copy croped image

    part_of_img_raw = part_of_img.load()
    for i in range(resize_x):
        for j in range(resize_y):
            if not check_range(obj_img_raw[i, j], info['background'], info['theta']):
                part_of_img_raw[i, j] = obj_img_raw[i, j]                          # composite part_of_image, fire

    part_of_img.filter(ImageFilter.MedianFilter)
    part_of_img.save(part_of_composite_img_name)
    part_of_img = Image.open(part_of_composite_img_name)

    blend_img = Image.blend(copy_img, part_of_img, info['alpha'])                 # composite part_of_image, part_of_composite_image with alpha

    src_img.paste(blend_img, (loc_x, loc_y))                                       # composite src_image, composite final part_of_image

    blend_img.save(part_of_composite_img_name)                                     # save
    src_img.save(composed_img_name)


def composite_fixed_imgs(src_img, obj_img, info, composed_img_name, part_of_img_name, part_of_composite_img_name):
    src_x, src_y = info['src_size']
    src_img = src_img.resize((src_x, src_y))    # set fixed size

    size_ratio = random.randrange(15, 30) / 100
    obj_x = int(info['src_size'][0] * size_ratio)
    obj_y = int(info['src_size'][1] * size_ratio)

    obj_img = obj_img.resize((obj_x, obj_y))    # set fixed size
    obj_img_raw = obj_img.load()                # load obj img pixel data

    loc_x = random.randrange(0, src_x - obj_x)
    loc_y = random.randrange(0, src_y - obj_y)

    part_of_img = src_img.crop((loc_x, loc_y, loc_x + obj_x, loc_y + obj_y)) # crop src image
    part_of_img.save(part_of_img_name)

    copy_img = copy.deepcopy(part_of_img)                                          # copy croped image

    part_of_img_raw = part_of_img.load()
    for i in range(obj_x):
        for j in range(obj_y):
            if not check_range(obj_img_raw[i, j], info['background'], info['theta']):
                part_of_img_raw[i, j] = obj_img_raw[i, j]                          # composite part_of_image, fire

    part_of_img.filter(ImageFilter.MedianFilter)
    part_of_img.save(part_of_composite_img_name)
    part_of_img = Image.open(part_of_composite_img_name)

    blend_img = Image.blend(copy_img, part_of_img, info['alpha'])                 # composite part_of_image, part_of_composite_image with alpha

    src_img.paste(blend_img, (loc_x, loc_y))                                       # composite src_image, composite final part_of_image

    blend_img.save(part_of_composite_img_name)                                     # save
    src_img.save(composed_img_name)

    return src_img, [loc_x, loc_y, obj_x, obj_y]                                                         # for saving np data


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
    part_of_img_name = 'part_of_img.jpg'
    part_of_composite_img_name = 'part_of_composite_img.jpg'

    info = {'background': (0, 0, 0), 'theta': 20, 'alpha': 0.65, 'src_size': (256, 256)}

    composite_with_blend(join(dir, src), join(dir, obj), info, join(dir, composed_img_name), join(dir, part_of_img_name), join(dir, part_of_composite_img_name))