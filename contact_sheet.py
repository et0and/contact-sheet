import os
from PIL import Image
from multiprocessing import Pool
from tqdm import tqdm
import argparse
import random
from utils import create_contact_sheet_no_crop
from utils import heic_converter

accepted_extensions = (".jpg", ".jpeg", ".png")

def generate_thumbnail(image_path, output_dir, thumbnail_max_size, spacing):
    image = Image.open(image_path)
    max_width, max_height = thumbnail_max_size

    # Preserve aspect ratio
    width, height = image.size
    if width > height:
        new_width = max_width
        new_height = int(height * max_width / width)
    else:
        new_height = max_height
        new_width = int(width * max_height / height)

    image = image.resize((new_width, new_height), Image.ANTIALIAS)
    image.save(os.path.join(output_dir, os.path.basename(image_path)))
    return new_width, new_height

def create_contact_sheet(image_paths, output_file, img_size, shuffle, spacing):
    if img_size ==  0:
        img_size = len(image_paths)
    output_dir = "thumbnails"
    os.makedirs(output_dir, exist_ok=True)

    with Pool() as pool, tqdm(total=len(image_paths[0:img_size]), desc="Generating Thumbnails") as pbar:
        thumbnail_max_size = (100,  100)
        results = []
        for image_path in image_paths[0:img_size]:
            results.append(pool.apply_async(generate_thumbnail, (image_path, output_dir, thumbnail_max_size, spacing)))
            pbar.update(1)

        for result in tqdm(results, desc="Processing Thumbnails"):
            result.wait()

    thumbnails = [Image.open(os.path.join(output_dir, file)) for file in os.listdir(output_dir)]
    if shuffle:
        random.shuffle(thumbnails)
    num_thumbnails = len(thumbnails)
    contact_sheet_width =  4
    contact_sheet_height =  6

    thumbnail_size = max(thumbnail_max_size)
    square_size = (thumbnail_size * contact_sheet_width + spacing, thumbnail_size * contact_sheet_height + spacing)

    contact_sheet = Image.new("RGB", square_size)
    x_offset, y_offset =  0,  0
    for thumbnail in thumbnails:
        contact_sheet.paste(thumbnail, (x_offset + spacing, y_offset + spacing))
        x_offset += thumbnail_size + spacing
        if x_offset >= thumbnail_size * contact_sheet_width + spacing:
            x_offset =  0
            y_offset += thumbnail_size + spacing

    contact_sheet.save(output_file)

    for file in os.listdir(output_dir):
        os.remove(os.path.join(output_dir, file))
    os.rmdir(output_dir)

def progress_no_crop(*args):
    for rect in tqdm(args[1], desc='Processing images', unit='image'):
        _, x, y, w, h, rid = rect
        img = args[2][rid].resize((w, h))
        args[0].paste(img, (x, y))
    args[0].save(args[3])

def main(output_file, image_dir=None, file_list=None, no_crop=None, img_size=0, heic_arg=None, shuffle=None, spacing=10):
    if heic_arg:
        heic_image_paths = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.lower().endswith(".heic")]
        for heic_img in heic_image_paths:
            heic_converter(path=heic_img, out_path=str(image_dir + "/" + os.path.basename(heic_img).strip(".heic") + "." + str(heic_arg)), format=heic_arg)

    if file_list is not None:
        with open(file_list, "r") as f:
            image_paths = [line.strip() for line in f.readlines()]
    elif image_dir is not None:
        image_paths = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.lower().endswith(accepted_extensions)]
    else:
        print("Please provide at least folder path or file list.")
    
    if no_crop:
        image_paths = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.lower().endswith(accepted_extensions)]
        if shuffle:
            random.shuffle(image_paths)
        contact_sheet, all_rects, images = create_contact_sheet_no_crop(image_paths, output_file, img_size)
        progress_no_crop(contact_sheet, all_rects, images, output_file)
    else:
        create_contact_sheet(image_paths, output_file, img_size, shuffle, spacing)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Contact Sheet Generator")
    parser.add_argument("output_file", type=str, help="Output file path for contact sheet")
    parser.add_argument("--image_dir", type=str, default=None, help="Directory path containing images")
    parser.add_argument("--file_list", type=str, default=None, help="Path to the file list (filelist.txt) if available")
    parser.add_argument("--img-size", type=int, help="Contact sheet image size", default=0)
    parser.add_argument("--no-crop", help="No crop for generate contact sheet", default=```
