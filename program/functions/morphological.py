import numpy as np

def dilation(image, kernel):
    """
    Perform the dilation operation on a binary image, handling `-1` in the kernel.
    """
    # Get dimensions of image and kernel
    image_h, image_w = image.shape
    kernel_h, kernel_w = kernel.shape

    # Calculate padding
    pad_h = kernel_h // 2
    pad_w = kernel_w // 2

    # Pad the input image
    padded_image = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)  # Pad with 0s (black)

    # Prepare the output image
    output_image = np.zeros_like(image)

    # Perform dilation
    for i in range(image_h):
        for j in range(image_w):
            # Extract the region of interest
            region = padded_image[i:i + kernel_h, j:j + kernel_w]

            # Check if any non-`-1` kernel position overlaps with the region
            match = False
            for m in range(kernel_h):
                for n in range(kernel_w):
                    if region[m, n] == 1 and kernel[m, n] == 1:
                        match = True
                        break
                if match:
                    break

            output_image[i, j] = 1 if match else 0

    return output_image


def erosion(image, kernel):
    """
    Perform the erosion operation on a binary image, handling `-1` in the kernel.
    """
    # Get dimensions of image and kernel
    image_h, image_w = image.shape

    kernel_h, kernel_w = kernel.shape

    # Calculate padding
    pad_h = kernel_h // 2
    pad_w = kernel_w // 2

    # Pad the input image
    padded_image = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=1)  # Pad with 1s (white)

    # Prepare the output image
    output_image = np.ones_like(image)  # Start with all pixels as 1 (white)

    # Perform erosion
    for i in range(image_h):
        for j in range(image_w):
            # Extract the region of interest
            region = padded_image[i:i + kernel_h, j:j + kernel_w]

            # Check if all non-`-1` kernel positions match the region
            match = True
            for m in range(kernel_h):
                for n in range(kernel_w):
                    if kernel[m, n] == 1 and region[m, n] != 1:
                        match = False
                        break
                if not match:
                    break

            output_image[i, j] = 1 if match else 0

    return output_image


def opening(image, kernel):
    """
    Perform the opening operation (erosion followed by dilation).
    """
    # First, apply erosion
    eroded_image = erosion(image, kernel)

    # Then, apply dilation to the result of erosion
    opened_image = dilation(eroded_image, kernel)

    return opened_image


def closing(image, kernel):
    """
    Perform the closing operation (dilation followed by erosion).
    """
    # First, apply dilation
    dilated_image = dilation(image, kernel)

    # Then, apply erosion to the result of dilation
    closed_image = erosion(dilated_image, kernel)

    return closed_image


def hitOrMiss(image, foreground_kernel, background_kernel=None):
    """
    Perform the hit-or-miss transform on a binary image.
    """

    # Erode the image with the foreground kernel (this matches foreground pixels)
    eroded_foreground = erosion(image, foreground_kernel)
    print("Eroded Foreground")
    print(eroded_foreground)

    if background_kernel is not None:
        # Invert the image for the background kernel (background becomes foreground)
        print("Original image")
        print(image)
        inverted_image = np.logical_not(image)
        print("inverted image:")
        print(inverted_image)

        # Erode the inverted image with the background kernel (this matches background pixels)
        eroded_background = erosion(inverted_image, background_kernel)
        print("Eroded Background")
        print(eroded_background)

        # Combine the results using logical AND
        result = np.logical_and(eroded_foreground, eroded_background)
        print("Result:")
        print(result)
    else:
        # If no background kernel is provided, use only the foreground erosion
        result = eroded_foreground

    return result.astype(np.uint8)



def iterative_dilation(image, p, kernel):
    """
    Perform iterative dilation starting from point p until the set stops changing.
    """
    # Initialize the set X_0, which is just the point p
    X_k = np.zeros_like(image)
    print('X_k')
    print(X_k)
    print(' X_k[p[0], p[1]]')
    print( X_k[p[0], p[1]])
    print('p')
    print(p)

    X_k[p[0], p[1]] = 1  # Set the initial point as 1 (foreground)


    while True:
        # Dilate the current set X_k with the kernel
        X_k_next = dilation(X_k, kernel)
        print('X_k_next before intersect')
        print(X_k_next)

        # Intersect with the original image A (this is equivalent to X_k = (X_k ⊕ B) ∩ A)
        X_k_next = X_k_next & image
        print('X_k_next after intersect')
        print(X_k_next)

        # Check if the set has stabilized (X_k == X_k_next)
        if np.array_equal(X_k, X_k_next):
            break

        X_k = X_k_next

    return X_k

