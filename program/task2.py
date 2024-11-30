import sys
from PIL import Image
import numpy as np
import os

from functions.histogram import save_histogram_image, calculate_histogram
from functions.characteristics import (
    calculate_mean, calculate_mean_rgb, calculate_variance_rgb,
    calculate_asymmetry_coefficient, calculate_asymmetry_coefficient_rgb,
    calculate_flattening_coefficient_rgb, calculate_flattening_coefficient,
    calculate_variation_coefficient_2_rgb, calculate_variation_coefficient_2,
    calculate_entropy_rgb, calculate_entropy
)
from functions.characteristics import calculate_variance, calculate_standard_dev, calculate_variation_coefficient_1
from functions.improvement import power_2_3_pdf
from functions.linear_filtration import universal_convolution, optimized_convolution_detail_extraction
from functions.non_linear_filtration import apply_roberts_operator
from utils.file_operations import load_image, save_image
from utils.help import print_help
from utils.parse_arguments import parse_arguments

# ==============================
# TASK 2 SCRIPT
# ==============================

def is_binary_image(im):
    """Check if the image is binary (1-bit)."""
    return im.mode == '1'

def convert_to_grayscale(im):
    """Convert binary or color image to grayscale."""
    if is_binary_image(im):
        # Convert binary (1-bit) to 'L' (grayscale)
        return im.convert('L')
    return im  # Return original if already in grayscale

def is_grayscale(rgb_pixels):
    """Check if an RGB image has identical channels."""
    r, g, b = rgb_pixels[:, :, 0], rgb_pixels[:, :, 1], rgb_pixels[:, :, 2]
    return np.array_equal(r, g) and np.array_equal(g, b)

# Main program logic
if len(sys.argv) < 2 or '--help' in sys.argv:
    print_help()
    sys.exit()

input_image_path = sys.argv[1]
output_image_path = sys.argv[2]
commands = sys.argv[3:]

original_pixels, mode, size, im = load_image(input_image_path)
pixels = original_pixels.copy()
args_dict = parse_arguments(commands)

# Handle binary images
if is_binary_image(im):
    im = convert_to_grayscale(im)
    mode = 'L'  # Update mode to grayscale
    original_pixels = list(im.getdata())  # Reload pixels for grayscale mode
    pixels = original_pixels.copy()

# Handle grayscale in RGB mode
if mode == 'RGB' and is_grayscale(np.array(im)):

    im = im.convert('L')
    mode = 'L'  # Update mode to grayscale
    original_pixels = list(im.getdata())  # Reload pixels for grayscale mode
    pixels = original_pixels.copy()

# ========== HISTOGRAM ========== #
if 'histogram' in args_dict:
    print("Calculating and saving histogram...")
    histogram_image_path = args_dict.get('histogram_output', 'histogram.png')
    channels = args_dict.get('channel', [])
    if isinstance(channels, str):
        channels = [channels]
    save_histogram_image(pixels, mode, histogram_image_path, channels)

# ========== POWER TRANSFORMATION (hpower) ========== #
if 'hpower' in args_dict:
    print('Image improvement using power 2/3 PDF transformation...')
    histogram = calculate_histogram(pixels, mode)

    # Convert g_min and g_max to integers
    g_min = int(args_dict.get('gmin', 0))  # Default to 0 if not specified
    g_max = int(args_dict.get('gmax', 255))  # Default to 255 if not specified

    #size = (width, height):
    #size[0] = width of image
    #size[1] = height of image

    N = size[0] * size[1]  # Total number of pixels

    for y in range(size[1]):
        for x in range(size[0]):
            index = y * size[0] + x
            if mode == 'L':  # Grayscale
                f = pixels[index]
                g_f = power_2_3_pdf(histogram, g_min, g_max, f, N)
                pixels[index] = int(g_f)
            elif mode == 'RGB':  # RGB
                r, g, b = pixels[index]
                r_new = power_2_3_pdf(histogram[0], g_min, g_max, r, N)
                g_new = power_2_3_pdf(histogram[1], g_min, g_max, g, N)
                b_new = power_2_3_pdf(histogram[2], g_min, g_max, b, N)
                pixels[index] = (int(r_new), int(g_new), int(b_new))

    save_image(pixels, mode, size, 'output_hpower.bmp')
    print("Improved image saved as 'output_hpower.bmp'")

# ========== STATISTICAL CHARACTERISTICS ========== #
if 'cmean' in args_dict:
    histogram = calculate_histogram(pixels, mode)
    mean = calculate_mean_rgb(histogram) if mode == 'RGB' else calculate_mean(histogram)
    print(f"Mean value: {mean}")

if 'cvariance' in args_dict:
    histogram = calculate_histogram(pixels, mode)
    if mode == 'RGB':
        mean_rgb = calculate_mean_rgb(histogram)
        variance = calculate_variance_rgb(histogram, mean_rgb)
    else:
        mean = calculate_mean(histogram)
        variance = calculate_variance(histogram, mean)
    print(f"Variance value: {variance}")

if "cstdev" in args_dict:
    histogram = calculate_histogram(pixels, mode)
    if mode == 'RGB':
        mean_rgb = calculate_mean_rgb(histogram)  # Calculate mean for R, G, B
        variances = calculate_variance_rgb(histogram, mean_rgb)  # Get variances for R, G, B
        avg_variance = sum(variances) / len(variances)  # Calculate average variance
        st_dev = calculate_standard_dev(avg_variance)  # Calculate standard deviation

        st_dev_r = calculate_standard_dev(variances[0])
        st_dev_g = calculate_standard_dev(variances[2])
        st_dev_b = calculate_standard_dev(variances[2])

        print(f"Standard deviation value for Red channel: {st_dev_r}")
        print(f"Standard deviation value for Green channel: {st_dev_g}")
        print(f"Standard deviation value for Blue channel: {st_dev_b}")

    else:
        mean = calculate_mean(histogram)
        variance = calculate_variance(histogram, mean)
        st_dev = calculate_standard_dev(variance)
    print(f"Standard deviation value: {st_dev}")

if "cvarcoi" in args_dict:
    histogram = calculate_histogram(pixels, mode)
    if mode == 'RGB':
        mean_rgb = calculate_mean_rgb(histogram)
        variances = calculate_variance_rgb(histogram, mean_rgb)
        mean = sum(mean_rgb) / len(mean_rgb)
        avg_variance = sum(variances) / len(variances)
        dev = calculate_standard_dev(avg_variance)


    else:
        mean = calculate_mean(histogram)
        variance = calculate_variance(histogram, mean)
        dev = calculate_standard_dev(variance)
    var_co = calculate_variation_coefficient_1(dev, mean)
    print(f"Variation coefficient value: {var_co}")

if "casyco" in args_dict:
    histogram = calculate_histogram(pixels, mode)
    asym_coe = calculate_asymmetry_coefficient_rgb(histogram) if mode == 'RGB' else calculate_asymmetry_coefficient(histogram)
    print(f"Asymmetry Coefficient: {asym_coe}")

if "flaco" in args_dict:
    histogram = calculate_histogram(pixels, mode)
    flat_coe = calculate_flattening_coefficient_rgb(histogram) if mode == 'RGB' else calculate_flattening_coefficient(histogram)
    print(f"Flattening coefficient: {flat_coe}")

if "cvarcoii" in args_dict:
    histogram = calculate_histogram(pixels, mode)
    var_coeffs = calculate_variation_coefficient_2_rgb(histogram) if mode == 'RGB' else calculate_variation_coefficient_2(histogram)
    print(f"Variation coefficient II: {var_coeffs}")

if "centropy" in args_dict:
    histogram = calculate_histogram(pixels, mode)
    entropy_values = calculate_entropy_rgb(histogram) if mode == 'RGB' else calculate_entropy(histogram)
    print(f"Entropy value: {entropy_values}")

# ========== IMAGE PROCESSING ========== #
if 'sexdeti_universal' in args_dict:
    print("Performing detail extraction using universal convolution...")

if 'sexdeti' in args_dict:
    print("Performing optimized detail extraction...")

if 'orobertsii' in args_dict:
    print("Applying Roberts II operator...")
    pixels = apply_roberts_operator(pixels, size)
    save_image(pixels, mode, size, output_image_path)
    print(f"Edge-detected image saved as '{output_image_path}'")
