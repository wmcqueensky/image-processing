def print_help():
    """Prints available commands and their usage."""
    help_text = """
    Image Processor - Available Commands:
    
    Usage: python3 main.py <input_image> <output_image> [--command=value ...]

    Commands:
      --brightness=value      Adjust brightness by the specified value (positive or negative)
      --contrast=value        Adjust contrast by the specified value (e.g., 1.2 to increase, 0.8 to decrease)
      --negative              Apply a negative filter (no additional arguments needed)

      Geometric Operations:
      --hflip                 Flip the image horizontally
      --vflip                 Flip the image vertically
      --dflip                 Flip the image along the diagonal (transpose)
      --shrink=value          Shrink the image by the given factor (e.g., 2 to halve the size)
      --enlarge=value         Enlarge the image by the given factor (e.g., 2 to double the size)
    
    Example Usage:
      python3 main.py input.bmp output.bmp --brightness=50 --contrast=1.5
      python3 main.py input.bmp output.bmp --hflip --shrink=2
      python3 main.py input.bmp output.bmp --brightness=50 --contrast=1.2 --negative --vflip
    """
    print(help_text)
