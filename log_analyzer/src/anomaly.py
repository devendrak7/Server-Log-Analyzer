import numpy as np


def detect_anomalies(
    requests_per_minute,
    window=10,
    z_threshold=3,
    min_requests=20
):
    # Calculate average requests from the previous minutes
    rolling_mean = requests_per_minute.rolling(window).mean().shift(1)

    # Calculate standard deviation from the previous minutes
    rolling_std = requests_per_minute.rolling(window).std().shift(1)

    # Calculate Z-score
    # If standard deviation is 0, replace it with NaN
    z_score = (
        (requests_per_minute - rolling_mean)
        / rolling_std.replace(0, np.nan)
    )

    # Missing Z-score values are replaced with 0
    z_score = z_score.fillna(0)

    # A request count is considered an anomaly when:
    # 1. Z-score is greater than the threshold
    # 2. Request count is at least the minimum required
    anomalies = (
        (z_score > z_threshold)
        & (requests_per_minute >= min_requests)
    )

    return rolling_mean, rolling_std, z_score, anomalies
