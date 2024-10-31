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

# Apply elementary operations if specified
if 'brightness' in args_dict:
    brightness_factor = int(args_dict['brightness'])
    pixels = adjust_brightness(pixels, brightness_factor)
    save_image(pixels, mode, size, 'output_brightness.bmp')  # Save after brightness adjustment

if 'contrast' in args_dict:
    contrast_factor = float(args_dict['contrast'])
    pixels = adjust_contrast(pixels, contrast_factor)
    save_image(pixels, mode, size, 'output_contrast.bmp')  # Save after contrast adjustment

if 'negative' in args_dict:
    pixels = apply_negative(pixels)
    save_image(pixels, mode, size, 'output_negative.bmp')  # Save after negative application

# Apply geometric operations if specified
if 'hflip' in args_dict:
    pixels = horizontal_flip(pixels, size[0], size[1])
    save_image(pixels, mode, size, 'output_hflip.bmp')  # Save after horizontal flip

if 'vflip' in args_dict:
    pixels = vertical_flip(pixels, size[0], size[1])
    save_image(pixels, mode, size, 'output_vflip.bmp')  # Save after vertical flip

if 'dflip' in args_dict:
    pixels = diagonal_flip(pixels, size[0], size[1])
    save_image(pixels, mode, size, 'output_dflip.bmp')  # Save after diagonal flip

if 'shrink' in args_dict:
    shrink_factor = int(args_dict['shrink'])
    pixels, new_width, new_height = shrink_image(pixels, size[0], size[1], shrink_factor)
    size = (new_width, new_height)
    save_image(pixels, mode, size, 'output_shrink.bmp')  # Save after shrinking

if 'enlarge' in args_dict:
    enlarge_factor = int(args_dict['enlarge'])
    pixels, new_width, new_height = enlarge_image(pixels, size[0], size[1], enlarge_factor)
    size = (new_width, new_height)
    save_image(pixels, mode, size, 'output_enlarge.bmp')  # Save after enlarging

# Apply alpha-trimmed mean filter if specified
if 'alpha' in args_dict:
    try:
        alpha_value = int(args_dict['alpha'])
        kernel_size = 3  # Default kernel size, can make this configurable
        print(f"Applying alpha-trimmed mean filter with alpha {alpha_value}")
        pixels = alpha_trimmed_mean_filter(noisy_pixels, size_noisy[0], size_noisy[1], kernel_size, alpha_value)
        save_image(pixels, mode, size, 'output_alpha.bmp')  # Save
    except ValueError:
        print("Error: Alpha value must be an integer.")

# Apply geometric mean filter if specified
if 'gmean' in args_dict:
    try:
        gmean_value = int(args_dict['gmean'])
        kernel_size = 3  # Default kernel size, can make this configurable
        print(f"Applying geometric mean filter with value {gmean_value}")
        pixels = geometric_mean_filter(noisy_pixels, size_noisy[0], size_noisy[1], kernel_size)
        save_image(pixels, mode, size, 'output_gmean.bmp')  # Save
    except ValueError:
        print("Error: Gmean value must be an integer.")

# Perform MSE calculation if specified
if 'mse' in args_dict:
    alpha_value = int(args_dict.get('alpha', 0))  # Default alpha value
    kernel_size = 3  # Adjust as needed

    # Calculate MSE between original and noisy image
    mse_noisy = mean_square_error(original_pixels, noisy_pixels, size_noisy[0], size_noisy[1])

    # Apply alpha-trimmed mean filter to the noisy image
    denoised_pixels = alpha_trimmed_mean_filter(noisy_pixels, size_noisy[0], size_noisy[1], kernel_size, alpha_value)

    # Calculate MSE between original and denoised image
    mse_denoised = mean_square_error(original_pixels, denoised_pixels, size_noisy[0], size_noisy[1])

    # Print the MSE results
    print(f'Mean Square Error (MSE) between original and noisy image: {mse_noisy}')
    print(f'Mean Square Error (MSE) between original and denoised image: {mse_denoised}')
    print(f'The difference between noisy image and denoised image equals: {mse_noisy - mse_denoised}')

# Perform PMSE calculation if specified
if 'pmse' in args_dict:
    alpha_value = int(args_dict.get('alpha', 0))  # Default alpha value
    kernel_size = 3  # Adjust as needed

    # Apply alpha-trimmed mean filter to the noisy image
    denoised_pixels = alpha_trimmed_mean_filter(noisy_pixels, size_noisy[0], size_noisy[1], kernel_size, alpha_value)
    pmse_value = peak_mean_square_error(original_pixels, denoised_pixels, size_noisy[0], size_noisy[1])
    print(f'Peak Mean Square Error (PMSE) between original and denoised image: {pmse_value}')

# Perform SNR calculation if specified
if 'snr' in args_dict:
    alpha_value = int(args_dict.get('alpha', 0))  # Default alpha value
    kernel_size = 3  # Adjust as needed

    # Apply alpha-trimmed mean filter to the noisy image
    denoised_pixels = alpha_trimmed_mean_filter(noisy_pixels, size_noisy[0], size_noisy[1], kernel_size, alpha_value)

    # Calculate SNR between original and denoised image
    snr_value = signal_to_noise_ratio(original_pixels, denoised_pixels, size_noisy[0], size_noisy[1])
    print(f'Signal to Noise Ratio (SNR) between original and denoised image: {snr_value}')

if 'psnr' in args_dict:
    alpha_value = int(args_dict.get('alpha', 0))  # Default alpha value
    kernel_size = 3  # Adjust as needed

    # Apply alpha-trimmed mean filter to the noisy image
    denoised_pixels = alpha_trimmed_mean_filter(noisy_pixels, size_noisy[0], size_noisy[1], kernel_size, alpha_value)

    # Calculate PSNR between original and denoised image
    psnr_value = peak_signal_to_noise_ratio(original_pixels, denoised_pixels, size_noisy[0], size_noisy[1])
    print(f'Peak Signal to Noise Ratio (PSNR) between original and denoised image: {psnr_value}')
    
if 'md' in args_dict:

    alpha_value = int(args_dict.get('alpha', 0))  # Default alpha value
    kernel_size = 3  # Adjust as needed

    # Apply alpha-trimmed mean filter to the noisy image
    denoised_pixels = alpha_trimmed_mean_filter(noisy_pixels, size_noisy[0], size_noisy[1], kernel_size, alpha_value)

    md_value = maximum_difference(original_pixels, denoised_pixels)
    print(f'Maximum Difference (MD) between original and denoised image: {md_value}')

    
if 'mse_gmean' in args_dict:
    kernel_size = 3  # Set default kernel size, can be adjusted

    # Calculate MSE between original and noisy image
    mse_noisy = mean_square_error(original_pixels, noisy_pixels, size_noisy[0], size_noisy[1])

    # Apply geometric mean filter to the noisy image
    gmean_filtered_pixels = geometric_mean_filter(noisy_pixels, size_noisy[0], size_noisy[1], kernel_size)

    # Calculate MSE between original and geometric mean-filtered image
    mse_denoised_gmean = mean_square_error(original_pixels, gmean_filtered_pixels, size_noisy[0], size_noisy[1])

    # Print the MSE results
    print(f'Mean Square Error (MSE) between original and noisy image: {mse_noisy}')
    print(f'Mean Square Error (MSE) between original and geometric mean filtered image: {mse_denoised_gmean}')
    print(f'Difference between noisy and geometric mean filtered image MSE: {mse_noisy - mse_denoised_gmean}')

# Perform PMSE calculation with geometric mean filter if specified
if 'pmse_gmean' in args_dict:
    kernel_size = 3  # Set default kernel size, can be adjusted

    # Apply geometric mean filter to the noisy image
    gmean_filtered_pixels = geometric_mean_filter(noisy_pixels, size_noisy[0], size_noisy[1], kernel_size)
    pmse_value_gmean = peak_mean_square_error(original_pixels, gmean_filtered_pixels, size_noisy[0], size_noisy[1])
    print(f'Peak Mean Square Error (PMSE) between original and geometric mean filtered image: {pmse_value_gmean}')

# Perform SNR calculation with geometric mean filter if specified
if 'snr_gmean' in args_dict:
    kernel_size = 3  # Set default kernel size, can be adjusted

    # Apply geometric mean filter to the noisy image
    gmean_filtered_pixels = geometric_mean_filter(noisy_pixels, size_noisy[0], size_noisy[1], kernel_size)

    # Calculate SNR between original and geometric mean-filtered image
    snr_value_gmean = signal_to_noise_ratio(original_pixels, gmean_filtered_pixels, size_noisy[0], size_noisy[1])
    print(f'Signal to Noise Ratio (SNR) between original and geometric mean filtered image: {snr_value_gmean}')

# Perform PSNR calculation with geometric mean filter if specified
if 'psnr_gmean' in args_dict:
    kernel_size = 3  # Set default kernel size, can be adjusted

    # Apply geometric mean filter to the noisy image
    gmean_filtered_pixels = geometric_mean_filter(noisy_pixels, size_noisy[0], size_noisy[1], kernel_size)

    # Calculate PSNR between original and geometric mean-filtered image
    psnr_value_gmean = peak_signal_to_noise_ratio(original_pixels, gmean_filtered_pixels, size_noisy[0], size_noisy[1])
    print(f'Peak Signal to Noise Ratio (PSNR) between original and geometric mean filtered image: {psnr_value_gmean}')

# Perform MD calculation with geometric mean filter if specified
if 'md_gmean' in args_dict:
    kernel_size = 3  # Set default kernel size, can be adjusted

    # Apply geometric mean filter to the noisy image
    gmean_filtered_pixels = geometric_mean_filter(noisy_pixels, size_noisy[0], size_noisy[1], kernel_size)

    # Calculate Maximum Difference (MD) between original and geometric mean-filtered image
    md_value_gmean = maximum_difference(original_pixels, gmean_filtered_pixels)
    print(f'Maximum Difference (MD) between original and geometric mean filtered image: {md_value_gmean}')