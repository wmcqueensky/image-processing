import sys
import numpy as np
from utils.file_operations import load_image, save_image
from utils.help import print_help
from utils.parse_arguments import parse_arguments
from functions.fourier import process_and_save_fourier

# ==============================
# TASK 4 SCRIPT
# ==============================

if len(sys.argv) < 2 or '--help' in sys.argv:
    print_help()
    sys.exit()

input_image_path = sys.argv[1]
output_image_path = sys.argv[2]
commands = sys.argv[3:]

# Load image and extract metadata
original_pixels, mode, size, im = load_image(input_image_path)
pixels = original_pixels.copy()

# Parse command-line arguments into a dictionary
args_dict = parse_arguments(commands)

# Apply Fourier Transform and Inverse Fourier Transform
if "fourier" in args_dict:
    print("Applying Fourier Transform and Inverse Fourier Transform...")
    use_fast = str(args_dict.get("fast", "True")).lower() == "true"  # Default to using fast Fourier transform
    try:
        process_and_save_fourier(
            input_pixels=pixels,
            size=size,
            mode=mode,
            output_base_path=output_image_path.replace('.bmp', ''),
            use_fast=use_fast
        )
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)