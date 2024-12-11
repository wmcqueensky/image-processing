import numpy as np

def region_growing(pixels, size, seeds, threshold=10, connectivity=4, criterion='intensity'):
    """
    Perform region growing on a grayscale image represented as a 1D array.
    
    Args:
        pixels (list): 1D list of pixel intensity values.
        size (tuple): (width, height) of the image.
        seeds (list of tuples): List of (x, y) coordinates for seed points.
        threshold (int): Threshold for homogeneity criterion.
        connectivity (int): Connectivity type (4 or 8).
        criterion (str): Type of homogeneity criterion ('intensity', 'relative', 'texture').

    Returns:
        list: 1D list representing labeled regions.
    """
    # Get the width and height of the image
    width, height = size
    
    # Initialize a list to track which pixels have been visited
    visited = [False] * len(pixels)
    
    # Initialize the output labels (0 means no label assigned yet)
    labels = [0] * len(pixels)
    
    # Start labeling regions from 1
    region_id = 1

    # Define offsets for 4-connectivity (left, right, up, down)
    if connectivity == 4:
        offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    
    # Define offsets for 8-connectivity (includes diagonals)
    elif connectivity == 8:
        offsets = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    # Raise an error if an invalid connectivity is provided
    else:
        raise ValueError("Invalid connectivity. Use 4 or 8.")

    # Helper function to convert 2D (x, y) coordinates to a 1D index
    def to_index(x, y):
        return y * width + x

    # Function to calculate the local standard deviation around a pixel
    def calculate_local_std(pixels, x, y, width, height, window_size=3):
        half_window = window_size // 2
        neighbors = []

        # Iterate over the neighborhood defined by window_size
        for dx in range(-half_window, half_window + 1):
            for dy in range(-half_window, half_window + 1):
                nx, ny = x + dx, y + dy
                
                # Check if the neighbor is within image bounds
                if 0 <= nx < width and 0 <= ny < height:
                    neighbors.append(pixels[to_index(nx, ny)])

        # Calculate and return the standard deviation of the neighborhood
        return np.std(neighbors)

    # Process each seed point
    for seed in seeds:
        # Extract the (x, y) coordinates of the seed point
        x, y = seed
        
        # Convert the (x, y) coordinates to a 1D index
        index = to_index(x, y)

        # Skip this seed if it has already been visited
        if visited[index]:
            continue

        # Initialize the region's intensity with the seed's intensity
        region_intensity = pixels[index]
        
        # Create a stack to store the pixels to process for this region
        region_pixels = [index]
        
        # Mark the seed pixel as visited
        visited[index] = True

        # Process all the pixels in the current region
        while region_pixels:
            # Get the current pixel index from the stack
            current_index = region_pixels.pop()
            
            # Assign the current region ID to the pixel
            labels[current_index] = region_id
            
            # Get the current pixel's (y, x) coordinates
            current_y, current_x = divmod(current_index, width)

            # Check all neighboring pixels based on the chosen connectivity
            for dx, dy in offsets:
                nx, ny = current_x + dx, current_y + dy

                # Check if the neighbor is within image bounds
                if 0 <= nx < width and 0 <= ny < height:
                    neighbor_index = to_index(nx, ny)

                    # Process the neighbor if it hasn't been visited
                    if not visited[neighbor_index]:
                        # Homogeneity criterion: 'intensity' (default)
                        if criterion == 'intensity':
                            if abs(pixels[neighbor_index] - region_intensity) <= threshold:
                                visited[neighbor_index] = True
                                region_pixels.append(neighbor_index)
                        
                        # Homogeneity criterion: 'relative' (relative difference)
                        elif criterion == 'relative':
                            if abs(pixels[neighbor_index] - region_intensity) / max(region_intensity, 1) <= threshold:
                                visited[neighbor_index] = True
                                region_pixels.append(neighbor_index)
                        
                        # Homogeneity criterion: 'texture' (standard deviation comparison)
                        elif criterion == 'texture':
                            local_std = calculate_local_std(pixels, nx, ny, width, height)
                            region_std = calculate_local_std(pixels, x, y, width, height)
                            if abs(local_std - region_std) <= threshold:
                                visited[neighbor_index] = True
                                region_pixels.append(neighbor_index)

        # Move to the next region label
        region_id += 1

    # Return the labeled regions as a 1D list
    return labels
