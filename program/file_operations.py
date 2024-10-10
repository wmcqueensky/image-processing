import sys
from PIL import Image

def load_image(image_path):
    """Loads an image and returns a pixel matrix."""
    try:
        im = Image.open(image_path)
        pixels = list(im.getdata())  # Get the pixels as a flat list
        width, height = im.size
        return pixels, im.mode, (width, height), im  # Return the image object as well
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' does not exist.")
        sys.exit()

def save_image(pixels, mode, size, output_path):
    """Converts pixel data back to an image and saves it."""
    new_image = Image.new(mode, size)
    new_image.putdata(pixels)
    new_image.save(output_path)
    print(f"Image saved to {output_path}")
