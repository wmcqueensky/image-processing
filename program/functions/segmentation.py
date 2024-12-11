def region_growing(pixels, size, seeds, threshold=10, connectivity=4):
    """
    Perform region growing on a grayscale image represented as a 1D array.
    
    Args:
        pixels (list): 1D list of pixel intensity values.
        size (tuple): (width, height) of the image.
        seeds (list of tuples): List of (x, y) coordinates for seed points.
        threshold (int): Intensity difference threshold for growing regions.
        connectivity (int): Connectivity type (4 or 8).
    
    Returns:
        list: 1D list representing labeled regions.
    """
    width, height = size
    visited = [False] * len(pixels)  # Track visited pixels
    labels = [0] * len(pixels)       # Initialize output labels
    region_id = 1                    # Start labeling regions from 1

    # Define connectivity offsets for 4 and 8 connectivity
    if connectivity == 4:
        offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    elif connectivity == 8:
        offsets = [
            (0, -1), (0, 1), (-1, 0), (1, 0),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
    else:
        raise ValueError("Invalid connectivity. Use 4 or 8.")

    # Helper function to convert (x, y) to 1D index
    def to_index(x, y):
        return y * width + x

    # Process each seed point
    for seed in seeds:
        x, y = seed
        index = to_index(x, y)

        # Skip if already visited
        if visited[index]:
            continue

        # Initialize region
        region_intensity = pixels[index]
        region_pixels = [index]  # Stack for region growing
        visited[index] = True

        while region_pixels:
            current_index = region_pixels.pop()
            labels[current_index] = region_id

            # Get current (x, y) coordinates
            current_y, current_x = divmod(current_index, width)

            # Check neighbors based on connectivity
            for dx, dy in offsets:
                nx, ny = current_x + dx, current_y + dy

                # Check if the neighbor is within bounds
                if 0 <= nx < width and 0 <= ny < height:
                    neighbor_index = to_index(nx, ny)

                    # Check if the neighbor is unvisited and within the threshold
                    if not visited[neighbor_index] and abs(pixels[neighbor_index] - region_intensity) <= threshold:
                        visited[neighbor_index] = True
                        region_pixels.append(neighbor_index)

        # Move to the next region label
        region_id += 1

    return labels
