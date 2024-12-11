import numpy as np

def dilation(image, kernel):
    """
    Perform the dilation operation on a binary image.
    """
    # Get dimensions of image and kernel
    image_h, image_w = image.shape
    kernel_h, kernel_w = kernel.shape

    # Calculate padding
    pad_h = kernel_h // 2
    pad_w = kernel_w // 2

    # Pad the input image
    padded_image = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)

    # Prepare the output image
    output_image = np.zeros_like(image)

    # Perform dilation
    for i in range(image_h):
        for j in range(image_w):
            # Extract the region of interest
            region = padded_image[i:i + kernel_h, j:j + kernel_w]
            # Apply the kernel
            if np.any(region & kernel):  # Checks for overlap with foreground
                output_image[i, j] = 1  # Set pixel to white (1)

    return output_image


def erosion(image, kernel):
    """
    Perform the erosion operation on a binary image.
    """
    # Get dimensions of image and kernel
    image_h, image_w = image.shape
    kernel_h, kernel_w = kernel.shape

    # Calculate padding
    pad_h = kernel_h // 2
    pad_w = kernel_w // 2

    # Pad the input image CHECK HERE IF TUPLES ARE NEEDED
    padded_image = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=1)  # pad with 0s (black)

    # Prepare the output image
    output_image = np.ones_like(image)  # Start with all pixels as 1 (white)

    # Perform erosion
    for i in range(image_h):
        for j in range(image_w):
            # Extract the region of interest
            region = padded_image[i:i + kernel_h, j:j + kernel_w]
            # Apply the kernel: check if all elements in the region match the kernel (foreground overlap)
            if np.all(region & kernel):  # Checks if all overlap with foreground (1)
                output_image[i, j] = 1  # Keep pixel as white
            else:
                output_image[i, j] = 0  # Set pixel to black if not fully matched

    return output_image

def opening(image, kernel):
    """
    Perform the opening operation (erosion followed by dilation).
    """
    # First, apply erosion
    eroded_image = erosion(image, kernel)

    # Then, apply dilation to the result of erosion
    opened_image = dilation(eroded_image, kernel)

    return opened_image


def closing(image, kernel):
    """
    Perform the closing operation (dilation followed by erosion).
    """
    # First, apply dilation
    dilated_image = dilation(image, kernel)

    # Then, apply erosion to the result of dilation
    closed_image = erosion(dilated_image, kernel)

    return closed_image


def hitOrMiss(image, foreground_kernel, background_kernel=None):
    """
    Perform the hit-or-miss transform on a binary image.
    """

    # Erode the image with the foreground kernel (this matches foreground pixels)
    eroded_foreground = erosion(image, foreground_kernel)
    print("Eroded Foreground")
    print(eroded_foreground)

    if background_kernel is not None:
        # Invert the image for the background kernel (background becomes foreground)
        print("Original image")
        print(image)
        inverted_image = np.logical_not(image)
        print("inverted image:")
        print(inverted_image)
        # Erode the inverted image with the background kernel (this matches background pixels)
        eroded_background = erosion(inverted_image, background_kernel)
        print("Eroded Background")
        print(eroded_background)
        # Combine the results using logical AND
        result = np.logical_and(eroded_foreground, eroded_background)
        print("Result:")
        print(result)
    else:
        # If no background kernel is provided, use only the foreground erosion
        result = eroded_foreground

    return result.astype(np.uint8)  # Return as uint8 (binary)
