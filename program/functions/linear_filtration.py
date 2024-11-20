import numpy as np

def universal_convolution(pixels, size, args_dict):
    """
    Perform universal convolution on the image using either a custom mask or predefined filters.
    
    Args:
        pixels: List of pixel values (grayscale or RGB).
        size: Tuple (width, height) of the image.
        args_dict: Dictionary of arguments, including 'custom_mask' or 'filter'.

    Returns:
        List of pixels after applying the convolution.
    """
    # Step 1: Generate the convolution mask
    if 'custom_mask' in args_dict:
        # Parse the custom mask, assuming it's provided as a comma-separated string
        try:
            mask_values = list(map(int, args_dict['custom_mask'].split(',')))
            if len(mask_values) != 9:
                raise ValueError("Custom mask must contain exactly 9 values.")
            mask = np.array(mask_values).reshape((3, 3))
        except ValueError as e:
            raise ValueError(f"Invalid custom mask format: {e}")
    else:
        # Use one of the standard filters (N, NE, E, SE)
        filter_type = args_dict.get('filter', 'N')  # Default to N filter if not specified
        filters = {
            "N": np.array([[ 1,  1,  1],
                           [-1, -2, -1],
                           [ 1,  1,  1]]),
            "NE": np.array([[ 1, -1, -1],
                            [-1, -2, -1],
                            [ 1,  1,  1]]),
            "E": np.array([[-1, -1, -1],
                           [ 1, -2,  1],
                           [ 1,  1,  1]]),
            "SE": np.array([[-1, -1, -1],
                            [ 1, -2,  1],
                            [ 1,  1,  1]])
        }
        mask = filters.get(filter_type)
        if mask is None:
            raise ValueError(f"Invalid filter type '{filter_type}' provided. Please choose from N, NE, E, SE, or provide a custom mask.")

    # Step 2: Determine the size of the mask
    mask_height, mask_width = len(mask), len(mask[0])
    
    # Step 3: Calculate padding
    pad_y = mask_height // 2
    pad_x = mask_width // 2
    
    # Step 4: Convert the pixels into a numpy array for easier manipulation
    if isinstance(pixels[0], tuple):  # RGB
        image_array = np.array(pixels).reshape((size[1], size[0], 3))
    else:  # Grayscale
        image_array = np.array(pixels).reshape((size[1], size[0]))
    
    # Step 5: Create an output array for the result
    output_array = np.zeros_like(image_array)
    
    # Step 6: Iterate over each pixel (excluding the border)
    for y in range(pad_y, size[1] - pad_y):
        for x in range(pad_x, size[0] - pad_x):
            # Extract the region of interest (ROI) around the current pixel
            region = image_array[y - pad_y : y + pad_y + 1, x - pad_x : x + pad_x + 1]
            
            # Perform element-wise multiplication and sum the result
            if isinstance(pixels[0], tuple):  # RGB
                for channel in range(3):
                    output_array[y, x, channel] = np.sum(region[:, :, channel] * mask)
            else:  # Grayscale
                output_array[y, x] = np.sum(region * mask)
    
    # Step 7: Convert back to list of pixels
    output_pixels = output_array.flatten()
    
    # Handle the case where the image is RGB
    if isinstance(pixels[0], tuple):
        output_pixels = [tuple(output_pixels[i:i+3]) for i in range(0, len(output_pixels), 3)]
    
    return output_pixels

import numpy as np

def optimized_convolution_fixed_filter(pixels, size):
    """Optimized convolution for a fixed detail extraction filter (N) using vectorized NumPy operations."""
    # Define the specific filter (hard-coded to "N")
    mask = np.array([[ 1,  1,  1],
                     [-1, -2, -1],
                     [ 1,  1,  1]])
    
    # Check if the image is RGB or Grayscale and reshape accordingly
    is_rgb = isinstance(pixels[0], tuple)
    if is_rgb:  # RGB
        image_array = np.array(pixels).reshape((size[1], size[0], 3))
    else:  # Grayscale
        image_array = np.array(pixels).reshape((size[1], size[0]))
    
    # Calculate padding size
    pad_y, pad_x = mask.shape[0] // 2, mask.shape[1] // 2
    
    # Pad the image to handle border pixels
    if is_rgb:
        padded_image = np.pad(image_array, ((pad_y, pad_y), (pad_x, pad_x), (0, 0)), mode='constant')
        output_array = np.zeros_like(image_array)
        # Perform convolution for each channel
        for channel in range(3):
            output_array[..., channel] = sum(
                padded_image[y:y + size[1], x:x + size[0], channel] * mask[y, x]
                for y in range(mask.shape[0])
                for x in range(mask.shape[1])
            )
    else:  # Grayscale
        padded_image = np.pad(image_array, ((pad_y, pad_y), (pad_x, pad_x)), mode='constant')
        output_array = sum(
            padded_image[y:y + size[1], x:x + size[0]] * mask[y, x]
            for y in range(mask.shape[0])
            for x in range(mask.shape[1])
        )
    
    # Flatten the output and convert back to a list of pixels
    if is_rgb:
        output_pixels = [tuple(pixel) for row in output_array for pixel in row]
    else:
        output_pixels = output_array.flatten().tolist()
    
    return output_pixels