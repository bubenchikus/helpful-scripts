import os
import re
import argparse
from PIL import Image


def converter(image_name):
    img = Image.open(image_name).convert('RGB')
    img.save(os.path.splitext(image_name)[
             0] + '.webp', 'webp', optimize=True)
    os.remove(image_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--image_directory', '-d',
                        type=str, default=os.getcwd() + '/')
    parser.add_argument('--image_name', '-n',
                        type=str, default=None)  # for single images

    args = vars(parser.parse_args())

    if args["image_name"]:
        if os.path.isfile(args["image_name"]):
            converter(args["image_name"])
        else:
            print("Image path does not exist!")
    else:
        if args["image_directory"][-1] != "/":
            args["image_directory"] += '/'

        files = [file for file in os.listdir(args["image_directory"]) if re.match(
            ".*\.(?:jpg|jpeg|png)", file)]

        for file in files:
            converter(args["image_directory"] + file)
