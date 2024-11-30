def apply_roberts_operator(pixels, size):
    """Applies Roberts II operator to an image in the spatial domain for edge detection."""
    # CZY TUTAJ NIE TRZBEA JAKIEGOŚ KERNELA ZEBY TO BYLO 2x2, COŚ WSPOMINAŁ NA ZAJĘCIACH
    width, height = size
    new_pixels = []
    
    # Iterate over each pixel, ignoring the last row and column (boundary pixels)
    for y in range(height):
        for x in range(width):
            if x < width - 1 and y < height - 1:
                # Calculate indices for current pixel and its neighbors
                idx = y * width + x
                idx_right = y * width + (x + 1)
                idx_below = (y + 1) * width + x
                idx_diag = (y + 1) * width + (x + 1)
                
                # Roberts II operator calculation
                if isinstance(pixels[0], tuple):  # RGB image
                    r = abs(pixels[idx][0] - pixels[idx_diag][0]) + abs(pixels[idx_right][0] - pixels[idx_below][0])
                    g = abs(pixels[idx][1] - pixels[idx_diag][1]) + abs(pixels[idx_right][1] - pixels[idx_below][1])
                    b = abs(pixels[idx][2] - pixels[idx_diag][2]) + abs(pixels[idx_right][2] - pixels[idx_below][2])
                    new_pixels.append((min(255, r), min(255, g), min(255, b)))  # Clamp values to [0, 255]
                else:  # Grayscale image
                    g = abs(pixels[idx] - pixels[idx_diag]) + abs(pixels[idx_right] - pixels[idx_below])
                    new_pixels.append(min(255, g))  # Clamp values to [0, 255]
            else:
                # For boundary pixels, append zero (black)
                if isinstance(pixels[0], tuple):
                    new_pixels.append((0, 0, 0))
                else:
                    new_pixels.append(0)
    return new_pixels