import numpy as np

def universal_convolution(pixels, size, mask):
    """Perform convolution on the image with a given mask."""
    # Determine the size of the mask
    mask_height, mask_width = len(mask), len(mask[0])
    
    # Calculate padding
    pad_y = mask_height // 2
    pad_x = mask_width // 2
    
    # Convert the pixels into a numpy array for easier manipulation
    if isinstance(pixels[0], tuple):  # RGB
        image_array = np.array(pixels).reshape((size[1], size[0], 3))
    else:  # Grayscale
        image_array = np.array(pixels).reshape((size[1], size[0]))
    
    # Create an output array for the result
    output_array = np.zeros_like(image_array)
    
    # Iterate over each pixel (excluding the border)
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
    
    # Convert back to list of pixels
    output_pixels = output_array.flatten()
    
    # Handle the case where the image is RGB
    if isinstance(pixels[0], tuple):
        output_pixels = [tuple(output_pixels[i:i+3]) for i in range(0, len(output_pixels), 3)]
    
    return output_pixels

def optimized_convolution_detail_extraction(pixels, size, filter_type):
    """Optimized convolution for detail extraction filters (N, NE, E, SE)."""
    # Define the specific filters (N, NE, E, SE)
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
    
    # Get the corresponding filter
    mask = filters[filter_type]
    
    # Convert the pixels into a numpy array for easier manipulation
    if isinstance(pixels[0], tuple):  # RGB
        image_array = np.array(pixels).reshape((size[1], size[0], 3))
    else:  # Grayscale
        image_array = np.array(pixels).reshape((size[1], size[0]))
    
    # Calculate padding
    pad_y = mask.shape[0] // 2
    pad_x = mask.shape[1] // 2
    
    # Create an output array for the result
    output_array = np.zeros_like(image_array)
    
    # Iterate over each pixel (excluding the border)
    for y in range(pad_y, size[1] - pad_y):
        for x in range(pad_x, size[0] - pad_x):
            # Extract the region of interest (ROI) around the current pixel
            region = image_array[y - pad_y : y + pad_y + 1, x - pad_x : x + pad_x + 1]
            
            # Perform the convolution operation only for the masked elements
            if isinstance(pixels[0], tuple):  # RGB
                for channel in range(3):
                    output_array[y, x, channel] = np.sum(region[:, :, channel] * mask)
            else:  # Grayscale
                output_array[y, x] = np.sum(region * mask)
    
    # Convert back to list of pixels
    output_pixels = output_array.flatten()
    
    # Handle the case where the image is RGB
    if isinstance(pixels[0], tuple):
        output_pixels = [tuple(output_pixels[i:i+3]) for i in range(0, len(output_pixels), 3)]
    
    return output_pixels
