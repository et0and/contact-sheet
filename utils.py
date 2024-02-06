from PIL import Image
import os

accepted_extensions = (".jpg", ".jpeg", ".png")

def create_contact_sheet_no_crop(image_paths, output_file, img_size):
    # Define the size of the contact sheet
    contact_sheet_width = 4 * img_size  # 4 columns
    contact_sheet_height = 6 * img_size  # 6 rows

    # Create a blank contact sheet
    contact_sheet = Image.new('RGB', (contact_sheet_width, contact_sheet_height))

    x = 0
    y = 0
    for filename in image_paths:
        if filename.lower().endswith(accepted_extensions):
            img = Image.open(filename)
            # Resize the image to fit the grid cell
            img.thumbnail((img_size, img_size), Image.ANTIALIAS)
            # Paste the image into the contact sheet
            contact_sheet.paste(img, (x, y))
            # Move position to the right for the next image
            x += img_size
            if x >= contact_sheet_width:
                x = 0
                y += img_size
                if y >= contact_sheet_height:
                    print("Contact sheet is full.")
                    break

    # Save the contact sheet
    contact_sheet.save(output_file)
    return contact_sheet
