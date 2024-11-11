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
    total_pixels = sum(histogram)  # N: total number of pixels
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
        mean = sum(i * hist[i] for i in range(256)) / total_pixels
        means.append(mean)

    return means  # This returns a list [mean_r, mean_g, mean_b]



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
    variances = {}
    for i, (hist, mean) in enumerate(zip(histograms, means)):
        # Calculate the variance for the current channel (R, G, or B)
        total_pixels = sum(hist)
        variance = sum((m - mean) ** 2 * hist[m] for m in range(256)) / total_pixels
        channel_name = ['Red', 'Green', 'Blue'][i]
        variances[channel_name] = variance


    return variances

def calculate_standard_dev(variance):
    st_dev = math.sqrt(variance)

    return st_dev


def calculate_variation_coefficient_1 (mean, deviation):
    v_c_1 = deviation/mean

    return v_c_1


def calculate_asymmetry_coefficient(histogram):
    """
    Calculate the asymmetry coefficient `b_S` for a single color channel.
    """
    total_pixels = sum(histogram)  # N: total number of pixels
    mean = calculate_mean(histogram)  # Calculate mean for the channel
    variance = calculate_variance(histogram, mean)  # Calculate variance for the channel
    sigma = math.sqrt(variance)  # Standard deviation

    # Asymmetry coefficient calculation
    b_S = sum((m - mean) ** 3 * histogram[m] for m in range(len(histogram))) / (total_pixels * sigma ** 3)
    return b_S


# Main code to handle RGB images
def calculate_asymmetry_coefficient_rgb(histograms):
    """
    Calculate the asymmetry coefficient for each channel (R, G, B) in an RGB image.
    histograms: A tuple (r_histogram, g_histogram, b_histogram)
    """
    coefficients = {}
    channel_names = ['Red', 'Green', 'Blue']

    # Calculate the asymmetry coefficient for each channel
    for i, histogram in enumerate(histograms):
        b_S = calculate_asymmetry_coefficient(histogram)
        coefficients[channel_names[i]] = b_S

    return coefficients


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
    sigma = math.sqrt(variance)  # Standard deviation (σ)
    total_pixels = sum(histogram)  # N: total number of pixels

    # Flattening coefficient (bK) calculation
    bK = (1 / (sigma ** 4 * total_pixels)) * sum((m - mean) ** 4 * histogram[m] for m in range(256)) - 3


    return bK


def calculate_flattening_coefficient_rgb(histograms):
    """
    Calculate the Flattening coefficient for each channel (R, G, B) of an RGB image.
    histograms: A tuple (r_histogram, g_histogram, b_histogram)
    """
    flattening_coeffs = {}
    channel_names = ['Red', 'Green', 'Blue']

    # Calculate the flattening coefficient for each channel
    for i, histogram in enumerate(histograms):
        bK = calculate_flattening_coefficient(histogram)
        flattening_coeffs[channel_names[i]] = bK


    return flattening_coeffs



def calculate_variation_coefficient_2(histogram):
    """
    Calculate the Variation Coefficient 2 (bN) using the formula:
    bN = (1 / N^2) * Σ (H(m))^2, where m = 0 to L-1
    N: Total number of pixels
    H(m): Histogram value for brightness level m
    """
    total_pixels = sum(histogram)  # N: total number of pixels

    # Sum of squared histogram values
    sum_of_squares = sum(H_m ** 2 for H_m in histogram)

    # Variation Coefficient 2 calculation
    bN = sum_of_squares / (total_pixels ** 2)


    return bN


def calculate_variation_coefficient_2_rgb(histograms):
    """
    Calculate the Variation Coefficient 2 for each channel (R, G, B) of an RGB image.
    histograms: A tuple (r_histogram, g_histogram, b_histogram)
    """
    variation_coeffs = {}
    channel_names = ['Red', 'Green', 'Blue']

    # Calculate the Variation Coefficient 2 for each channel
    for i, histogram in enumerate(histograms):
        bN = calculate_variation_coefficient_2(histogram)
        variation_coeffs[channel_names[i]] = bN


    return variation_coeffs


def calculate_entropy(histogram):
    """
    Calculate the Information Source Entropy (bE) using the formula:
    bE = - (1 / N) * Σ H(m) * log2(H(m) / N), where m = 0 to L-1
    """
    total_pixels = sum(histogram)  # N: total number of pixels

    # Entropy calculation, avoiding log(0) by checking if H(m) > 0
    entropy = -sum(H_m * math.log2(H_m / total_pixels) for H_m in histogram if H_m > 0) / total_pixels

    return entropy


def calculate_entropy_rgb(histograms):
    """
    Calculate the Information Source Entropy for each channel (R, G, B) of an RGB image.
    histograms: A tuple (r_histogram, g_histogram, b_histogram)
    """
    entropy_values = {}
    channel_names = ['Red', 'Green', 'Blue']

    # Calculate the entropy for each channel
    for i, histogram in enumerate(histograms):
        bE = calculate_entropy(histogram)
        entropy_values[channel_names[i]] = bE


    return entropy_values
