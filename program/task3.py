import sys
import numpy as np
from PIL import Image
from utils.file_operations import load_image, save_image
from utils.help import print_help
from utils.parse_arguments import parse_arguments
from functions.morphological import dilation, erosion, closing, \
    opening, hitOrMiss, iterative_dilation
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
        [0, 1, 0],
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
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
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
        binary_array = np.array(im)
        print("Binary array:")
        print(binary_array)
    else:
        print("The image is not binary (1-bit). Please provide a binary image.")
        sys.exit(1)

    # Define a simple structuring element (3x3 square)
    structuring_element = np.array([
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
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

    # Normalize the output labels to 0-255 for visualization
    max_label = max(segmented_pixels)
    if max_label > 0:
        segmented_pixels = [int((pixel / max_label) * 255) for pixel in segmented_pixels]
    else:
        print("Warning: No regions found. The result might be empty.")

    # Save the segmented result as an image
    save_image(segmented_pixels, 'L', size, output_image_path)  # Save as grayscale ('L')
    print(f"Segmented image saved as '{output_image_path}'")



elif 'hit-or-miss' in args_dict:
    print("Performing hit-or-miss transform on the binary image...")

    original_array = np.array(im)
    print("Original image array:")
    print(original_array)

    # Ensure the image is binary (1-bit)
    if mode != '1':  # Check if the image is binary (1-bit)
        print("The image is not binary (1-bit). Please provide a binary image.")
        sys.exit(1)

    # (xi)
    structuring_element1 = np.array([
            [1, -1, -1],
            [1, 0, -1],
            [1, -1, -1]])
    structuring_element2 = np.array(
                [[1, 1, 1],
                [-1, 0, -1],
                [-1, -1, -1]])

    structuring_element3 = np.array([
                [-1, -1, 1],
                [-1, 0, 1],
                [-1, -1, 1]])

    structuring_element4 = np.array([
                [-1, -1, -1],
                [-1, 0, -1],
                [1, 1, 1]]),
    # xii

    structuring_element5 = np.array([
                    [0, 0, 0],
                    [-1, 1, -1],
                    [1, 1, 1]])

    structuring_element6 = np.array([
                    [1, 1, 1],
                    [-1, 0, -1],
                    [0, 0, 0]])

    structuring_element7 = np.array([
                    [0, 0, 0],
                    [-1, 0, -1],
                    [1, 1, 1]])

    structuring_element8 = np.array([
                    [-1, 0, 0],
                    [1, 1, 0],
                    [1, 1, -1]])

    structuring_element9 = np.array([
                    [1, -1, 0],
                    [1, 1, 0],
                    [1, -1, 0]])

    structuring_element10 = np.array([
                    [0, -1, 1],
                    [0, 1, 1 ],
                    [0, -1, 1]])

    structuring_element11 = np.array([
                    [1, 1, -1],
                    [1, 1, 0],
                    [-1, 0, 0]])

    structuring_element12 = np.array([
                    [0, 0, -1],
                    [0, 1, 1],
                    [-1, 1, 1]])


    background_kernel1 = np.array([
                    [0, 0, -1],
                    [0, 1, 1],
                    [0, 1, 1]])

    kernel1 = np.array([
                    [0, 1, 1],
                    [0, 0, 1],
                    [0, 0, 1]])

    kernel2 = np.array([
                    [1, 0, 0],
                    [1, 1, 0],
                    [1, 1, 0]])
    # Call the hitOrMiss function
    final_hit_or_miss_result = hitOrMiss(original_array, kernel1, kernel2)

    print("Final Hit-or-Miss Result:")
    print(final_hit_or_miss_result)

    # Save the result
    save_image(
        final_hit_or_miss_result.flatten(),  # Convert 2D numpy array to 1D
        '1',  # Save as binary (1-bit)
        size,  # Image size
        output_image_path  # Output file path
    )
    print(f"Hit-or-Miss image saved as '{output_image_path}'")

elif 'm3' in args_dict:
    print("Performing iterative dilation on the binary image...")

    # Ensure the image is binary (1-bit)
    if mode != '1':  # Check if the image is binary (1-bit)
        print("The image is not binary (1-bit). Please provide a binary image.")
        sys.exit(1)

    # Convert the image to a numpy array
    original_array = np.array(im)
    print("Original image array:")
    print(original_array)

    # Parse the starting point p from the arguments (e.g., 'p=x,y')
    p_str = args_dict.get('p', '2,2')  # Default to (0, 0) if not provided
    p = tuple(map(int, p_str.split(',')))  # Convert the string to a tuple (x, y)

    print(f"Starting point p: {p}")

    # Define a simple structuring element (3x3 square)
    structuring_element = np.array([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ])

    # Perform iterative dilation starting from point p
    final_result = iterative_dilation(original_array, p, structuring_element)

    # Print the final result of iterative dilation
    print("Final iterative dilation result:")
    print(final_result)

    # Flatten the result before saving
    flattened_pixels = final_result.flatten()  # Convert the 2D numpy array to a 1D array

    # Save the result
    save_image(flattened_pixels, '1', size, output_image_path)  # Save as binary (1-bit)
    print(f"Iterative dilation image saved as '{output_image_path}'")