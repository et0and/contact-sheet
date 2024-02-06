import os
from PIL import Image
import streamlit as st
from utils import create_contact_sheet, heic_converter

accepted_extensions = (".jpg", ".jpeg", ".png")

def main():
    st.title('Contact Sheet Generator')

    output_file = 'contact_sheet.jpg'
    image_files = st.file_uploader('Upload images', type=accepted_extensions, accept_multiple_files=True)
    heic_arg = st.checkbox('Convert HEIC images')
    spacing = st.number_input('Spacing between images', value=10)

    if st.button('Generate Contact Sheet'):
        if image_files:
            # Create the directory if it doesn't exist
            os.makedirs("uploaded_images", exist_ok=True)

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
