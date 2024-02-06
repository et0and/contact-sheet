# utils.py
from PIL import Image
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader  # New import for ImageReader

accepted_extensions = (".jpg", ".jpeg", ".png")

def images_to_pdf(image_paths, output_file, columns=4, rows=6):
    # Calculate the size of each image on the PDF page
    page_width, page_height = letter
    image_width = page_width / columns
    image_height = page_height / rows

    # Create a new PDF with portrait orientation
    c = canvas.Canvas(output_file, pagesize=letter)
    c.setPageRotation(90)  # Rotate the page to portrait orientation

    # Iterate over each image and add it to the PDF
    for i, image_path in enumerate(image_paths):
        if image_path.lower().endswith(accepted_extensions):
            img = Image.open(image_path)
            img.thumbnail((image_width, image_height), Image.Resampling.LANCZOS)  # Resize the image

            # Calculate the position of the image on the page
            x = (i % columns) * image_width
            y = page_height - ((i // columns) * image_height) - image_height

            # Add the image to the PDF
            c.drawImage(ImageReader(img), x, y, image_width, image_height)  # Use drawImage instead of drawInlineImage

            # If we've filled the current page, create a new one
            if (i + 1) % (columns * rows) == 0:
                c.showPage()
                c.setPageRotation(90)  # Rotate the new page to portrait orientation

    # Save the PDF
    c.save()
