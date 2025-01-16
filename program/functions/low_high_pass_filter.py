import sys
from pprint import pprint

import numpy as np
from PIL import Image
from numpy import convolve
from utils.file_operations import save_image
from functions.fourier import save_magnitude_spectrum, fast_fft
from functions.fourier import save_magnitude_spectrum, fast_fft, fast_ifft


def apply_low_pass_filter(frequency_data, cutoff_frequency):
    """
    Apply a low-pass filter to the frequency data.
    Zeroes out high frequencies above the cutoff frequency.

    Args:
        frequency_data: List of frequency domain data for each channel.
        cutoff_frequency: The cut-off frequency for the low-pass filter.

    Returns:
        Filtered frequency data.
    """
    filtered_frequency_data = []

    for frequency in frequency_data:
        # Get the dimensions of the frequency data
        height, width = frequency.shape

        # Create a frequency grid manually
        u = np.arange(width)
        v = np.arange(height)
        u[u > width // 2] -= width
        v[v > height // 2] -= height
        U, V = np.meshgrid(u, v)

        # Calculate the distance from the center of the frequency grid
        distance = np.sqrt(U**2 + V**2)

        # Apply the low-pass filter
        mask = distance <= cutoff_frequency
        filtered_frequency = frequency * mask  # Apply mask directly to frequency data

        filtered_frequency_data.append(filtered_frequency)

    return filtered_frequency_data

def apply_high_pass_filter(frequency_data, cutoff_frequency):
    """
    Apply a high-pass filter to the frequency data.
    Zeroes out low frequencies below the cutoff frequency.

    Args:
        frequency_data: List of frequency domain data for each channel.
        cutoff_frequency: The cut-off frequency for the high-pass filter.

    Returns:
        Filtered frequency data.
    """
    filtered_frequency_data = []

    for frequency in frequency_data:
        # Get the dimensions of the frequency data
        height, width = frequency.shape

        # Create a frequency grid manually
        u = np.arange(width)
        v = np.arange(height)
        u[u > width // 2] -= width
        v[v > height // 2] -= height
        U, V = np.meshgrid(u, v)

        # Calculate the distance from the center of the frequency grid
        distance = np.sqrt(U**2 + V**2)

        # Apply the high-pass filter
        mask = distance >= cutoff_frequency
        filtered_frequency = frequency * mask  # Apply mask directly to frequency data

        filtered_frequency_data.append(filtered_frequency)

    return filtered_frequency_data

def process_and_save_filtered(frequency_data, size, mode, output_base_path, filter_type):
    """
    Apply inverse Fourier transform to filtered frequency data using custom FFT functions
    and save the reconstructed image.

    Args:
        frequency_data: Filtered frequency domain data for each channel.
        size: Tuple (width, height) of the image.
        mode: Image mode ('L' for grayscale, 'RGB' for color).
        output_base_path: Base path for saving output images.
        filter_type: Type of filter applied ('lowpass' or 'highpass').
    """
    # Save the magnitude spectrum of the filtered frequency data
    save_magnitude_spectrum(frequency_data, size, mode, output_base_path)

    # The frequency_data is already in frequency domain and filtered
    # Just need to apply IFFT once for each dimension
    inverse_transformed = []
    for channel in frequency_data:
        # Apply IFFT to rows first
        rows_ifft = np.array([fast_ifft(row) for row in channel])
        # Then apply IFFT to columns
        full_ifft = np.array([fast_ifft(col) for col in rows_ifft.T]).T
        inverse_transformed.append(full_ifft)

    # Normalize and convert back to uint8 for each channel
    reconstructed_channels = [
        np.real(channel).clip(0, 255).astype(np.uint8)
        for channel in inverse_transformed
    ]

    # Combine the reconstructed channels back into an RGB image (for color images)
    if mode == 'RGB':
        # Stack the RGB channels back together and reshape into a 1D list of tuples
        reconstructed_pixels = np.stack(reconstructed_channels, axis=-1).reshape(-1, 3)
        reconstructed_pixels = [tuple(pixel) for pixel in reconstructed_pixels]
    else:
        reconstructed_pixels = reconstructed_channels[0].flatten()

    reconstructed_output_path = f"{output_base_path}_{filter_type}.bmp"
    save_image(reconstructed_pixels, mode, size, reconstructed_output_path)
    print(f"Reconstructed {filter_type} image saved to '{reconstructed_output_path}'.")





#F3-F6

def apply_band_pass_filter(frequency_data, f_low, f_high):
    """
    Apply a band-pass filter to the frequency data.
    Allows frequencies between f_low and f_high.

    Args:
        frequency_data: List of frequency domain data for each channel.
        f_low: Lower cut-off frequency.
        f_high: Upper cut-off frequency.

    Returns:
        Filtered frequency data.
    """
    filtered_frequency_data = []

    for frequency in frequency_data:
        # Get the dimensions of the frequency data
        height, width = frequency.shape

        # Create a frequency grid manually
        u = np.arange(width)
        v = np.arange(height)
        u[u > width // 2] -= width
        v[v > height // 2] -= height
        U, V = np.meshgrid(u, v)

        # Calculate the distance from the center of the frequency grid
        distance = np.sqrt(U**2 + V**2)

        # Apply the band-pass filter
        mask = (distance >= f_low) & (distance <= f_high)
        filtered_frequency = frequency * mask  # Apply mask directly to frequency data

        filtered_frequency_data.append(filtered_frequency)

    return filtered_frequency_data

def apply_band_cut_filter(frequency_data, f_low, f_high):
    """
    Apply a band-cut (notch) filter to the frequency data.
    Suppresses frequencies between f_low and f_high.

    Args:
        frequency_data: List of frequency domain data for each channel.
        f_low: Lower frequency cutoff.
        f_high: Higher frequency cutoff.

    Returns:
        Filtered frequency data.
    """
    filtered_frequency_data = []

    for frequency in frequency_data:
        # Get the dimensions of the frequency data
        height, width = frequency.shape

        # Create a frequency grid manually
        u = np.arange(width)
        v = np.arange(height)
        u[u > width // 2] -= width
        v[v > height // 2] -= height
        U, V = np.meshgrid(u, v)

        # Calculate the distance from the center of the frequency grid
        distance = np.sqrt(U**2 + V**2)

        # Apply the band-cut filter
        mask = (distance < f_low) | (distance > f_high)
        filtered_frequency = frequency * mask  # Apply mask directly to frequency data

        filtered_frequency_data.append(filtered_frequency)

    return filtered_frequency_data


def apply_directional_high_pass_filter(frequency_data, cutoff_frequency, angle_ranges, save_mask_path=None):
    """
    Apply a directional high-pass filter to the frequency data and optionally save the mask.

    Args:
        frequency_data: List of frequency domain data for each channel.
        cutoff_frequency: The cutoff frequency for the high-pass filter.
        angle_ranges: List of tuples with angle ranges (min_angle, max_angle), in degrees.
        save_mask_path: If provided, saves the mask as an image at this path.

    Returns:
        Filtered frequency data.
    """
    filtered_frequency_data = []

    for frequency in frequency_data:
        # Get the dimensions of the frequency data
        height, width = frequency.shape

        # Create the frequency grid
        u = np.arange(width)
        v = np.arange(height)
        u[u > width // 2] -= width
        v[v > height // 2] -= height
        U, V = np.meshgrid(u, v)

        # Calculate the distance from the origin (magnitude in frequency space)
        distance = np.sqrt(U**2 + V**2)

        # Calculate the angle of each point in the frequency domain
        angle = np.degrees(np.arctan2(V, U)) % 360  # Angle in degrees, range [0, 360)

        # Initialize a mask with zeros (i.e., exclude all by default)
        mask = np.zeros((height, width), dtype=float)

        # Loop through each angular range and set the corresponding regions to 1
        for (theta_min, theta_max) in angle_ranges:
            # Apply the mask for the original angular range
            if theta_min > theta_max:
                mask[(angle >= theta_min) | (angle <= theta_max)] = 1
            else:
                mask[(angle >= theta_min) & (angle <= theta_max)] = 1

            # Calculate the 180-degree rotated range
            rotated_min = (theta_min - 180) % 360
            rotated_max = (theta_max - 180) % 360

            # Apply the mask for the rotated range
            if rotated_min > rotated_max:
                mask[(angle >= rotated_min) | (angle <= rotated_max)] = 1
            else:
                mask[(angle >= rotated_min) & (angle <= rotated_max)] = 1

        # Incorporate the high-pass cutoff frequency

        mask[distance < cutoff_frequency] = 0

        # Apply the high-pass filter: multiply frequency by the inverted mask
        filtered_frequency = frequency * mask

        filtered_frequency_data.append(filtered_frequency)

    return filtered_frequency_data




def apply_phase_modifying_filter(frequency_data, k, l):
    """
    Apply a phase modification filter to the frequency data.
    
    Args:
        frequency_data: List of frequency domain data for each channel.
        k: Horizontal shift parameter.
        l: Vertical shift parameter.
    
    Returns:
        Modified frequency data.
    """
    modified_frequency_data = []
    
    for frequency in frequency_data:
        # Calculate the magnitude and phase
        magnitude = np.abs(frequency)
        phase = np.angle(frequency)
        
        # Get the dimensions of the frequency data
        height, width = frequency.shape
        
        # Create a frequency grid manually
        u = np.arange(width)
        v = np.arange(height)
        u[u > width // 2] -= width
        v[v > height // 2] -= height
        U, V = np.meshgrid(u, v)
        
        # Calculate the phase modification mask using the manual frequency grid
        phase_mask = np.exp(1j * (-k * 2 * np.pi * U / width - l * 2 * np.pi * V / height + (k + l) * np.pi))
        
        # Apply the phase modification
        modified_phase = np.angle(phase_mask)
        modified_frequency = magnitude * np.exp(1j * (phase + modified_phase))
        
        modified_frequency_data.append(modified_frequency)
    
    return modified_frequency_data