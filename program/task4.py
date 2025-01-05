import sys
import numpy as np
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