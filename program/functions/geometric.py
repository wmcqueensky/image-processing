import sys

def horizontal_flip(pixels, width, height):
    """Flip the image horizontally by reversing each row."""
    print("Applying horizontal flip")
    new_pixels = []
    for y in range(height):
        row = pixels[y * width: (y + 1) * width]
        new_pixels.extend(row[::-1])  # Reverse the row
    return new_pixels

def vertical_flip(pixels, width, height):
    """Flip the image vertically by reversing the rows."""
    print("Applying vertical flip")
    new_pixels = []
    for y in range(height - 1, -1, -1):  # Start from the last row and move upwards
        row = pixels[y * width: (y + 1) * width]
        new_pixels.extend(row)
    return new_pixels

def diagonal_flip(pixels, width, height):
    """Flip the image diagonally by first applying a vertical flip and then a horizontal flip."""
    ##nie wiem czy to dobrze działa :(
    print("Applying diagonal flip (vertical flip followed by horizontal flip)")

    # Step 1: Vertical flip
    vertical_flipped_pixels = [None] * len(pixels)
    for y in range(height):
        for x in range(width):
            vertical_flipped_pixels[y * width + x] = pixels[(height - y - 1) * width + x]

    # Step 2: Horizontal flip
    diagonal_flipped_pixels = [None] * len(pixels)
    for y in range(height):
        for x in range(width):
            diagonal_flipped_pixels[y * width + x] = vertical_flipped_pixels[y * width + (width - x - 1)]

    return diagonal_flipped_pixels

def shrink_image(pixels, width, height, factor):
    """Shrink the image by a given factor."""
    if factor <= 0:
        print("Error: Shrink factor must be greater than 0.")
        sys.exit()
    print(f"Shrinking image by a factor of {factor}")
    new_width = int(width / factor)
    new_height = int(height / factor)
    new_pixels = []

    for y in range(0, height, factor):
        for x in range(0, width, factor):
            new_pixels.append(pixels[y * width + x])  # Pick one pixel per 'factor' block

    return new_pixels, new_width, new_height

def enlarge_image(pixels, width, height, factor):
    """Enlarge the image by a given factor."""
    if factor <= 0:
        print("Error: Enlargement factor must be greater than 0.")
        sys.exit()
    print(f"Enlarging image by a factor of {factor}")
    new_width = int(width * factor)
    new_height = int(height * factor)
    new_pixels = []

    for y in range(height):
        for _ in range(factor):  # Repeat each row 'factor' times
            for x in range(width):
                new_pixels.extend([pixels[y * width + x]] * factor)  # Repeat each pixel 'factor' times

    return new_pixels, new_width, new_height
