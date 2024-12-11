import sys
import numpy as np
from PIL import Image
from utils.file_operations import load_image, save_image
from utils.help import print_help
from utils.parse_arguments import parse_arguments
from functions.morphological import dilation, erosion, closing, \
    opening, hitOrMiss  # Import the dilate function from morphological.py
from functions.segmentation import region_growing
# ==============================
# TASK 3 SCRIPT
# ==============================


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

# ========== DILATION ========== #
if 'dilation' in args_dict:
    print("Performing dilation on the binary image...")

    original_array = np.array(im)
    print("Original image array:")
    print(original_array)

    # Ensure the image is binary (1-bit)
    if mode == '1':  # Check if the image is binary (1-bit)
        # Convert the binary image to a numpy array (True/False)
        binary_array = np.array(im)  # This already has values of True (white) and False (black)
        print("Binary array:")
        print(binary_array)
    else:
        print("The image is not binary (1-bit). Please provide a binary image.")
        sys.exit(1)

    # Define a simple structuring element (3x3 square)
    structuring_element = np.array([
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ])

    # Apply dilation
    dilated_image = dilation(original_array, structuring_element)

    # Debugging: Print the dilated image array
    print("Dilated binary array:")
    print(dilated_image)

    # Flatten the dilated image before saving
    flattened_pixels = dilated_image.flatten()  # Convert the 2D numpy array to a 1D array

    # Save the result
    save_image(flattened_pixels, '1', size, output_image_path)  # Save as binary (1-bit)
    print(f"Dilated image saved as '{output_image_path}'")


elif 'erosion' in args_dict:
    print("Performing erosion on the binary image...")

    original_array = np.array(im)
    print("Original image array:")
    print(original_array)

    # Ensure the image is binary (1-bit)
    if mode == '1':  # Check if the image is binary (1-bit)
        binary_array = np.array(im)  # This already has values of True (white) and False (black)
        print("Binary array:")
        print(binary_array)
    else:
        print("The image is not binary (1-bit). Please provide a binary image.")
        sys.exit(1)

    # Define a simple structuring element (3x3 square)
    structuring_element = np.array([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ])

    # Apply erosion
    eroded_image = erosion(original_array, structuring_element)

    # Debugging: Print the eroded image array
    print("Eroded binary array:")
    print(eroded_image)

    # Flatten the eroded image before saving
    flattened_pixels = eroded_image.flatten()  # Convert the 2D numpy array to a 1D array

    # Save the result
    save_image(flattened_pixels, '1', size, output_image_path)  # Save as binary (1-bit)
    print(f"Eroded image saved as '{output_image_path}'")

elif 'opening' in args_dict:
    print("Performing opening on the binary image...")

    original_array = np.array(im)
    print("Original image array:")
    print(original_array)

    # Ensure the image is binary (1-bit)
    if mode == '1':  # Check if the image is binary (1-bit)
        binary_array = np.array(im)  # This already has values of True (white) and False (black)
        print("Binary array:")
        print(binary_array)
    else:
        print("The image is not binary (1-bit). Please provide a binary image.")
        sys.exit(1)

    # Define a simple structuring element (3x3 square)
    structuring_element = np.array([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ])

    # Apply opening
    opened_image = opening(original_array, structuring_element)

    # Debugging: Print the opened image array
    print("Opened binary array:")
    print(opened_image)

    # Flatten the opened image before saving
    flattened_pixels = opened_image.flatten()  # Convert the 2D numpy array to a 1D array

    # Save the result
    save_image(flattened_pixels, '1', size, output_image_path)  # Save as binary (1-bit)
    print(f"Opened image saved as '{output_image_path}'")

elif 'closing' in args_dict:
    print("Performing closing on the binary image...")

    original_array = np.array(im)
    print("Original image array:")
    print(original_array)

    # Ensure the image is binary (1-bit)
    if mode == '1':  # Check if the image is binary (1-bit)
        binary_array = np.array(im)  # This already has values of True (white) and False (black)
        print("Binary array:")
        print(binary_array)
    else:
        print("The image is not binary (1-bit). Please provide a binary image.")
        sys.exit(1)

    # Define a simple structuring element (3x3 square)
    structuring_element = np.array([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ])

    # Apply closing
    closed_image = closing(original_array, structuring_element)

    # Debugging: Print the closed image array
    print("Closed binary array:")
    print(closed_image)

    # Flatten the closed image before saving
    flattened_pixels = closed_image.flatten()  # Convert the 2D numpy array to a 1D array

    # Save the result
    save_image(flattened_pixels, '1', size, output_image_path)  # Save as binary (1-bit)
    print(f"Closed image saved as '{output_image_path}'")

elif 'region_growing' in args_dict:
    print("Performing region growing segmentation...")

    # Convert the image to grayscale and get the pixels as a flat list
    gray_image = im.convert('L')
    pixels = list(gray_image.getdata())

    # Parse the seeds and threshold from arguments
    seeds = args_dict.get('seeds', '0,0').split(';')
    seeds = [tuple(map(int, seed.split(','))) for seed in seeds]
    threshold = int(args_dict.get('threshold', 10))
    connectivity = int(args_dict.get('connectivity', 4))

    # Perform region growing using the new function (which expects a 1D list)
    segmented_pixels = region_growing(pixels, size, seeds, threshold, connectivity)

    # Save the segmented result as an image
    save_image(segmented_pixels, 'L', size, output_image_path)  # Save as grayscale ('L')
    print(f"Segmented image saved as '{output_image_path}'")

    # Convert the segmented pixels back to a 2D numpy array for morphological operations
    original_array = np.array(segmented_pixels).reshape(size[1], size[0])

    # Define a simple structuring element (3x3 square)
    structuring_element = np.array([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ])

    # Apply closing
    closed_image = closing(original_array, structuring_element)

    # Flatten the closed image before saving
    flattened_pixels = closed_image.flatten()  # Convert the 2D numpy array to a 1D array

    # Save the result
    save_image(flattened_pixels, '1', size, output_image_path)  # Save as binary (1-bit)
    print(f"Closed image saved as '{output_image_path}'")

elif 'hit-or-miss' in args_dict:
    print("Performing hit-or-miss transform on the binary image...")

    original_array = np.array(im)
    print("Original image array:")
    print(original_array)

    # Ensure the image is binary (1-bit)
    if mode != '1':  # Check if the image is binary (1-bit)
        print("The image is not binary (1-bit). Please provide a binary image.")
        sys.exit(1)

    # Foreground-only structuring elements (xi)
    foreground_structuring_elements = [
        np.array([[1, -1, -1],
                  [1, 0, -1],
                  [1, -1, -1]]),

        np.array([[1, 1, 1],
                  [-1, 0, -1],
                  [-1, -1, -1]]),

        np.array([[-1, -1, 1],
                  [-1, 0, 1],
                  [-1, -1, 1]]),

        np.array([[-1, -1, -1],
                  [-1, 0, -1],
                  [1, 1, 1]]),
    ]

    # Foreground and Background structuring elements (xii)
    foreground_background_structuring_elements = [
        (
            np.array([[0, 0, 0],
                      [-1, 1, -1],
                      [1, 1, 1]]),  # Foreground

            np.array([[1, 1, 1],
                      [-1, 1, -1],
                      [0, 0, 0]])       # Background
        ),
        (
            np.array([[-1, 0, 0],
                      [1, 1, 0],
                      [1, 1, -1]]),  # Foreground

            np.array([[-1, 1, 1],
                      [0, 1, 1],
                      [0, 0, -1]])       # Background
        ),
        # Add more foreground-background pairs as needed
    ]

    # Initialize an empty result image
    final_hit_or_miss_result = np.zeros_like(original_array)

    # Apply (xi): Foreground-only kernels
    for foreground_kernel in foreground_structuring_elements:
        hit_or_miss_result = hitOrMiss(original_array, foreground_kernel)
        final_hit_or_miss_result = np.logical_or(final_hit_or_miss_result, hit_or_miss_result)

    # Apply (xii): Foreground and Background kernels
    for foreground_kernel, background_kernel in foreground_background_structuring_elements:
        hit_or_miss_result = hitOrMiss(original_array, foreground_kernel, background_kernel)
        final_hit_or_miss_result = np.logical_or(final_hit_or_miss_result, hit_or_miss_result)

    # Flatten the result before saving
    flattened_pixels = final_hit_or_miss_result.flatten()  # Convert the 2D numpy array to a 1D array

    # Save the result
    save_image(flattened_pixels, '1', size, output_image_path)  # Save as binary (1-bit)
    print(f"Hit-or-Miss image saved as '{output_image_path}'")

