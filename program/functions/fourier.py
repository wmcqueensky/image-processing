import numpy as np
from utils.file_operations import save_image


def slow_dft(signal):
    """Compute the Discrete Fourier Transform (DFT) using the direct definition."""
    N = len(signal)
    dft_result = np.zeros(N, dtype=complex)
    for k in range(N):
        for n in range(N):
            dft_result[k] += signal[n] * np.exp(-2j * np.pi * k * n / N)
    return dft_result

def slow_idft(frequency_signal):
    """Compute the Inverse Discrete Fourier Transform (IDFT) using the direct definition."""
    N = len(frequency_signal)
    idft_result = np.zeros(N, dtype=complex)
    for n in range(N):
        for k in range(N):
            idft_result[n] += frequency_signal[k] * np.exp(2j * np.pi * k * n / N)
    return idft_result / N

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

    Args:
        input_pixels: Flat list of pixel values from the image.
        size: Tuple (width, height) of the image.
        mode: Image mode ('L' for grayscale).
        output_base_path: Base path for saving output images (e.g., 'output').
        use_fast: Whether to use Fast Fourier Transform (FFT).
    """
    width, height = size
    if mode != 'L':
        raise ValueError("Fourier transform is implemented for grayscale ('L') images only.")

    # Reshape flat pixel list into a 2D array
    pixel_array = np.array(input_pixels, dtype=float).reshape(height, width)

    # Apply Fourier Transform (row and column-wise)
    if use_fast:
        transformed_rows = np.apply_along_axis(fast_fft, axis=1, arr=pixel_array)
        frequency_data = np.apply_along_axis(fast_fft, axis=0, arr=transformed_rows)
    else:
        transformed_rows = np.apply_along_axis(slow_dft, axis=1, arr=pixel_array)
        frequency_data = np.apply_along_axis(slow_dft, axis=0, arr=transformed_rows)

    # Save the magnitude spectrum for visualization
    magnitude_spectrum = np.log(1 + np.abs(frequency_data))
    magnitude_image = (magnitude_spectrum / magnitude_spectrum.max() * 255).astype(np.uint8)
    magnitude_output_path = f"{output_base_path}_fourier.bmp"
    save_image(magnitude_image.flatten(), 'L', size, magnitude_output_path)
    print(f"Magnitude spectrum saved to '{magnitude_output_path}'.")

    # Apply Inverse Fourier Transform (row and column-wise)
    if use_fast:
        inverse_rows = np.apply_along_axis(fast_ifft, axis=1, arr=frequency_data)
        inverse_transformed = np.apply_along_axis(fast_ifft, axis=0, arr=inverse_rows)
    else:
        inverse_rows = np.apply_along_axis(slow_idft, axis=1, arr=frequency_data)
        inverse_transformed = np.apply_along_axis(slow_idft, axis=0, arr=inverse_rows)

    # Normalize and convert back to uint8
    processed_pixels = np.real(inverse_transformed).clip(0, 255).astype(np.uint8).flatten()
    reconstructed_output_path = f"{output_base_path}_reconstructed.bmp"
    save_image(processed_pixels, mode, size, reconstructed_output_path)
    print(f"Reconstructed image saved to '{reconstructed_output_path}'.")
