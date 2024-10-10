import sys
from PIL import Image
import math

# ==============================
# FUNCTION DEFINITIONS
# ==============================

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

def adjust_brightness(pixels, factor):
    """Adjust brightness by adding factor to each pixel's RGB value."""
    print(f"Adjusting brightness by a factor of {factor}")
    new_pixels = []
    for pixel in pixels:
        if isinstance(pixel, int):  # Grayscale image
            new_pixel = pixel + factor
            new_pixels.append(max(0, min(255, new_pixel)))
        else:  # RGB image
            new_pixel = tuple(max(0, min(255, channel + factor)) for channel in pixel)
            new_pixels.append(new_pixel)
    return new_pixels

def adjust_contrast(pixels, factor):
    """Adjust contrast by multiplying the distance from 128 (midpoint)."""
    print(f"Adjusting contrast by a factor of {factor}")
    midpoint = 128
    new_pixels = []
    for pixel in pixels:
        if isinstance(pixel, int):  # Grayscale image
            new_pixel = int((pixel - midpoint) * factor + midpoint)
            new_pixels.append(max(0, min(255, new_pixel)))
        else:  # RGB image
            new_pixel = tuple(int((channel - midpoint) * factor + midpoint) for channel in pixel)
            new_pixels.append(tuple(max(0, min(255, channel)) for channel in new_pixel))
    return new_pixels

def apply_negative(pixels):
    """Apply a negative effect by inverting the color of each pixel."""
    print(f"Applying negative filter")
    new_pixels = []
    for pixel in pixels:
        if isinstance(pixel, int):  # Grayscale image
            new_pixels.append(255 - pixel)
        else:  # RGB image
            new_pixels.append(tuple(255 - channel for channel in pixel))
    return new_pixels

# ==============================
# GEOMETRIC OPERATIONS
# ==============================

def horizontal_flip(pixels, width, height):
    """Flip the image horizontally by reversing each row."""
    print("Applying horizontal flip")
    new_pixels = []
    for y in range(height):
        row = pixels[y * width: (y + 1) * width]
        new_pixels.extend(row[::-1])  # Reverse the row
    return new_pixels

def vertical_flip(pixels, width, height):
    """Flip the image vertically by reversing the rows."""
    print("Applying vertical flip")
    new_pixels = []
    for y in range(height - 1, -1, -1):  # Start from the last row and move upwards
        row = pixels[y * width: (y + 1) * width]
        new_pixels.extend(row)
    return new_pixels

def diagonal_flip(pixels, width, height):
    """Flip the image diagonally by first applying a vertical flip and then a horizontal flip."""
    print("Applying diagonal flip (vertical flip followed by horizontal flip)")

    # Step 1: Vertical flip
    vertical_flipped_pixels = [None] * len(pixels)
    for y in range(height):
        for x in range(width):
            vertical_flipped_pixels[y * width + x] = pixels[(height - y - 1) * width + x]

    # Step 2: Horizontal flip
    diagonal_flipped_pixels = [None] * len(pixels)
    for y in range(height):
        for x in range(width):
            diagonal_flipped_pixels[y * width + x] = vertical_flipped_pixels[y * width + (width - x - 1)]

    return diagonal_flipped_pixels


def shrink_image(pixels, width, height, factor):
    """Shrink the image by a given factor."""
    if factor <= 0:
        print("Error: Shrink factor must be greater than 0.")
        sys.exit()
    print(f"Shrinking image by a factor of {factor}")
    new_width = int(width / factor)
    new_height = int(height / factor)
    new_pixels = []

    for y in range(0, height, factor):
        for x in range(0, width, factor):
            new_pixels.append(pixels[y * width + x])  # Pick one pixel per 'factor' block

    return new_pixels, new_width, new_height

def enlarge_image(pixels, width, height, factor):
    """Enlarge the image by a given factor."""
    if factor <= 0:
        print("Error: Enlargement factor must be greater than 0.")
        sys.exit()
    print(f"Enlarging image by a factor of {factor}")
    new_width = int(width * factor)
    new_height = int(height * factor)
    new_pixels = []

    for y in range(height):
        for _ in range(factor):  # Repeat each row 'factor' times
            for x in range(width):
                new_pixels.extend([pixels[y * width + x]] * factor)  # Repeat each pixel 'factor' times

    return new_pixels, new_width, new_height




# ==============================
# ARGUMENT PARSING AND HELP
# ==============================

def parse_arguments(arguments):
    """Parses the command-line arguments in the form of --argument=value."""
    args_dict = {}
    for arg in arguments:
        if '=' in arg and arg.startswith('--'):
            key, value = arg.lstrip('-').split('=', 1)
            args_dict[key] = value
        elif arg.startswith('--'):
            key = arg.lstrip('-')
            args_dict[key] = None
    return args_dict



def print_help():
    help_text = """
    Image Processor - Available Commands:

    Usage: python3 main.py <input_image> <output_image> [--command=value ...]

    Commands:
      --brightness=value      Adjust brightness by the specified value (positive or negative)
      --contrast=value        Adjust contrast by the specified value (e.g., 1.2 to increase, 0.8 to decrease)
      --negative              Apply a negative filter (no additional arguments needed)

      Geometric Operations:
      --hflip                 Flip the image horizontally
      --vflip                 Flip the image vertically
      --dflip                 Flip the image along the diagonal (transpose)
      --shrink=value          Shrink the image by the given factor (e.g., 2 to halve the size)
      --enlarge=value         Enlarge the image by the given factor (e.g., 2 to double the size)

 

    Example Usage:
      python3 main.py input.bmp output.bmp --brightness=50 --contrast=1.5
      python3 main.py input.bmp output.bmp --alpha=2 --gmean
    """
    print(help_text)

# ==============================
# MAIN SCRIPT
# ==============================

if len(sys.argv) < 2 or '--help' in sys.argv:
    print_help()
    sys.exit()

# Ensure that the number of arguments is valid for commands
if len(sys.argv) < 4:
    print("Error: Not enough arguments provided.")
    print("Use --help for command information.")
    sys.exit()

# Input arguments
input_image_path = sys.argv[1]
output_image_path = sys.argv[2]
commands = sys.argv[3:]

# Load the image
pixels, mode, size, im = load_image(input_image_path)

# Dictionary to store command-line argument values (e.g., brightness, contrast)
args_dict = parse_arguments(commands)

# Apply the operations based on input
if 'brightness' in args_dict:
    brightness_factor = int(args_dict['brightness'])  # Get the brightness factor
    pixels = adjust_brightness(pixels, brightness_factor)

if 'contrast' in args_dict:
    contrast_factor = float(args_dict['contrast'])  # Get the contrast factor
    pixels = adjust_contrast(pixels, contrast_factor)

if 'negative' in args_dict:
    pixels = apply_negative(pixels)

# Apply geometric operations
if 'hflip' in args_dict:
    pixels = horizontal_flip(pixels, size[0], size[1])

if 'vflip' in args_dict:
    pixels = vertical_flip(pixels, size[0], size[1])

if 'dflip' in args_dict:
    pixels = diagonal_flip(pixels, size[0], size[1])

if 'shrink' in args_dict:
    shrink_factor = int(args_dict['shrink'])
    pixels, new_width, new_height = shrink_image(pixels, size[0], size[1], shrink_factor)
    size = (new_width, new_height)

if 'enlarge' in args_dict:
    enlarge_factor = int(args_dict['enlarge'])
    pixels, new_width, new_height = enlarge_image(pixels, size[0], size[1], enlarge_factor)
    size = (new_width, new_height)




# Save the modified image
# If geometric transformations are applied, use the image object directly.
save_image(pixels, mode, size, output_image_path)
