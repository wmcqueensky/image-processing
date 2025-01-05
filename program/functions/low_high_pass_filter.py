import numpy as np
from utils.file_operations import save_image
from functions.fourier import save_magnitude_spectrum

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
        # Get the dimensions of the frequency data (height and width)
        height, width = frequency.shape
        
        # Create a frequency grid
        u = np.fft.fftfreq(width, 1.0 / width)
        v = np.fft.fftfreq(height, 1.0 / height)
        U, V = np.meshgrid(u, v)
        
        # Calculate the distance from the center of the frequency grid
        distance = np.sqrt(U**2 + V**2)
        
        # Apply the low-pass filter
        mask = distance <= cutoff_frequency
        filtered_frequency = frequency * mask
        
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
        # Get the dimensions of the frequency data (height and width)
        height, width = frequency.shape
        
        # Create a frequency grid
        u = np.fft.fftfreq(width, 1.0 / width)
        v = np.fft.fftfreq(height, 1.0 / height)
        U, V = np.meshgrid(u, v)
        
        # Calculate the distance from the center of the frequency grid
        distance = np.sqrt(U**2 + V**2)
        
        # Apply the high-pass filter
        mask = distance >= cutoff_frequency
        filtered_frequency = frequency * mask
        
        filtered_frequency_data.append(filtered_frequency)
    
    return filtered_frequency_data


def process_and_save_filtered(frequency_data, size, mode, output_base_path, filter_type):
    """
    Apply inverse Fourier transform to filtered frequency data and save the reconstructed image.
    
    Args:
        frequency_data: Filtered frequency domain data for each channel.
        size: Tuple (width, height) of the image.
        mode: Image mode ('L' for grayscale, 'RGB' for color).
        output_base_path: Base path for saving output images.
        filter_type: Type of filter applied ('lowpass' or 'highpass').
    """
    # Save the magnitude spectrum for the filtered frequency data
    save_magnitude_spectrum(frequency_data, size, mode, output_base_path)

    # Apply Inverse Fourier Transform to each channel
    inverse_channels = [np.fft.ifft2(np.fft.ifftshift(channel)) for channel in frequency_data]

    # Normalize and convert back to uint8 for each channel
    reconstructed_channels = [np.real(channel).clip(0, 255).astype(np.uint8) for channel in inverse_channels]

    # Combine the reconstructed channels back into an RGB image (for color images)
    if mode == 'RGB':
        # Stack the RGB channels back together and reshape into a 1D list of tuples
        reconstructed_pixels = np.stack(reconstructed_channels, axis=-1).reshape(-1, 3)
        reconstructed_pixels = [tuple(pixel) for pixel in reconstructed_pixels]  # Convert to tuple format
    else:
        reconstructed_pixels = reconstructed_channels[0].flatten()

    reconstructed_output_path = f"{output_base_path}_{filter_type}.bmp"
    save_image(reconstructed_pixels, mode, size, reconstructed_output_path)
    print(f"Reconstructed {filter_type} image saved to '{reconstructed_output_path}'.")