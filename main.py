import sys
from PIL import Image
import numpy as np

# ==============================
# FUNCTION DEFINITIONS
# ==============================

def load_image(image_path):
    """Loads an image and converts it to a numpy array."""
    try:
        im = Image.open(image_path)
        arr = np.array(im)
        return arr, im.mode, im.size
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' does not exist.")
        sys.exit()

def save_image(image_array, mode, size, output_path):
    """Converts numpy array back to image and saves it."""
    new_image = Image.fromarray(image_array.astype(np.uint8), mode)
    new_image.save(output_path)
    print(f"Image saved to {output_path}")

def adjust_brightness(arr, factor):
    """Manual implementation of brightness adjustment."""
    print(f"Adjusting brightness by a factor of {factor}")
    arr = arr.astype(np.int32)  # To avoid overflow/underflow during processing
    arr += int(factor)  # Adjust brightness
    arr = np.clip(arr, 0, 255)  # Ensure values stay in [0, 255]
    return arr

def adjust_contrast(arr, factor):
    """Manual implementation of contrast adjustment."""
    print(f"Adjusting contrast by a factor of {factor}")
    arr = arr.astype(np.int32)
    mean_value = np.mean(arr, axis=(0, 1))  # Compute the mean pixel value
    arr = (arr - mean_value) * float(factor) + mean_value
    arr = np.clip(arr, 0, 255)
    return arr

def apply_negative(arr):
    """Manual implementation of the negative filter."""
    print(f"Applying negative filter")
    arr = 255 - arr  # Invert the pixel values
    return arr

# ==============================
# MAIN SCRIPT
# ==============================

if len(sys.argv) < 4:
    print("Usage: python3 image_processor.py <image> <output_image> --command [argument=value]")
    sys.exit()

# Input arguments
input_image_path = sys.argv[1]
output_image_path = sys.argv[2]
command = sys.argv[3]

# Load the image as a numpy array
image_data, mode, size = load_image(input_image_path)

# Apply the command based on input
if command == '--brightness':
    if len(sys.argv) < 5:
        print("Error: Missing brightness factor argument")
        sys.exit()
    brightness_factor = int(sys.argv[4].split('=')[1])
    image_data = adjust_brightness(image_data, brightness_factor)

elif command == '--contrast':
    if len(sys.argv) < 5:
        print("Error: Missing contrast factor argument")
        sys.exit()
    contrast_factor = float(sys.argv[4].split('=')[1])
    image_data = adjust_contrast(image_data, contrast_factor)

elif command == '--negative':
    image_data = apply_negative(image_data)

else:
    print(f"Unknown command: {command}")
    sys.exit()

# Save the modified image
save_image(image_data, mode, size, output_image_path)
