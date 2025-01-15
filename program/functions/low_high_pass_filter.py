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
    """
    filtered_frequency_data = []
    for frequency in frequency_data:
        height, width = frequency.shape
        u = np.fft.fftfreq(width, 1.0 / width)
        v = np.fft.fftfreq(height, 1.0 / height)
        U, V = np.meshgrid(u, v)
        distance = np.sqrt(U**2 + V**2)

        mask = (distance >= f_low) & (distance <= f_high)
        filtered_frequency = frequency * mask
        filtered_frequency_data.append(filtered_frequency)
    return filtered_frequency_data

def apply_band_cut_filter(frequency_data, f_low, f_high):
    """
    Apply a band-cut (notch) filter to the frequency data.
    Suppresses frequencies between f_low and f_high.
    """
    print('frequency data')
    print(frequency_data)
    filtered_frequency_data = []
    for frequency in frequency_data:
        height, width = frequency.shape
        print('height:')
        print(height)
        print('width:')
        print(width)
        # u = fast_fft(np.arange(width) / width)
        u = np.fft.fftfreq(width, 1.0 / width)
        print('u:')
        print(u)
        # v = fast_fft(np.arange(height) / height)
        v = np.fft.fftfreq(height, 1.0 / height)
        print('v:')
        print(v)
        U, V = np.meshgrid(u, v)
        print('U:')
        print(U)
        print('V:')
        print(V)
        distance = np.sqrt(U**2 + V**2)
        print('Distance:')
        print(distance)

        mask = (distance < f_low) | (distance > f_high)
        print('mask:')
        print(mask)
        filtered_frequency = frequency * mask
        print('filtered frequency:')
        print(filtered_frequency)
        filtered_frequency_data.append(filtered_frequency)
    return filtered_frequency_data


def apply_directional_high_pass_filter(frequency_data, cutoff_frequency, angle_range, mask_image_path=None):
    """
    Apply a directional high-pass filter with optional mask to frequency domain data.

    Args:
        frequency_data: List of frequency domain data for each channel.
        cutoff_frequency: The cutoff frequency for the high-pass filter.
        angle_range: Tuple (theta_min, theta_max) in radians.
        mask_image_path: Optional path to a grayscale mask image to apply in the frequency domain.

    Returns:
        Filtered frequency domain data.
    """

    theta_min, theta_max = angle_range
    filtered_frequency_data = []
    print('theta min:', theta_min)
    print('theta max:', theta_max)

    # If a mask is provided, load and normalize it
    mask = None
    if mask_image_path:
        try:
            mask_image = Image.open(mask_image_path).convert('L')
            mask = np.array(mask_image, dtype=float) / 255.0  # Normalize to [0, 1]
        except Exception as e:
            print(f"Error loading mask image: {e}")
            return None
    print('mask:', mask)
    print("Mask min:", mask.min())
    print("Mask max:", mask.max())

    for frequency in frequency_data:
        # Get dimensions of frequency data
        height, width = frequency.shape

        print('height:', height)
        print('width:', width)

        # Create frequency grid
        u = np.fft.fftfreq(width, 1.0 / width)
        v = np.fft.fftfreq(height, 1.0 / height)
        U, V = np.meshgrid(u, v)

        # Calculate distance and angle
        distance = np.sqrt(U ** 2 + V ** 2)
        angle = np.arctan2(V, U)

        # Create the high-pass filter mask (cutoff frequency)
        high_pass_mask = distance >= cutoff_frequency

        # Create the directional filter mask
        directional_mask = (angle >= theta_min) & (angle <= theta_max)

        # Combine masks
        combined_mask = high_pass_mask & directional_mask

        # If a user mask is provided, combine it
        if mask is not None:
            user_mask_resized = np.resize(mask, (height, width))  # Resize user mask to match frequency dimensions
            combined_mask = combined_mask & (user_mask_resized > 0.5)  # Apply user mask (threshold > 0.5)

        # Apply the combined mask to the frequency data
        filtered_frequency = frequency * combined_mask
        filtered_frequency_data.append(filtered_frequency)

    return filtered_frequency_data

#F5 start


def apply_high_pass_edge_with_mask(input_image_path, mask_path, output_image_path):
    print(f"Mask Path: {mask_path}")  # Debugging line to check the mask path
    # Load mask
    try:
        mask_image = Image.open(mask_path).convert('L')
    except Exception as e:
        print(f"Error loading mask image: {e}")
        sys.exit(1)
    mask_kernel = np.array(mask_image, dtype=float)

    # Normalize kernel (optional, depending on how the mask is designed)
    mask_kernel /= np.sum(np.abs(mask_kernel)) if np.sum(np.abs(mask_kernel)) != 0 else 1

    # High-pass filter kernel (Laplacian example)
    high_pass_kernel = np.array([[0, -1, 0],
                                 [-1, 4, -1],
                                 [0, -1, 0]])

    # Load the input image
    input_image = Image.open(input_image_path).convert('L')
    input_array = np.array(input_image, dtype=float)

    # Apply high-pass filter
    high_pass_filtered = convolve(input_array, high_pass_kernel)

    # Apply edge detection using the mask
    edge_direction = convolve(high_pass_filtered, mask_kernel)

    # Normalize for visualization
    edge_direction_normalized = (edge_direction - edge_direction.min()) / (edge_direction.max() - edge_direction.min()) * 255
    edge_direction_image = Image.fromarray(edge_direction_normalized.astype(np.uint8))

    # Save or display the result
    edge_direction_image.save(output_image_path)
    print(f"Edge direction detection saved to '{output_image_path}'.")


def apply_phase_modifying_filter(frequency_data, k, l):
    modified_frequency_data = []

    for frequency in frequency_data:

        # Calculate the magnitude and phase
        magnitude = np.abs(frequency)
        phase = np.angle(frequency)

        # Get the dimensions of the frequency data
        height, width = frequency.shape
        u = np.fft.fftfreq(width, 1.0 / width)
        v = np.fft.fftfreq(height, 1.0 / height)
        U, V = np.meshgrid(u, v)


        # Calculate the phase modification mask based on the provided formula
        phase_mask = np.exp(1j * (-k * 2 * np.pi * U / width - l * 2 * np.pi * V / height + (k + l) * np.pi))

        # Apply the phase modification to the frequency data
        modified_phase = np.angle(phase_mask)
        modified_frequency = magnitude * np.exp(1j * (phase + modified_phase))

        modified_frequency_data.append(modified_frequency)

    return modified_frequency_data
