from .noise_removal import alpha_trimmed_mean_filter


def mean_square_error(original_pixels, compared_pixels, width, height):
    """Calculate Mean Square Error (MSE) between the original image and another image."""
    sum_squared_error = 0.0  # Initialize sum of squared differences

    # Loop through each pixel by coordinates
    for y in range(height):
        for x in range(width):
            # Calculate the index for a 1D array representation
            idx = y * width + x

            # Access the pixels directly
            orig_pixel = original_pixels[idx]
            comp_pixel = compared_pixels[idx]

            # Calculate squared difference for each channel (RGB)
            if isinstance(orig_pixel, tuple):  # Color image
                difference = sum((o - c) ** 2 for o, c in zip(orig_pixel, comp_pixel))
            else:  # Grayscale image
                difference = (orig_pixel - comp_pixel) ** 2

            # Add the squared difference to the total sum
            sum_squared_error += difference

    # Calculate MSE
    mse = sum_squared_error / (width * height)  # Divide by total number of pixels

    return mse


def peak_mean_square_error(original_pixels, filtered_pixels, width, height):
    """Calculate Peak Mean Square Error (PMSE) between original and filtered image."""
    # Calculate MSE using the mean_square_error function
    mse_value = mean_square_error(original_pixels, filtered_pixels, width, height)

    # Calculate PMSE
    peak_value = 255.0  # Assuming 8-bit image depth (values from 0 to 255)
    pmse = (peak_value ** 2) / mse_value if mse_value != 0 else float('inf')  # Avoid division by zero

    return pmse


#
# def signal_to_noise_ratio(original, modified):
#     """Calculates the Signal to Noise Ratio."""
#     mse = mean_square_error(original, modified)
#
#     # Calculate signal power
#     signal_power = sum(sum(o_channel ** 2 for o_channel in o) for o in original) / (len(original) * 3)  # Average for R, G, B
#
#     if mse == 0:
#         return float('inf')  # SNR is infinite if there is no error
#     snr = 10 * (signal_power / mse) ** 0.5
#     return snr
#
# def peak_signal_to_noise_ratio(original, modified):
#     """Calculates the Peak Signal to Noise Ratio."""
#     mse = mean_square_error(original, modified)
#     if mse == 0:
#         return float('inf')  # PSNR is infinite if there is no error
#     psnr = 10 * (255 ** 2 / mse)
#     return psnr
#
def maximum_difference(original_pixels, filtered_pixels, width, height):
    """Calculate Maximum Difference (MD) between original and filtered image."""


    max_diff = 0.0  # Initialize maximum difference

    # Loop through each pixel by coordinates
    for y in range(height):
        for x in range(width):
            # Access the pixels directly
            orig_pixel = original_pixels[y][x]
            comp_pixel = filtered_pixels[y][x]

            # Calculate the absolute difference
            if isinstance(orig_pixel, tuple):  # Color image
                difference = max(abs(o - c) for o, c in zip(orig_pixel, comp_pixel))
            else:  # Grayscale image
                difference = abs(orig_pixel - comp_pixel)

            # Update the maximum difference
            if difference > max_diff:
                max_diff = difference

    return max_diff

