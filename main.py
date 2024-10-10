import sys
from PIL import Image

# ==============================
# FUNCTION DEFINITIONS
# ==============================

def load_image(image_path):
    """Loads an image and returns a pixel matrix."""
    try:
        im = Image.open(image_path)
        pixels = list(im.getdata())  # Get the pixels as a flat list
        width, height = im.size
        return pixels, im.mode, (width, height)
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

def parse_arguments(arguments):
    """Parses the command-line arguments in the form of -argument=value."""
    args_dict = {}
    for arg in arguments:
        if '=' in arg and arg.startswith('-'):
            key, value = arg.lstrip('-').split('=', 1)
            args_dict[key] = value
    return args_dict

def print_help():
    """Prints available commands and their usage."""
    help_text = """
    Image Processor - Available Commands:
    
    Usage: python3 main.py <input_image> <output_image> --command [-argument=value [...]]
    
    Commands:
      --brightness            Adjust brightness (requires -value)
      --contrast              Adjust contrast (requires -value)
      --negative              Apply a negative filter (no additional arguments)
    
    Example Usage:
      python3 main.py input.bmp output.bmp --brightness -value=50
      python3 main.py input.bmp output.bmp --contrast -value=1.5
      python3 main.py input.bmp output.bmp --brightness -value=50 --contrast -value=1.2
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
command = sys.argv[3]

# Load the image
pixels, mode, size = load_image(input_image_path)

# Dictionary to store command-line argument values (e.g., brightness, contrast)
args_dict = parse_arguments(sys.argv[4:])

# Apply the command based on input
if command == '--brightness':
    if 'value' not in args_dict:
        print("Error: Missing brightness value argument.")
        sys.exit()
    brightness_factor = int(args_dict['value'])  # Get the brightness factor
    pixels = adjust_brightness(pixels, brightness_factor)

elif command == '--contrast':
    if 'value' not in args_dict:
        print("Error: Missing contrast value argument.")
        sys.exit()
    contrast_factor = float(args_dict['value'])  # Get the contrast factor
    pixels = adjust_contrast(pixels, contrast_factor)

elif command == '--negative':
    pixels = apply_negative(pixels)

else:
    print(f"Unknown command: {command}")
    sys.exit()

# Apply multiple operations if more than one command is given
if '--brightness' in sys.argv and '--contrast' in sys.argv:
    if 'value' in args_dict:
        brightness_factor = int(args_dict['value'])
        contrast_factor = float(args_dict['value'])
        pixels = adjust_brightness(pixels, brightness_factor)
        pixels = adjust_contrast(pixels, contrast_factor)

# Save the modified image
save_image(pixels, mode, size, output_image_path)
