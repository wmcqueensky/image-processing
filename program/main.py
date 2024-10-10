import sys
from elementary import adjust_brightness, adjust_contrast, apply_negative
from geometric import horizontal_flip, vertical_flip, diagonal_flip, shrink_image, enlarge_image
from file_operations import load_image, save_image
from help import print_help

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
save_image(pixels, mode, size, output_image_path)
