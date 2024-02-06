import os
from PIL import Image
import streamlit as st
from utils import create_contact_sheet_no_crop, heic_converter

accepted_extensions = (".jpg", ".jpeg", ".png")

def generate_thumbnail(image_path, output_dir, thumbnail_max_size):
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

def create_contact_sheet(image_paths, output_file, thumbnail_max_size):
    output_dir = "thumbnails"
    os.makedirs(output_dir, exist_ok=True)

    thumbnail_max_size = (100, 100)
    thumbnails = []

    for image_path in image_paths:
        thumbnails.append(generate_thumbnail(image_path, output_dir, thumbnail_max_size))

    thumbnail_size = max(thumbnail_max_size)
    square_size = (thumbnail_size * 4 + 10, thumbnail_size * 6 + 10)

    contact_sheet = Image.new("RGB", square_size)
    x_offset, y_offset = 0, 0
    for thumbnail in thumbnails:
        img = Image.open(os.path.join(output_dir, os.path.basename(thumbnail[0])))
        contact_sheet.paste(img, (x_offset + 10, y_offset + 10))
        x_offset += thumbnail[1] + 10
        if x_offset >= thumbnail_size * 4 + 10:
            x_offset = 0
            y_offset += thumbnail[2] + 10

    contact_sheet.save(output_file)

    for file in os.listdir(output_dir):
        os.remove(os.path.join(output_dir, file))
    os.rmdir(output_dir)

def main():
    st.title('Contact Sheet Generator')

    output_file = 'contact_sheet.jpg'
    image_files = st.file_uploader('Upload images', type=accepted_extensions, accept_multiple_files=True)
    heic_arg = st.checkbox('Convert HEIC images')
    spacing = st.number_input('Spacing between images', value=10)

    if st.button('Generate Contact Sheet'):
        if image_files:
            image_paths = []
            for image_file in image_files:
                file_path = os.path.join("uploaded_images", image_file.name)
                with open(file_path, "wb") as f:
                    f.write(image_file.getbuffer())
                image_paths.append(file_path)

                if heic_arg and image_file.name.lower().endswith(".heic"):
                    heic_converter(path=file_path, out_path=file_path.replace(".heic", ".jpg"), format='jpg')

            create_contact_sheet(image_paths, output_file, (100, 100))

            # Display the contact sheet
            st.image(Image.open(output_file), caption='Generated Contact Sheet', use_column_width=True)

            # Clean up uploaded images
            for file_path in image_paths:
                os.remove(file_path)

if __name__ == "__main__":
    main()
