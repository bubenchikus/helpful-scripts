import argparse
import re
import os
from PIL import Image
import math

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--image_directory', '-d',
                        type=str, default=os.getcwd() + '/')
    parser.add_argument('--max_megapixels', '-m', type=int, default=None)

    args = vars(parser.parse_args())

    if args['image_directory'][-1] != '/':
        args['image_directory'] += '/'

    files = [file for file in os.listdir(args["image_directory"]) if re.match(
        ".*\.(?:jpg|jpeg|png)", file)]

    if (args['max_megapixels']):
        for file in files:
            img = Image.open(args["image_directory"] + file)
            width, height = img.size
            area = width * height / 1_000_000  # in megapixels
            if area > args['max_megapixels']:
                factor = math.sqrt(args['max_megapixels'] / area)
                new_width = math.floor(width * factor)
                new_height = math.floor(height * factor)
                img.resize((new_width, new_height),
                           Image.LANCZOS).save(args['image_directory'] + file)
