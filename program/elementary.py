def adjust_brightness(pixels, factor):
    """Adjust brightness by adding factor to each pixel's RGB value."""
    print(f"Adjusting brightness by a factor of {factor}")
    new_pixels = []
    for pixel in pixels:
        if isinstance(pixel, int):  # Grayscale image
            new_pixel = pixel + factor
            new_pixels.append(max(0, min(255, new_pixel)))
        else:  # RGB image
            new_pixel = tuple(max(0, min(255, channel + factor)) for channel in pixel)
            new_pixels.append(new_pixel)
    return new_pixels

def adjust_contrast(pixels, factor):
    """Adjust contrast by multiplying the distance from 128 (midpoint)."""
    print(f"Adjusting contrast by a factor of {factor}")
    midpoint = 128
    new_pixels = []
    for pixel in pixels:
        if isinstance(pixel, int):  # Grayscale image
            new_pixel = int((pixel - midpoint) * factor + midpoint)
            new_pixels.append(max(0, min(255, new_pixel)))
        else:  # RGB image
            new_pixel = tuple(int((channel - midpoint) * factor + midpoint) for channel in pixel)
            new_pixels.append(tuple(max(0, min(255, channel)) for channel in new_pixel))
    return new_pixels

def apply_negative(pixels):
    """Apply a negative effect by inverting the color of each pixel."""
    print(f"Applying negative filter")
    new_pixels = []
    for pixel in pixels:
        if isinstance(pixel, int):  # Grayscale image
            new_pixels.append(255 - pixel)
        else:  # RGB image
            new_pixels.append(tuple(255 - channel for channel in pixel))
    return new_pixels
