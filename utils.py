# utils.py
from PIL import Image
import os
import math

accepted_extensions = (".jpg", ".jpeg", ".png")

def create_contact_sheet_no_crop(image_paths, output_file, img_size):
    images = []  # list to hold image objects
    sizes = []  # list to hold sizes of each image
    total_size = 0  # total size of all images
    if img_size == 0:
        img_size = len(image_paths)
    for filename in image_paths[0:img_size]:
        if filename.lower().endswith(accepted_extensions):
            img = Image.open(filename)
            images.append(img)
            sizes.append(img.size)
            total_size += img.size[0] * img.size[1]

    # calculate the side of a square that can contain all images
    side = int(math.sqrt(total_size))

    # create a blank canvas
    contact_sheet = Image.new('RGB', (side, side))

    # Placeholder for the rectangles and packing logic
    # Since rectpack is not available in Streamlit, you would need to implement your own logic
    all_rects = []
    for i, img in enumerate(images):
        all_rects.append((img.size[0], img.size[1], i))

    return contact_sheet, all_rects, images

def heic_converter(path, out_path, format='jpeg'):
    # Since wand is not available in Streamlit, you would need to find an alternative way to convert HEIC images
    # For example, you could use a system call to a command-line tool like ImageMagick
    os.system(f"magick {path} {out_path}")
