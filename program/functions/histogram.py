from PIL import Image


def calculate_histogram(image_pixels, mode):
    """
    Calculate the histogram based on the image mode (grayscale or RGB).
    Returns the histogram data for each channel (if RGB) or a single histogram (if grayscale).
    """
    histogram = [0] * 256  # Initialize a list of 256 zeros for histogram counts

    if mode == 'L':  # Grayscale image
        # Iterate over each pixel and update the histogram
        for pixel in image_pixels:
            histogram[pixel] += 1
        return histogram

    elif mode == 'RGB':  # RGB image
        # Separate histograms for red, green, and blue channels
        r_histogram = [0] * 256
        g_histogram = [0] * 256
        b_histogram = [0] * 256

        for pixel in image_pixels:
            r, g, b = pixel
            r_histogram[r] += 1
            g_histogram[g] += 1
            b_histogram[b] += 1

        return r_histogram, g_histogram, b_histogram


def save_histogram_image(image_pixels, mode, output_path="histogram.png"):
    """
    Given the image pixels and mode, calculate the histogram and save it as an image.
    """
    # Create an empty white image (for the histogram plot)
    width = 256  # The histogram image will have 256 pixels width
    height = 200  # You can adjust the height depending on the histogram's scaling
    image = Image.new("RGB", (width, height), (255, 255, 255))  # White background
    pixel_data = image.load()

    # Calculate the histogram for grayscale or RGB image
    histogram_data = calculate_histogram(image_pixels, mode)

    if isinstance(histogram_data, tuple):  # If the histogram data contains R, G, and B channels
        red_hist, green_hist, blue_hist = histogram_data
        max_val = max(max(red_hist), max(green_hist), max(blue_hist))  # Find max value for scaling

        # Scale the histograms to fit the image height
        for i in range(256):
            # For each channel, draw bars for the histogram
            red_height = int((red_hist[i] / max_val) * height)
            green_height = int((green_hist[i] / max_val) * height)
            blue_height = int((blue_hist[i] / max_val) * height)

            for y in range(height - red_height, height):
                pixel_data[i, y] = (255 - red_height, 0, 0)  # Red channel (Red bar)
            for y in range(height - green_height, height):
                pixel_data[i, y] = (0, 255 - green_height, 0)  # Green channel (Green bar)
            for y in range(height - blue_height, height):
                pixel_data[i, y] = (0, 0, 255 - blue_height)  # Blue channel (Blue bar)
    else:  # Grayscale image, histogram has one channel
        max_val = max(histogram_data)  # Find max value for scaling

        # Scale the histogram to fit the image height
        for i in range(256):
            height_scaled = int((histogram_data[i] / max_val) * height)
            for y in range(height - height_scaled, height):
                pixel_data[i, y] = (0, 0, 0)  # Black bar representing histogram

    # Save the histogram image
    image.save(output_path)
    print(f"Histogram saved as: {output_path}")
