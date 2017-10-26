import os
import copy
import numpy as np
import random

from make_composite_image import composite_imgs
from make_composite_image import composite_fixed_imgs
from make_composite_image import join
from PIL import Image


def composite_imgs_in_dirs(src_dir, obj_dir, info, composed_dir, part_of_imgs_dir, part_of_composite_imgs_dir):
    src_files = os.listdir(src_dir)
    obj_files = os.listdir(obj_dir)

    if not os.path.exists(composed_dir):
        os.makedirs(composed_dir)
    if not os.path.exists(part_of_imgs_dir):
        os.makedirs(part_of_imgs_dir)
    if not os.path.exists(part_of_composite_imgs_dir):
        os.makedirs(part_of_composite_imgs_dir)

    src_images = []
    for file in src_files:
        img = Image.open(join(src_dir, file))
        src_images.append(img)

    obj_images = []
    for file in obj_files:
        img = Image.open(join(obj_dir, file))
        obj_images.append(img)

    idx = 1
    for i in range(len(src_images)):
        for j in range(len(src_images)):
            # def composite_with_img(src, obj, info, composed_img_name, part_of_img_name, part_of_composite_img_name)
            src_img = copy.deepcopy(src_images[i])
            obj_img = copy.deepcopy(obj_images[j])
            composite_imgs(src_img, obj_img, info,
                                 join(composed_dir, str(idx) + '.jpg'), join(part_of_imgs_dir, str(idx) + '.jpg'), join(part_of_composite_imgs_dir, str(idx) + '.jpg'))
            idx += 1


def composite_fixed_imgs_in_dirs(src_dir, obj_dir, info, composed_dir, part_of_imgs_dir, part_of_composite_imgs_dir, feature_file_name, location_file_name):
    src_files = os.listdir(src_dir)
    obj_files = os.listdir(obj_dir)

    if not os.path.exists(composed_dir):
        os.makedirs(composed_dir)
    if not os.path.exists(part_of_imgs_dir):
        os.makedirs(part_of_imgs_dir)
    if not os.path.exists(part_of_composite_imgs_dir):
        os.makedirs(part_of_composite_imgs_dir)
    if not os.path.exists(os.path.dirname(feature_file_name)):
        os.makedirs(os.path.dirname(feature_file_name))
    if not os.path.exists(os.path.dirname(location_file_name)):
        os.makedirs(os.path.dirname(location_file_name))

    src_images = []
    for file in src_files:
        img = Image.open(join(src_dir, file))
        src_images.append(img)

    obj_images = []
    for file in obj_files:
        img = Image.open(join(obj_dir, file))
        obj_images.append(img)

    idx = 1

    feature_list = []
    location_list = []
    for i in range(len(src_images)):
        for j in range(len(obj_images)):
            # def composite_with_img(src, obj, info, composed_img_name, part_of_img_name, part_of_composite_img_name)
            src_img = copy.deepcopy(src_images[i])
            obj_img = copy.deepcopy(obj_images[j])

            composite_img, location = composite_fixed_imgs(src_img, obj_img, info,
                                      join(composed_dir, str(idx) + '.jpg'), join(part_of_imgs_dir, str(idx) + '.jpg'), join(part_of_composite_imgs_dir, str(idx) + '.jpg'))

            feature = img_to_numpy(composite_img)
            feature_list.append(feature)
            location_list.append(np.array(location))

            idx += 1
    feature_list = np.array(feature_list)           # list to numpy array
    location_list = np.array(location_list)

    np.save(feature_file_name, feature_list)              # save numpy array
    np.save(location_file_name, location_list)


def img_to_numpy(img):
    x, y = img.size
    img_raw = img.load()
    feature = []
    for i in range(x):
        for j in range(y):
            feature.append(img_raw[i, j][0])
            feature.append(img_raw[i, j][1])
            feature.append(img_raw[i, j][2])
    feature = np.array(feature)
    feature = np.reshape(feature, (x, y, 3))

    return feature


if __name__ == '__main__':
    """
    src_dir = 'test/src'
    obj_dir = 'test/obj'
    composed_dir = 'test/composed'
    part_of_imgs_dir = 'test/part_of_img'
    part_of_composite_imgs_dir = 'test/part_of_composite_img'

    info = {'background': (0, 0, 0), 'theta': 20, 'alpha': 0.6, 'size': (64, 64)}

    composite_imgs_in_dirs(src_dir, obj_dir, info, composed_dir, part_of_imgs_dir, part_of_composite_imgs_dir)
    """

    src_dir = 'test/src'
    obj_dir = 'test/obj'
    composed_dir = 'test/composed'
    part_of_imgs_dir = 'test/part_of_img'
    feature_file_name = 'test/feature/feature.npy'
    location_file_name = 'test/location/location.npy'
    part_of_composite_imgs_dir = 'test/part_of_composite_img'

    info = {'background': (0, 0, 0), 'theta': 20, 'alpha': 0.65, 'src_size': (256, 256)}

    composite_fixed_imgs_in_dirs(src_dir, obj_dir, info, composed_dir, part_of_imgs_dir, part_of_composite_imgs_dir, feature_file_name, location_file_name)