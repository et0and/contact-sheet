from PIL import Image, ImageDraw, ImageFont
import os

accepted_extensions = (".jpg", ".jpeg", ".png")

def create_contact_sheet(image_paths, output_dir, columns=4, rows=6, padding=5, padding_bottom=100):
    # Define the size of the contact sheet
    image_size = 100  # Each image and padding is 100x100 pixels
    contact_sheet_width = columns * image_size
    contact_sheet_height = rows * image_size + padding_bottom  # Additional padding at the bottom

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Initialize variables for the current contact sheet
    current_sheet = 1
    x = 0
    y = 0
    contact_sheet = Image.new('RGB', (contact_sheet_width, contact_sheet_height), color='white')
    draw = ImageDraw.Draw(contact_sheet)

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
                    # Save the current contact sheet
                    output_file = os.path.join(output_dir, f'contact_sheet_{current_sheet}.jpg')
                    contact_sheet.save(output_file, "JPEG")
                    print(f"Saved contact sheet {current_sheet}")
                    # Start a new contact sheet
                    current_sheet += 1
                    y = 0
                    contact_sheet = Image.new('RGB', (contact_sheet_width, contact_sheet_height), color='white')
                    draw = ImageDraw.Draw(contact_sheet)

    # Save the last contact sheet
    if y > 0:  # Only save if there are images on the sheet
        output_file = os.path.join(output_dir, f'contact_sheet_{current_sheet}.jpg')
        contact_sheet.save(output_file, "JPEG")
        print(f"Saved contact sheet {current_sheet}")

    return current_sheet  # Return the number of contact sheets generated
