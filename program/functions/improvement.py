def power_2_3_pdf(histogram, g_min, g_max, f, N):
    """
    Compute the Power 2/3 final probability density function for a given pixel intensity f.
    """
    # Confirm histogram is a list
    if not isinstance(histogram, list):
        raise ValueError("Expected histogram to be a list of values")

    # Compute cumulative histogram sum up to f
    cumulative_sum = sum(histogram[:f + 1])  # Sum H(m) from 0 to f

    # Normalize by dividing by N (total number of pixels)
    normalized_cumulative_sum = cumulative_sum / N

    # Cube roots of g_min and g_max
    g_min_13 = g_min ** (1 / 3)
    g_max_13 = g_max ** (1 / 3)

    # Compute final value of g(f) using the formula
    g_f = (g_min_13 + (g_max_13 - g_min_13) * normalized_cumulative_sum) ** 3
    return g_f
