import sys
import numpy as np
from PIL import Image
from utils.file_operations import load_image, save_image
from utils.help import print_help
from utils.parse_arguments import parse_arguments
from functions.morphological import dilation, erosion, closing, \
    opening  # Import the dilate function from morphological.py

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