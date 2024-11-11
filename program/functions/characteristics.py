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

    print(f"Histogram-based mean: {mean}")
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

    print(f"Histogram-based means for RGB channels: {means}")
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

    print(f"Variance: {variance}")
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

    print(f"Variance for RGB channels: {variances}")
    return variances

def calculate_standard_dev(variance):
    st_dev = math.sqrt(variance)
    print(f"Standard deviation: {st_dev}")
    return st_dev


def calculate_variation_coefficient_1 (mean, deviation):
    v_c_1 = deviation/mean
    print(f"Variation coefficient 1: {v_c_1}")
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