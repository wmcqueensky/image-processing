import sys
from PIL import Image
import numpy as np

from program.utils.file_operations import load_image
from program.utils.parse_arguments import parse_arguments

# Ensure that the number of arguments is valid for commands
if len(sys.argv) < 3:  # Adjusted from 4 to 3 as output is not always needed
    print("Error: Not enough arguments provided.")
    print("Use --help for command information.")
    sys.exit()

# Input arguments
input_image_path = sys.argv[1]
output_image_path = sys.argv[2]  # Output path for saving images
commands = sys.argv[3:]

# Load the original image without noise
original_pixels, mode, size, im = load_image(input_image_path)  # Load original pixels

# Load the noisy image (you can provide the path as an argument)
noisy_pixels, _, size_noisy, _ = load_image(output_image_path)  # Load noisy pixels (second image)

# Initialize pixels for processing
pixels = original_pixels.copy()  # Create a copy for processing

# Dictionary to store command-line argument values (e.g., brightness, contrast)
args_dict = parse_arguments(commands)