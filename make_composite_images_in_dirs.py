import os
import copy
from make_composite_image import composite_with_img
from make_composite_image import join
from PIL import Image


def composite_images_in_dirs(src_dir, obj_dir, info, composed_dir, part_of_imgs_dir, part_of_composite_imgs_dir):
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
            composite_with_img(src_img, obj_img, info,
                                 join(composed_dir, str(idx) + '.jpg'), join(part_of_imgs_dir, str(idx) + '.jpg'), join(part_of_composite_imgs_dir, str(idx) + '.jpg'))
            idx += 1


if __name__ == '__main__':
    src_dir = 'test/src'
    obj_dir = 'test/obj'
    composed_dir = 'test/composed'
    part_of_imgs_dir = 'test/part_of_img'
    part_of_composite_imgs_dir = 'test/part_of_composite_img'

    info = {'background': (0, 0, 0), 'theta': 20, 'alpha': 0.6, 'size': (64, 64)}

    composite_images_in_dirs(src_dir, obj_dir, info, composed_dir, part_of_imgs_dir, part_of_composite_imgs_dir)