import argparse
import math
import os

from PIL import Image, ImageStat, ImageFilter


# Pixel widths of mobile phones that we'd like to perfectly target.
# Chosen by looking at currently popular widths.
MOBILE_FULL_WIDTHS_TO_TARGET = [
    1440,
    1242,
    1125,
    1080,
    828,
    750,
    720,
    640
];


def output_mobile_images(image_file, destination, percent_viewport, quality):
    widths = [math.ceil(w * (percent_viewport / 100.0)) \
        for w in MOBILE_FULL_WIDTHS_TO_TARGET]

    with Image.open(image_file) as image:
        ratio = image.height / float(image.width)

        for width in widths:
            resized = image.resize((width, round(width * ratio)),
                resample=Image.LANCZOS)
            # For example: some/path/mansfield.jpg => mansfield_1440.jpg
            filename = os.path.splitext(os.path.basename(image_file))[0] + \
                "-" + str(width) + ".jpg"
            save_to = os.path.join(destination, filename)
            resized.save(save_to, "jpeg", quality=quality, optimize=True)

        # Save a placeholder for lazy loading images.
        placeholder_width = widths[-1] // 2
        resized_for_placeholder = image.resize(
            (placeholder_width, round(placeholder_width * ratio)),
            resample=Image.LANCZOS)
        placeholder = resized_for_placeholder.filter(ImageFilter.BoxBlur(3))
        filename = os.path.splitext(os.path.basename(image_file))[0] + \
            "-placeholder.jpg"
        save_to = os.path.join(destination, filename)
        placeholder.save(save_to, "jpeg", quality=quality, optimize=True)


def get_images(path):
    if os.path.isdir(path):
        return [f for f in os.listdir(path) if
            os.path.isfile(os.path.join(path, f))]
    else:
        return [path]


parser = argparse.ArgumentParser()
parser.add_argument("input",
    help="File path to the full image, or folder of full images.")
parser.add_argument("destination",
    help="File path to the folder to send new images.")
parser.add_argument("percent_viewport", type=int,
    help="The percentage of the width of the viewport the image will take.")
parser.add_argument("--quality", type=int, default=80,
    help="The 0-100 desired quality of output image.")
args = parser.parse_args()

images = get_images(args.input)
for image in images:
    output_mobile_images(image, args.destination, args.percent_viewport,
        args.quality)
