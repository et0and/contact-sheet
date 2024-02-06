from PIL import Image
import os

accepted_extensions = (".jpg", ".jpeg", ".png")

def create_contact_sheet(image_paths, output_file, columns=4, rows=6):
    # Define the size of the contact sheet
    contact_sheet_width = columns * 100  # Each image is 100x100 pixels
    contact_sheet_height = rows * 100

    # Create a blank contact sheet
    contact_sheet = Image.new('RGB', (contact_sheet_width, contact_sheet_height))

    x = 0
    y = 0
    for filename in image_paths:
        if filename.lower().endswith(accepted_extensions):
            img = Image.open(filename)
            # Resize the image to fit the grid cell
            img.thumbnail((100, 100), Image.Resampling.LANCZOS)  # Use Image.Resampling.LANCZOS instead of Image.ANTIALIAS
            # Paste the image into the contact sheet
            contact_sheet.paste(img, (x, y))
            # Move position to the right for the next image
            x += 100
            if x >= contact_sheet_width:
                x = 0
                y += 100
                if y >= contact_sheet_height:
                    print("Contact sheet is full.")
                    break

    # Save the contact sheet as a JPEG
    contact_sheet.save(output_file, "JPEG")
    return contact_sheet
