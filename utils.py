from PIL import Image
import os
import math

accepted_extensions = (".jpg", ".jpeg", ".png")

def create_contact_sheet_no_crop(image_paths, output_file, spacing):
    images = []  # list to hold image objects
    total_size = 0  # total size of all images
    for filename in image_paths:
        if filename.lower().endswith(accepted_extensions):
            img = Image.open(filename)
            images.append(img)
            total_size += img.size[0] * img.size[1]

    # calculate the side of a square that can contain all images
    side = int(math.sqrt(total_size))

    # create a blank canvas
    contact_sheet = Image.new('RGB', (side, side))

    x_offset, y_offset = 0, 0
    for img in images:
        contact_sheet.paste(img, (x_offset, y_offset))
        x_offset += img.size[0] + spacing
        if x_offset >= side:
            x_offset = 0
            y_offset += img.size[1] + spacing

    contact_sheet.save(output_file)

    return contact_sheet
