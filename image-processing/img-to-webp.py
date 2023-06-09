import os
import re
import argparse
from PIL import Image


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--image_directory', '-d',
                        type=str, default=os.getcwd() + '/')
    parser.add_argument('--image_name', '-n',
                        type=str, default=None)  # for single images
    parser.add_argument('--remove_originals', '-r',
                        type=bool, default=False)
    parser.add_argument('--min_size', '-m',
                        type=int, default=None)  # in kBs
    parser.add_argument('--quality', '-q',
                        type=int, default=80)

    return vars(parser.parse_args())


def converter(image_name, min_size, quality):
    if min_size is None or os.path.getsize(image_name) > min_size * 1024:
        print(f"Working on {image_name}...")
        img = Image.open(image_name).convert('RGB')
        img.save(os.path.splitext(image_name)[
            0] + '.webp', 'webp', optimize=True, quality=quality)
        if args["remove_originals"]:
            os.remove(image_name)


if __name__ == '__main__':
    args = parse_args()

    if args["image_name"]:
        if os.path.isfile(args["image_name"]):
            converter(args["image_name"], args["min_size"], args["quality"])
        else:
            print("Image path does not exist!")
    else:
        if os.path.isdir(args["image_directory"]):
            files = [file for file in os.listdir(args["image_directory"]) if re.match(
                ".*\.(?:jpg|jpeg|png|webp)", file)]

            for file in files:
                converter(os.path.join(args["image_directory"], file),
                          args["min_size"], args["quality"])
        else:
            print("Directory does not exist!")
