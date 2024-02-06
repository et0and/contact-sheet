from PIL import Image, ImageDraw, ImageFont
import os

accepted_extensions = (".jpg", ".jpeg", ".png")

def create_contact_sheet(image_paths, output_file, columns=4, rows=6, padding=5):
    # Define the size of the contact sheet
    image_size = 100  # Each image and padding is 100x100 pixels
    contact_sheet_width = columns * image_size
    contact_sheet_height = rows * image_size

    # Create a blank contact sheet
    contact_sheet = Image.new('RGB', (contact_sheet_width, contact_sheet_height), color='white')
    draw = ImageDraw.Draw(contact_sheet)

    x = 0
    y = 0
    for filename in image_paths:
        if filename.lower().endswith(accepted_extensions):
            img = Image.open(filename)
            # Resize the image to fit the grid cell
            img.thumbnail((image_size - padding * 2, image_size - padding * 2), Image.Resampling.LANCZOS)
            # Paste the image into the contact sheet with padding
            contact_sheet.paste(img, (x + padding, y + padding))
            # Draw the file name below the image
            draw.text((x + padding, y + image_size - padding), os.path.basename(filename), fill='black')
            # Move position to the right for the next image
            x += image_size
            if x >= contact_sheet_width:
                x = 0
                y += image_size
                if y >= contact_sheet_height:
                    print("Contact sheet is full.")
                    break

    # Save the contact sheet as a JPEG
    contact_sheet.save(output_file, "JPEG")
    return contact_sheet
