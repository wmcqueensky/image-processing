def mean_square_error(original_pixels, filtered_pixels):
    """Calculate Mean Square Error (MSE) between original and filtered images."""
    n = len(original_pixels)
    mse = sum(
        (o - f) ** 2 if isinstance(o, int) else sum((oc - fc) ** 2 for oc, fc in zip(o, f)) / 3
        for o, f in zip(original_pixels, filtered_pixels)
    ) / n
    return mse

def peak_mean_square_error(original_pixels, filtered_pixels):
    """Calculate Peak Mean Square Error (PMSE) between original and filtered image."""
    max_pixel_value = 255
    n = len(original_pixels)
    pmse = sum(
        sum((o_channel - f_channel) ** 2 for o_channel, f_channel in zip(o, f))  # Sum across channels
        for o, f in zip(original_pixels, filtered_pixels)
    ) / (n * max_pixel_value ** 2 * 3)  # Divide by 3 for R, G, B channels
    return pmse

def signal_to_noise_ratio(original, modified):
    """Calculates the Signal to Noise Ratio."""
    mse = mean_square_error(original, modified)
    
    # Calculate signal power
    signal_power = sum(sum(o_channel ** 2 for o_channel in o) for o in original) / (len(original) * 3)  # Average for R, G, B
    
    if mse == 0:
        return float('inf')  # SNR is infinite if there is no error
    snr = 10 * (signal_power / mse) ** 0.5
    return snr

def peak_signal_to_noise_ratio(original, modified):
    """Calculates the Peak Signal to Noise Ratio."""
    mse = mean_square_error(original, modified)
    if mse == 0:
        return float('inf')  # PSNR is infinite if there is no error
    psnr = 10 * (255 ** 2 / mse)
    return psnr

def maximum_difference(original, modified):
    """Calculates the Maximum Difference between two images."""
    max_diff = max(
        max(abs(o_channel - m_channel) for o_channel, m_channel in zip(o, m))  # Compute max difference per pixel
        for o, m in zip(original, modified)  # Loop through each pixel
    )
    return max_diff

