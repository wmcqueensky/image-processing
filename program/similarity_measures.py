def mean_square_error(original, modified):
    """Calculates the Mean Square Error between two images."""
    error_sum = sum((o - m) ** 2 for o, m in zip(original, modified))
    mse = error_sum / len(original)
    return mse

# def peak_mean_square_error(original, modified):
#     """Calculates the Peak Mean Square Error between two images."""
#     mse = mean_square_error(original, modified)
#     pmse = mse / (255 ** 2)  # Assuming pixel values are in the range [0, 255]
#     return pmse

def signal_to_noise_ratio(original, modified):
    """Calculates the Signal to Noise Ratio."""
    mse = mean_square_error(original, modified)
    signal_power = sum(o ** 2 for o in original) / len(original)
    if mse == 0:
        return float('inf')  # SNR is infinite if there is no error
    snr = 10 * (signal_power / mse) ** 0.5
    return snr

# def peak_signal_to_noise_ratio(original, modified):
#     """Calculates the Peak Signal to Noise Ratio."""
#     mse = mean_square_error(original, modified)
#     if mse == 0:
#         return float('inf')  # PSNR is infinite if there is no error
#     psnr = 10 * (255 ** 2 / mse)
#     return psnr

# def maximum_difference(original, modified):
#     """Calculates the Maximum Difference between two images."""
#     max_diff = max(abs(o - m) for o, m in zip(original, modified))
#     return max_diff
