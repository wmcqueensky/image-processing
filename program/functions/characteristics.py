import math

# (C1) Histogram-based Mean (grayscale only)
def calculate_mean(histogram):
    """
    Calculate the Histogram-based Mean using the formula:
    b̄ = (1/N) * Σ (m * H(m)), where m = 0 to L-1
    b̄: Mean brightness based on the histogram
    N: Total number of pixels
    H(m): Histogram value for brightness level m
    """
    total_pixels = sum(histogram)
    mean = sum(m * histogram[m] for m in range(256)) / total_pixels  # sum of m * H(m)

    return mean

def calculate_mean_rgb(histograms):
    """
    Calculate the histogram-based mean for RGB images.
    histograms will be a tuple (r_histogram, g_histogram, b_histogram)
    """
    means = []
    for hist in histograms:
        total_pixels = sum(hist)
        mean = sum(m * hist[m] for m in range(256)) / total_pixels
        means.append(mean)

    return means  # Return a list [mean_r, mean_g, mean_b]



def calculate_variance(histogram, mean):
    """
    Calculate the variance (D^2) using the formula:
    D^2 = (1/N) * Σ (m - b̄)^2 * H(m), where m = 0 to L-1
    D^2: Variance (squared deviation from the mean)
    b̄: Mean brightness
    N: Total number of pixels
    H(m): Histogram value for brightness level m
    """
    total_pixels = sum(histogram)  # N: total number of pixels
    variance = sum((m - mean) ** 2 * histogram[m] for m in range(256)) / total_pixels  # sum of (m - b̄)^2 * H(m)


    return variance


def calculate_variance_rgb(histograms, means):
    """
    Calculate the variance for each channel (R, G, B) of an RGB image.
    histograms will be a tuple (r_histogram, g_histogram, b_histogram)
    means will be a tuple (mean_r, mean_g, mean_b)
    """
    variances = []  # List to store variances for R, G, B

    # Loop through each channel's histogram and corresponding mean value
    for hist, mean in zip(histograms, means):
        total_pixels = sum(hist)  # Total number of pixels in the channel
        variance = sum((m - mean) ** 2 * hist[m] for m in range(256)) / total_pixels  # Calculate variance
        variances.append(variance)  # Add the variance to the list

    return variances  # Return the list of variances for R, G, and B


def calculate_standard_dev(variance):
    st_dev = math.sqrt(variance)

    return st_dev


def calculate_variation_coefficient_1 (mean, deviation):
    v_c_1 = deviation/mean

    return v_c_1


def calculate_asymmetry_coefficient(histogram):
    """
    Calculate the asymmetry coefficient for a single color channel.
    """
    total_pixels = sum(histogram)  # N: total number of pixels
    mean = calculate_mean(histogram)  # Calculate mean for the channel
    variance = calculate_variance(histogram, mean)  # Calculate variance for the channel
    st_dev = math.sqrt(variance)  # Standard deviation

    # Asymmetry coefficient calculation
    asym_coe = sum((m - mean) ** 3 * histogram[m] for m in range(len(histogram))) / (total_pixels * st_dev ** 3)
    return asym_coe

def calculate_asymmetry_coefficient_rgb(histograms):
    """
    Calculate the asymmetry coefficient for each channel (R, G, B) in an RGB image.
    histograms: A tuple (r_histogram, g_histogram, b_histogram)
    """
    coefficients = []  # Use a list to store coefficients

    # Calculate the asymmetry coefficient for each channel
    for histogram in histograms:
        asym_coe = calculate_asymmetry_coefficient(histogram)
        coefficients.append(asym_coe)  # Append coefficient to the list

    return coefficients  # Return the list of coefficients


def calculate_flattening_coefficient(histogram):
    """
    Calculate the Flattening coefficient (bK) using the formula:
    bK = (1 / (σ^4 * N)) * Σ (m - b̄)^4 * H(m) - 3, where m = 0 to L-1
    b̄: Mean brightness based on the histogram
    σ: Standard deviation
    N: Total number of pixels
    H(m): Histogram value for brightness level m
    """
    mean = calculate_mean(histogram)  # Calculate mean brightness
    variance = calculate_variance(histogram, mean)  # Calculate variance
    st_dev = math.sqrt(variance)  # Standard deviation (σ)
    total_pixels = sum(histogram)  # N: total number of pixels

    # Flattening coefficient (bK) calculation
    fl_co = (1 / (st_dev ** 4 * total_pixels)) * sum((m - mean) ** 4 * histogram[m] for m in range(256)) - 3


    return fl_co


def calculate_flattening_coefficient_rgb(histograms):
    """
    Calculate the Flattening coefficient for each channel (R, G, B) of an RGB image.
    histograms: A tuple (r_histogram, g_histogram, b_histogram)
    """
    flattening_coeffs = []  # Use a list instead of a dictionary

    # Calculate the flattening coefficient for each channel
    for histogram in histograms:
        fl_co = calculate_flattening_coefficient(histogram)  # Compute the coefficient
        flattening_coeffs.append(fl_co)  # Append to the list

    return flattening_coeffs  # Return the list of coefficients



def calculate_variation_coefficient_2(histogram):
    """
    Calculate the Variation Coefficient 2  using the formula:
    bN = (1 / N^2) * Σ (H(m))^2, where m = 0 to L-1
    N: Total number of pixels
    H(m): Histogram value for brightness level m
    """
    total_pixels = sum(histogram)  # N: total number of pixels

    # Sum of squared histogram values
    sum_of_squares = sum(histogram[m] ** 2 for m in range(256))

    # Variation Coefficient 2 calculation
    var_co = sum_of_squares / (total_pixels ** 2)


    return var_co


def calculate_variation_coefficient_2_rgb(histograms):
    """
    Calculate the Variation Coefficient 2 for each channel (R, G, B) of an RGB image.
    histograms: A tuple (r_histogram, g_histogram, b_histogram)
    """
    variation_coeffs = []  # Use a list instead of a dictionary

    # Calculate the Variation Coefficient 2 for each channel
    for histogram in histograms:
        var_co = calculate_variation_coefficient_2(histogram)  # Compute coefficient for the channel
        variation_coeffs.append(var_co)  # Add to the list

    return variation_coeffs  # Return the list of coefficients



def calculate_entropy(histogram):
    """
    Calculate the Information Source Entropy using the formula:
    bE = - (1 / N) * Σ H(m) * log2(H(m) / N), where m = 0 to L-1
    """
    total_pixels = sum(histogram)  # N: total number of pixels

    # Entropy calculation, avoiding log(0) by checking if H(m) > 0
    entropy = -sum(histogram[m] * math.log2(histogram[m] / total_pixels) for m in range(256) if histogram[m] > 0) / total_pixels

    return entropy



def calculate_entropy_rgb(histograms):
    """
    Calculate the Information Source Entropy for each channel (R, G, B) of an RGB image.
    histograms: A tuple (r_histogram, g_histogram, b_histogram)
    """
    entropy_values = []  # Use a list instead of a dictionary

    # Calculate the entropy for each channel
    for histogram in histograms:
        ent_val = calculate_entropy(histogram)  # Compute entropy for the channel
        entropy_values.append(ent_val)  # Add to the list

    return entropy_values  # Return the list of entropies

