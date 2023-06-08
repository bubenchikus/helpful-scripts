import argparse
import re
import os
from PIL import Image
import math


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--image_directory', '-d',
                        type=str, default=os.getcwd() + '/')
    parser.add_argument('--image_name', '-n',
                        type=str, default=None)
    parser.add_argument('--max_megapixels', '-m', type=float, default=None)

    return vars(parser.parse_args())


def resizer(img_path, max_megapixels):
    img = Image.open(img_path)
    width, height = img.size
    area = width * height / 1_000_000  # in megapixels

    if area > max_megapixels:
        print(f"Working on {file}...")
        factor = math.sqrt(max_megapixels / area)
        new_width = math.floor(width * factor)
        new_height = math.floor(height * factor)
        img.resize((new_width, new_height),
                   Image.LANCZOS).save(img_path)


if __name__ == '__main__':
    args = parse_args()

    if args["image_name"]:
        if os.path.isfile(args["image_name"]):
            resizer(args["image_name"], args['max_megapixels'])
        else:
            print("Image path does not exist!")
    else:
        if os.path.isdir(args["image_directory"]):
            files = [file for file in os.listdir(args["image_directory"]) if re.match(
                ".*\.(?:jpg|jpeg|png|webp)", file)]

            # script changes original files, passing max_megapixels is required to prevent accidental lauch
            if (args['max_megapixels']):
                for file in files:
                    resizer(os.path.join(
                        args["image_directory"], file), args['max_megapixels'])
        else:
            print("Directory does not exist!")
