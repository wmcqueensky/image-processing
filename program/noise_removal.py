import math
#N7
def alpha_trimmed_mean_filter(pixels, width, height, kernel_size, alpha):
    """Apply alpha-trimmed mean filter to the image."""
    print(f"Applying Alpha-trimmed Mean Filter with alpha={alpha} and kernel size={kernel_size}")
    new_pixels = []
    k = kernel_size // 2  # kernel radius
    total_trim = 2 * alpha  # trim from both ends

    for y in range(height):
        for x in range(width):
            # Extract the neighborhood
            neighborhood = []
            for ky in range(-k, k + 1):
                for kx in range(-k, k + 1):
                    ny = min(max(y + ky, 0), height - 1)
                    nx = min(max(x + kx, 0), width - 1)
                    neighborhood.append(pixels[ny * width + nx])

            # Sort and trim the extremes
            neighborhood.sort()
            trimmed_neighborhood = neighborhood[alpha: len(neighborhood) - alpha]

            # Compute the mean of the remaining values
            if isinstance(trimmed_neighborhood[0], int):  # Grayscale image
                avg_value = sum(trimmed_neighborhood) // len(trimmed_neighborhood)
                new_pixels.append(avg_value)
            else:  # RGB image
                avg_pixel = tuple(
                    sum(channel_values) // len(trimmed_neighborhood) for channel_values in zip(*trimmed_neighborhood))
                new_pixels.append(avg_pixel)

    return new_pixels


def geometric_mean_filter(pixels, width, height, kernel_size):
    """Apply geometric mean filter to the image."""
    print(f"Applying Geometric Mean Filter with kernel size={kernel_size}")
    new_pixels = []
    k = kernel_size // 2  # kernel radius

    for y in range(height):
        for x in range(width):
            # Extract the neighborhood
            neighborhood = []
            for ky in range(-k, k + 1):
                for kx in range(-k, k + 1):
                    ny = min(max(y + ky, 0), height - 1)
                    nx = min(max(x + kx, 0), width - 1)
                    neighborhood.append(pixels[ny * width + nx])

            # Compute the geometric mean
            if isinstance(neighborhood[0], int):  # Grayscale image
                product = math.prod(neighborhood)
                gmean_value = int(math.pow(product, 1 / len(neighborhood)))
                new_pixels.append(gmean_value)
            else:  # RGB image
                gmean_pixel = tuple(
                    int(math.pow(math.prod(channel_values), 1 / len(neighborhood)))
                    for channel_values in zip(*neighborhood)
                )
                new_pixels.append(gmean_pixel)

    return new_pixels