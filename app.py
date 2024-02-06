import os
from PIL import Image
from multiprocessing import Pool
from tqdm import tqdm
import argparse
import random
from utils import create_contact_sheet_no_crop
from utils import heic_converter
import streamlit as st

# Assuming utils.py contains the following functions:
# - create_contact_sheet_no_crop
# - heic_converter

accepted_extensions = (".jpg", ".jpeg", ".png")

# ... (rest of your functions)

def main():
    st.title('Contact Sheet Generator')

    output_file = st.text_input('Output file path for contact sheet', 'contact_sheet.jpg')
    image_dir = st.text_input('Directory path containing images (or upload images)', 'images/')
    file_list = st.file_uploader('Upload a file list (filelist.txt) if available')
    img_size = st.number_input('Contact sheet image size', value=0)
    heic_arg = st.checkbox('Convert HEIC images')
    shuffle = st.checkbox('Shuffle images')
    spacing = st.number_input('Spacing between images', value=10)
    no_crop = st.checkbox('No crop for generate contact sheet')

    if st.button('Generate Contact Sheet'):
        if heic_arg:
            heic_image_paths = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.lower().endswith(".heic")]
            for heic_img in heic_image_paths:
                heic_converter(path=heic_img, out_path=str(image_dir + "/" + os.path.basename(heic_img).strip(".heic") + "." + str(heic_arg)), format=heic_arg)

        if file_list is not None:
            image_paths = [line.strip() for line in file_list.readlines()]
        elif image_dir is not None:
            image_paths = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.lower().endswith(accepted_extensions)]
        else:
            st.error("Please provide at least folder path or file list.")
            return

        if no_crop:
            image_paths = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.lower().endswith(accepted_extensions)]
            if shuffle:
                random.shuffle(image_paths)
            contact_sheet, all_rects, images = create_contact_sheet_no_crop(image_paths, output_file, img_size)
            progress_no_crop(contact_sheet, all_rects, images, output_file)
        else:
            create_contact_sheet(image_paths, output_file, img_size, shuffle, spacing)

        # Display the contact sheet
        st.image(Image.open(output_file), caption='Generated Contact Sheet', use_column_width=True)

if __name__ == "__main__":
    main()
