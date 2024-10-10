import sys

from functions.elementary import adjust_brightness, adjust_contrast, apply_negative
from functions.geometric import horizontal_flip, vertical_flip, diagonal_flip, shrink_image, enlarge_image
from functions.noise_removal import alpha_trimmed_mean_filter, geometric_mean_filter
from functions.similarity_measures import mean_square_error, peak_mean_square_error, signal_to_noise_ratio, peak_signal_to_noise_ratio, maximum_difference

from utils.file_operations import load_image, save_image
from utils.help import print_help
from utils.parse_arguments import parse_arguments  

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
original_pixels, mode, size, im = load_image(input_image_path)  # Load original pixels
pixels = original_pixels.copy()  # Create a copy for processing

# Dictionary to store command-line argument values (e.g., brightness, contrast)
args_dict = parse_arguments(commands)

# Apply the elementary operations
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

if 'alpha' in args_dict:
    alpha_value = int(args_dict['alpha'])
    kernel_size = 3  # You can adjust or add a custom kernel size argument if desired
    pixels = alpha_trimmed_mean_filter(pixels, size[0], size[1], kernel_size, alpha_value)

if 'gmean' in args_dict:
    kernel_size = 3  # Fixed kernel size for now, can be adjustable
    pixels = geometric_mean_filter(pixels, size[0], size[1], kernel_size)

if 'mse' in args_dict:
    mse_value = mean_square_error(original_pixels, pixels)
    print(f'Mean Square Error (MSE): {mse_value}')

if 'pmse' in args_dict:
    pmse_value = peak_mean_square_error(original_pixels, pixels)
    print(f'Peak Mean Square Error (PMSE): {pmse_value}')
    
if 'snr' in args_dict:
    snr_value = signal_to_noise_ratio(original_pixels, pixels)
    print(f'Signal to Noise Ratio (SNR): {snr_value}')

if 'psnr' in args_dict:
    psnr_value = peak_signal_to_noise_ratio(original_pixels, pixels)
    print(f'Peak Signal to Noise Ratio (PSNR): {psnr_value}')

if 'md' in args_dict:
    md_value = maximum_difference(original_pixels, pixels)
    print(f'Maximum Difference (MD): {md_value}')

# Save the modified image
save_image(pixels, mode, size, output_image_path)
