import numpy as np

def detect_anomalies(
    requests_per_minute,
    window=10,
    z_threshold=3,
    min_requests=20
):
    rolling_mean = requests_per_minute.rolling(window).mean().shift(1)
    rolling_std = requests_per_minute.rolling(window).std().shift(1)
    z_score = (
        (requests_per_minute - rolling_mean)
        / rolling_std.replace(0, np.nan)
    ).fillna(0)

    anomalies = (
        (z_score > z_threshold)
        & (requests_per_minute >= min_requests)
    )

    return rolling_mean, rolling_std, z_score, anomalies
