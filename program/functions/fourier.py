import numpy as np
from utils.file_operations import save_image

def slow_dft(signal):
    """Compute the Discrete Fourier Transform (DFT) using the direct definition."""
    N = len(signal)
    n = np.arange(N)
    k = n[:, None]  # Create a column vector for k
    exponential = np.exp(-2j * np.pi * k * n / N)  # Precompute the exponential terms
    return np.dot(exponential, signal)  # Use matrix multiplication to compute DFT

def slow_idft(frequency_signal):
    """Compute the Inverse Discrete Fourier Transform (IDFT) using the direct definition."""
    N = len(frequency_signal)
    n = np.arange(N)
    k = n[:, None]  # Create a column vector for k
    exponential = np.exp(2j * np.pi * k * n / N)  # Precompute the exponential terms
    return np.dot(exponential, frequency_signal) / N  # Use matrix multiplication to compute IDFT

def fast_fft(signal):
    """Compute the Fast Fourier Transform (FFT) using decimation in time."""
    N = len(signal)
    if N <= 1:
        return signal
    if N % 2 != 0:
        raise ValueError("Signal length must be a power of 2 for FFT.")
    even = fast_fft(signal[::2])
    odd = fast_fft(signal[1::2])
    factor = np.exp(-2j * np.pi * np.arange(N) / N)
    return np.concatenate([even + factor[:N // 2] * odd, even - factor[:N // 2] * odd])

def fast_ifft(frequency_signal):
    """Compute the Inverse Fast Fourier Transform (IFFT) using decimation in time."""
    N = len(frequency_signal)
    if N <= 1:
        return frequency_signal
    if N % 2 != 0:
        raise ValueError("Signal length must be a power of 2 for IFFT.")
    even = fast_ifft(frequency_signal[::2])
    odd = fast_ifft(frequency_signal[1::2])
    factor = np.exp(2j * np.pi * np.arange(N) / N)
    return np.concatenate([even + factor[:N // 2] * odd, even - factor[:N // 2] * odd]) / 2

def process_and_save_fourier(input_pixels, size, mode, output_base_path, use_fast=True):
    """
    Apply Fourier Transform to an image, save magnitude spectrum,
    apply Inverse Fourier Transform, and save the reconstructed image.
    Supports both grayscale and color images.
    
    Args:
        input_pixels: Flat list of pixel values from the image.
        size: Tuple (width, height) of the image.
        mode: Image mode ('L' for grayscale, 'RGB' for color).
        output_base_path: Base path for saving output images (e.g., 'output').
        use_fast: Whether to use Fast Fourier Transform (FFT).
    """
    width, height = size
    if mode == 'L':
        # For grayscale images, treat as a 2D array of intensities
        pixel_array = np.array(input_pixels, dtype=float).reshape(height, width)
        channels = [pixel_array]
    elif mode == 'RGB':
        # For color images, split into R, G, B channels
        pixel_array = np.array(input_pixels, dtype=float).reshape(height, width, 3)
        channels = [pixel_array[:, :, i] for i in range(3)]
    else:
        raise ValueError("Fourier transform is implemented for grayscale ('L') or color ('RGB') images only.")

    # Apply Fourier Transform to each channel
    if use_fast:
        print("Applying Fast Fourier...")
        transformed_channels = [np.apply_along_axis(fast_fft, axis=1, arr=channel) for channel in channels]
        frequency_data = [np.apply_along_axis(fast_fft, axis=0, arr=transformed_channel) for transformed_channel in transformed_channels]
    else:
        print("Applying Slow Fourier...")
        transformed_channels = [np.apply_along_axis(slow_dft, axis=1, arr=channel) for channel in channels]
        frequency_data = [np.apply_along_axis(slow_dft, axis=0, arr=transformed_channel) for transformed_channel in transformed_channels]

    # Centering the zero-frequency component
    frequency_data_shifted = [np.fft.fftshift(frequency) for frequency in frequency_data]

    # Save the magnitude spectrum for visualization (separate for each channel)
    if mode == 'RGB':
        # Compute magnitude for each channel (R, G, B)
        magnitude_spectrum_r = np.log(1 + np.abs(frequency_data_shifted[0]))  # Red channel
        magnitude_spectrum_g = np.log(1 + np.abs(frequency_data_shifted[1]))  # Green channel
        magnitude_spectrum_b = np.log(1 + np.abs(frequency_data_shifted[2]))  # Blue channel
        
        # Normalize and convert each channel to uint8
        magnitude_r = (magnitude_spectrum_r / magnitude_spectrum_r.max() * 255).astype(np.uint8)
        magnitude_g = (magnitude_spectrum_g / magnitude_spectrum_g.max() * 255).astype(np.uint8)
        magnitude_b = (magnitude_spectrum_b / magnitude_spectrum_b.max() * 255).astype(np.uint8)
        
        # Stack the magnitude spectra of R, G, B channels into a single image
        magnitude_image = np.stack([magnitude_r, magnitude_g, magnitude_b], axis=-1)

        # Convert the magnitude image to a list of tuples for RGB format
        magnitude_image = [tuple(pixel) for pixel in magnitude_image.reshape(-1, 3)]

        magnitude_output_path = f"{output_base_path}_fourier_rgb.bmp"
        save_image(magnitude_image, 'RGB', size, magnitude_output_path)
        print(f"Magnitude spectrum for RGB saved to '{magnitude_output_path}'.")

    else:
        # For grayscale, just use the first channel (since there's only one channel in grayscale images)
        magnitude_spectrum = np.log(1 + np.abs(frequency_data_shifted[0]))  # Using the first channel for visualization
        magnitude_image = (magnitude_spectrum / magnitude_spectrum.max() * 255).astype(np.uint8)

        # Flatten the magnitude image for grayscale and save it
        magnitude_image = magnitude_image.flatten()

        magnitude_output_path = f"{output_base_path}_fourier.bmp"
        save_image(magnitude_image, 'L', size, magnitude_output_path)
        print(f"Magnitude spectrum saved to '{magnitude_output_path}'.")

    # Apply Inverse Fourier Transform to each channel
    if use_fast:
        inverse_channels = [np.apply_along_axis(fast_ifft, axis=1, arr=frequency_channel) for frequency_channel in frequency_data]
        inverse_transformed = [np.apply_along_axis(fast_ifft, axis=0, arr=inverse_channel) for inverse_channel in inverse_channels]
    else:
        inverse_channels = [np.apply_along_axis(slow_idft, axis=1, arr=frequency_channel) for frequency_channel in frequency_data]
        inverse_transformed = [np.apply_along_axis(slow_idft, axis=0, arr=inverse_channel) for inverse_channel in inverse_channels]

    # Normalize and convert back to uint8 for each channel
    reconstructed_channels = [np.real(channel).clip(0, 255).astype(np.uint8) for channel in inverse_transformed]

    # Combine the reconstructed channels back into an RGB image (for color images)
    if mode == 'RGB':
        # Stack the RGB channels back together and reshape into a 1D list of tuples
        reconstructed_pixels = np.stack(reconstructed_channels, axis=-1).reshape(-1, 3)
        reconstructed_pixels = [tuple(pixel) for pixel in reconstructed_pixels]  # Convert to tuple format
    else:
        reconstructed_pixels = reconstructed_channels[0].flatten()

    reconstructed_output_path = f"{output_base_path}_reconstructed.bmp"
    save_image(reconstructed_pixels, mode, size, reconstructed_output_path)
    print(f"Reconstructed image saved to '{reconstructed_output_path}'.")

    
    
    # Unoptimised slow FT!!!
# def slow_dft(signal):
#     """Compute the Discrete Fourier Transform (DFT) using the direct definition."""
#     N = len(signal)
#     dft_result = np.zeros(N, dtype=complex)
#     for k in range(N):
#         for n in range(N):
#             dft_result[k] += signal[n] * np.exp(-2j * np.pi * k * n / N)
#     return dft_result

# def slow_idft(frequency_signal):
#     """Compute the Inverse Discrete Fourier Transform (IDFT) using the direct definition."""
#     N = len(frequency_signal)
#     idft_result = np.zeros(N, dtype=complex)
#     for n in range(N):
#         for k in range(N):
#             idft_result[n] += frequency_signal[k] * np.exp(2j * np.pi * k * n / N)
#     return idft_result / N

