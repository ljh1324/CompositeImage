from make_composite_image import composite_with_blend
from make_composite_images_in_dirs import composite_fixed_imgs_in_dirs

import sys

image_composite_info = {
    'background': (0, 0, 0),
    'theta': 20,
    'alpha': 0.65,
    'src_size': (256, 256)
}

dir_composite_info = {
    'background': (0, 0, 0),
    'theta': 20,
    'alpha': 0.65,
    'src_size': (256, 256)
}

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("python main.py [menu] [arg1] [arg2] ...")
        print("Ex1) python main.py 1 src.jpg obj.jpg composite_image_dir part_of_img_name part_of_composite_img_name")
        print("Ex2) python main.py 2 src_dir obj_dir composite_dir part_of_img_dir part_of_composite_img_dir feature_file_name location_file_name")

    elif sys.argv[1] == '1':
        composite_with_blend(sys.argv[2], sys.argv[3], image_composite_info, sys.argv[4], sys.argv[5], sys.argv[6])
    elif sys.argv[1] == '2':
        composite_fixed_imgs_in_dirs(sys.argv[2], sys.argv[3], dir_composite_info, sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])