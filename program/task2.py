import sys
from PIL import Image
import numpy as np

from functions.histogram import save_histogram_image, calculate_histogram
from functions.characteristics import calculate_mean, calculate_mean_rgb, calculate_variance_rgb, \
    calculate_asymmetry_coefficient, calculate_asymmetry_coefficient_rgb, calculate_flattening_coefficient_rgb, \
    calculate_flattening_coefficient, calculate_variation_coefficient_2_rgb, calculate_variation_coefficient_2, \
    calculate_entropy_rgb, calculate_entropy
from functions.characteristics import calculate_variance, calculate_standard_dev, calculate_variation_coefficient_1
from functions.improvement import power_2_3_pdf
from functions.linear_filtration import optimized_convolution, universal_convolution
from functions.non_linear_filtration import apply_roberts_operator
from utils.file_operations import load_image, save_image
from utils.help import print_help
from utils.parse_arguments import parse_arguments

# ==============================
# TASK 2 SCRIPT
# ==============================

if len(sys.argv) < 2 or '--help' in sys.argv:
    print_help()
    sys.exit()

input_image_path = sys.argv[1]
output_image_path = sys.argv[2]
commands = sys.argv[3:]

original_pixels, mode, size, im = load_image(input_image_path)
pixels = original_pixels.copy()
args_dict = parse_arguments(commands)

if 'histogram' in args_dict:
    print("Calculating and saving histogram...")
    histogram_image_path = args_dict.get('histogram_output', 'histogram.png')
    channels = args_dict.get('channel', [])
    if isinstance(channels, str):
        channels = [channels]
    save_histogram_image(pixels, mode, histogram_image_path, channels)

if 'hpower' in args_dict:
    print('Image improvement using power 2/3 PDF transformation...')
    histogram = calculate_histogram(pixels, mode)  # Ensure this returns a list or tuple of lists
    g_min, g_max = 0, 255
    N = size[0] * size[1]  # Total number of pixels

    for y in range(size[1]):
        for x in range(size[0]):
            index = y * size[0] + x

            if mode == 'L':  # Grayscale image
                f = pixels[index]
                g_f = power_2_3_pdf(histogram, g_min, g_max, f, N)  # Pass grayscale histogram directly
                pixels[index] = int(g_f)

            elif mode == 'RGB':  # RGB image
                r, g, b = pixels[index]
                # Pass each channel histogram separately
                r_new = power_2_3_pdf(histogram[0], g_min, g_max, r, N)
                g_new = power_2_3_pdf(histogram[1], g_min, g_max, g, N)
                b_new = power_2_3_pdf(histogram[2], g_min, g_max, b, N)
                pixels[index] = (int(r_new), int(g_new), int(b_new))

    save_image(pixels, mode, size, 'output_hpower.bmp')
    print("Improved image saved as 'output_hpower.bmp'")
    
if 'cmean' in args_dict:
    print("Calculating mean...")

    # Get the histogram of the image
    histogram = calculate_histogram(pixels, mode)

    # If the image is RGB, we need to handle it differently
    if mode == 'RGB':
        print("Calculating mean for color image...")
        mean = calculate_mean_rgb(histogram)  # Calculate mean for RGB
    else:
        print("Calculating mean for gray image...")
        mean = calculate_mean(histogram)  # Calculate mean for grayscale
    print(f"Mean value: ${mean}")


if 'cvariance' in args_dict:
    print("Calculating variance")

    # Get the histogram of the image
    histogram = calculate_histogram(pixels, mode)


    if mode == 'RGB':
        print("Calculating variance for color image...")
        mean_rgb = calculate_mean_rgb(histogram)  # Calculate mean for RGB
        variance = calculate_variance_rgb(histogram, mean_rgb)
    else:
        print("Calculating variance for gray image...")
        mean = calculate_mean(histogram)  # Calculate mean for grayscale
        variance = calculate_variance(histogram, mean)

    print(f"Variance value: ${variance}")


if "cstdev" in args_dict:
    print("Calculating standard deviation")

    # Get the histogram of the image
    histogram = calculate_histogram(pixels, mode)

    if mode == 'RGB':
        print("Calculating variance for color image...")
        mean_rgb = calculate_mean_rgb(histogram)  # Calculate mean for RGB
        variances = calculate_variance_rgb(histogram, mean_rgb)  # Variance for each RGB channel

        # Calculate the average variance from all RGB channels
        avg_variance = sum(variances.values()) / len(variances)

        # Calculate the standard deviation based on the average variance
        st_dev = calculate_standard_dev(avg_variance)

    else:
        print("Calculating variance for gray image...")
        mean = calculate_mean(histogram)  # Calculate mean for grayscale
        variance = calculate_variance(histogram, mean)
        st_dev = calculate_standard_dev(variance)

    print(f"Standard deviation value: ${st_dev}")


if "cvarcoi" in args_dict:
    print("Calculating variation coefficient")

    # Use previously calculated histogram
    histogram = calculate_histogram(pixels, mode)

    if mode == 'RGB':
        print("Calculating variation coefficient for color image...")
        mean_rgb = calculate_mean_rgb(histogram)  # Calculate mean for RGB
        variances = calculate_variance_rgb(histogram, mean_rgb)  # Variances for each channel

        # Calculate average mean for the RGB channels
        mean = sum(mean_rgb) / len(mean_rgb)

        # Calculate average variance across all channels
        avg_variance = sum(variances.values()) / len(variances)

        # Calculate standard deviation based on the average variance
        dev = calculate_standard_dev(avg_variance)

    else:
        print("Calculating variation coefficient for gray image...")
        mean = calculate_mean(histogram)  # Calculate mean for grayscale
        variance = calculate_variance(histogram, mean)
        dev = calculate_standard_dev(variance)

    # Calculate and print the variation coefficient (stdev / mean)
    var_co = calculate_variation_coefficient_1(dev, mean)

    print(f"Variation coefficient value: ${var_co}")


if "casyco" in args_dict:

    if mode == 'RGB':
        r_histogram, g_histogram, b_histogram = calculate_histogram(pixels, mode)
        # Compute asymmetry coefficient using the histogram
        asym_coe = calculate_asymmetry_coefficient_rgb((r_histogram, g_histogram, b_histogram))
    else:
        histogram = calculate_histogram(pixels, mode)
        # Compute asymmetry coefficient using the histogram
        asym_coe = calculate_asymmetry_coefficient(histogram)

    print("Asymmetry Coefficient:", asym_coe)



if "flaco" in args_dict:

    if mode == 'RGB':
        r_histogram, g_histogram, b_histogram = calculate_histogram(pixels, mode)
        # Compute flattening coefficient using the histogram
        flat_coe = calculate_flattening_coefficient_rgb((r_histogram, g_histogram, b_histogram))
    else:
        histogram = calculate_histogram(pixels, mode)
        # Compute flattening coefficient using the histogram
        flat_coe = calculate_flattening_coefficient(histogram)

    print(f"Flattening coefficient value: ${flat_coe}")


if "cvarcoii" in args_dict:
    if mode == 'RGB':
        r_histogram, g_histogram, b_histogram = calculate_histogram(pixels, mode)
        # Compute Variation Coefficient 2 for each channel
        var_coeffs = calculate_variation_coefficient_2_rgb((r_histogram, g_histogram, b_histogram))
    else:
        histogram = calculate_histogram(pixels, mode)
        # Compute Variation Coefficient 2 for grayscale
        var_coeffs = calculate_variation_coefficient_2(histogram)
    print(f"Variation coefficient II: ${var_coeffs}")


if "centropy" in args_dict:
    if mode == 'RGB':
        r_histogram, g_histogram, b_histogram = calculate_histogram(pixels, mode)
        # Compute entropy for each channel
        entropy_values = calculate_entropy_rgb((r_histogram, g_histogram, b_histogram))
    else:
        histogram = calculate_histogram(pixels, mode)
        # Compute entropy for grayscale
        entropy_values = calculate_entropy(histogram)

    print(f"Entropy value: ${entropy_values}")
    
if 'sexdeti_universal' in args_dict:
    print("Performing detail extraction using universal convolution for a custom or predefined mask...")
    try:
        output_pixels = universal_convolution(pixels, size, args_dict)
        save_image(output_pixels, mode, size, output_image_path)
        filter_type = args_dict.get('filter', 'custom')
        print(f"Detail extraction with universal convolution completed and saved with {filter_type} mask.")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
        
if 'sexdeti' in args_dict:
    print("Performing optimized detail extraction using N mask")
    output_pixels = optimized_convolution(pixels, size)
    save_image(output_pixels, mode, size, output_image_path)
    print(f"Detail extraction with optimized convolution and N filter completed and saved.")

if 'orobertsii' in args_dict:
    print("Applying Roberts II operator for edge detection...")
    pixels = apply_roberts_operator(pixels, size)
    save_image(pixels, mode, size, output_image_path)
    print(f"Edge-detected image saved as '{output_image_path}'")