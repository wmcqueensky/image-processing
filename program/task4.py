import sys
import numpy as np

from functions.low_high_pass_filter import apply_directional_filter, apply_phase_modification, apply_band_cut_filter, \
    apply_band_pass_filter
from utils.file_operations import load_image, save_image
from utils.help import print_help
from utils.parse_arguments import parse_arguments
from functions.fourier import process_and_save_fourier, compute_frequency_data
from functions.low_high_pass_filter import apply_low_pass_filter, apply_high_pass_filter, process_and_save_filtered

# ==============================
# TASK 4 SCRIPT
# ==============================

if len(sys.argv) < 2 or '--help' in sys.argv:
    print_help()
    sys.exit()

input_image_path = sys.argv[1]
output_image_path = sys.argv[2]
commands = sys.argv[3:]

# Load image and extract metadata
original_pixels, mode, size, im = load_image(input_image_path)
pixels = original_pixels.copy()

# Parse command-line arguments into a dictionary
args_dict = parse_arguments(commands)

# Precompute frequency data if needed
use_fast = str(args_dict.get("fast", "True")).lower() == "true"
frequency_data = compute_frequency_data(pixels, size, mode, use_fast)

# Apply Fourier Transform and Inverse Fourier Transform
if "fourier" in args_dict:
    print("Applying Fourier Transform and Inverse Fourier Transform...")
    try:
        process_and_save_fourier(
            input_pixels=pixels,
            size=size,
            mode=mode,
            output_base_path=output_image_path.replace('.bmp', ''),
            use_fast=use_fast,
            frequency_data=frequency_data
        )
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

# Apply Low-pass Filter
if "lowpass" in args_dict:
    cutoff_frequency = float(args_dict.get("lowpass", 30))  # Default cutoff frequency
    print(f"Applying Low-pass filter with cutoff frequency {cutoff_frequency}...")
    filtered_frequency_data = apply_low_pass_filter(frequency_data, cutoff_frequency)
    process_and_save_filtered(
        frequency_data=filtered_frequency_data,
        size=size,
        mode=mode,
        output_base_path=output_image_path.replace('.bmp', '_lowpass'),
        filter_type='lowpass'
    )

# Apply High-pass Filter
if "highpass" in args_dict:
    cutoff_frequency = float(args_dict.get("highpass", 30))  # Default cutoff frequency
    print(f"Applying High-pass filter with cutoff frequency {cutoff_frequency}...")
    filtered_frequency_data = apply_high_pass_filter(frequency_data, cutoff_frequency)
    process_and_save_filtered(
        frequency_data=filtered_frequency_data,
        size=size,
        mode=mode,
        output_base_path=output_image_path.replace('.bmp', '_highpass'),
        filter_type='highpass'
    )


# Apply Band-Pass Filter
if "bandpass" in args_dict:
    f_low = float(args_dict.get("bandpass_low", 10))  # Default low cutoff frequency
    f_high = float(args_dict.get("bandpass_high", 50))  # Default high cutoff frequency
    print(f"Applying Band-Pass Filter with f_low={f_low}, f_high={f_high}...")
    filtered_frequency_data = apply_band_pass_filter(frequency_data, f_low, f_high)
    process_and_save_filtered(
        frequency_data=filtered_frequency_data,
        size=size,
        mode=mode,
        output_base_path=output_image_path.replace('.bmp', '_bandpass'),
        filter_type='bandpass'
    )

# Apply Band-Cut Filter
if "bandcut" in args_dict:
    f_low = float(args_dict.get("bandcut_low", 10))  # Default low cutoff frequency
    f_high = float(args_dict.get("bandcut_high", 50))  # Default high cutoff frequency
    print(f"Applying Band-Cut Filter with f_low={f_low}, f_high={f_high}...")
    filtered_frequency_data = apply_band_cut_filter(frequency_data, f_low, f_high)
    process_and_save_filtered(
        frequency_data=filtered_frequency_data,
        size=size,
        mode=mode,
        output_base_path=output_image_path.replace('.bmp', '_bandcut'),
        filter_type='bandcut'
    )

# Apply Directional Filter
if "directional" in args_dict:
    theta_min = float(args_dict.get("theta_min", 0))  # Default angle range start
    theta_max = float(args_dict.get("theta_max", np.pi/4))  # Default angle range end
    print(f"Applying Directional Filter with angle_range=({theta_min}, {theta_max})...")
    filtered_frequency_data = apply_directional_filter(frequency_data, (theta_min, theta_max))
    process_and_save_filtered(
        frequency_data=filtered_frequency_data,
        size=size,
        mode=mode,
        output_base_path=output_image_path.replace('.bmp', '_directional'),
        filter_type='directional'
    )

# Apply Phase Modification
if "phase_mod" in args_dict:
    def custom_phase_function(phase):
        # Example: Add a constant shift of pi/4 to the phase
        return phase + np.pi / 4

    print("Applying Phase Modification...")
    modified_frequency_data = apply_phase_modification(frequency_data, custom_phase_function)
    process_and_save_filtered(
        frequency_data=modified_frequency_data,
        size=size,
        mode=mode,
        output_base_path=output_image_path.replace('.bmp', '_phase_mod'),
        filter_type='phase_mod'
    )
