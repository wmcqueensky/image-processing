def apply_roberts_operator(pixels, size):
    """Applies Roberts II operator using explicit 2x2 convolution masks for edge detection."""
    width, height = size
    new_pixels = []

    # Define the 2x2 masks
    Gx = [[1, 0], [0, -1]]  # Diagonal difference mask
    Gy = [[0, 1], [-1, 0]]  # Anti-diagonal difference mask

    # Iterate over each pixel, ignoring the last row and column (boundary pixels)
    for y in range(height):
        for x in range(width):
            if x < width - 1 and y < height - 1:
                # Extract the 2x2 region for convolution
                top_left = pixels[y * width + x]
                top_right = pixels[y * width + (x + 1)]
                bottom_left = pixels[(y + 1) * width + x]
                bottom_right = pixels[(y + 1) * width + (x + 1)]

                # Apply the masks
                if isinstance(pixels[0], tuple):  # RGB image
                    # For each channel, calculate Gx and Gy
                    r_gx = Gx[0][0] * top_left[0] + Gx[0][1] * top_right[0] + \
                           Gx[1][0] * bottom_left[0] + Gx[1][1] * bottom_right[0]
                    r_gy = Gy[0][0] * top_left[0] + Gy[0][1] * top_right[0] + \
                           Gy[1][0] * bottom_left[0] + Gy[1][1] * bottom_right[0]

                    g_gx = Gx[0][0] * top_left[1] + Gx[0][1] * top_right[1] + \
                           Gx[1][0] * bottom_left[1] + Gx[1][1] * bottom_right[1]
                    g_gy = Gy[0][0] * top_left[1] + Gy[0][1] * top_right[1] + \
                           Gy[1][0] * bottom_left[1] + Gy[1][1] * bottom_right[1]

                    b_gx = Gx[0][0] * top_left[2] + Gx[0][1] * top_right[2] + \
                           Gx[1][0] * bottom_left[2] + Gx[1][1] * bottom_right[2]
                    b_gy = Gy[0][0] * top_left[2] + Gy[0][1] * top_right[2] + \
                           Gy[1][0] * bottom_left[2] + Gy[1][1] * bottom_right[2]

                    # Compute the magnitude of gradients
                    r = abs(r_gx) + abs(r_gy)
                    g = abs(g_gx) + abs(g_gy)
                    b = abs(b_gx) + abs(b_gy)

                    # Append the clamped values
                    new_pixels.append((min(255, r), min(255, g), min(255, b)))
                else:  # Grayscale image
                    gx = Gx[0][0] * top_left + Gx[0][1] * top_right + \
                         Gx[1][0] * bottom_left + Gx[1][1] * bottom_right
                    gy = Gy[0][0] * top_left + Gy[0][1] * top_right + \
                         Gy[1][0] * bottom_left + Gy[1][1] * bottom_right

                    # Compute the magnitude of gradients
                    g = abs(gx) + abs(gy)

                    # Append the clamped value
                    new_pixels.append(min(255, g))
            else:
                # For boundary pixels, append zero (black)
                if isinstance(pixels[0], tuple):
                    new_pixels.append((0, 0, 0))
                else:
                    new_pixels.append(0)

    return new_pixels
