import pandas as pd

def calculate_statistics(df):
    if df.empty:
        return {
            "total_requests": 0,
            "unique_ips": 0,
            "top_ips": pd.Series(dtype=int),
            "top_endpoints": pd.Series(dtype=int),
            "status_distribution": pd.Series(dtype=int),
            "error_count": 0,
            "error_rate": 0,
            "requests_per_minute": pd.Series(dtype=int),
        }

    # Total number of requests
    total_requests = len(df)

    # Number of unique IP addresses
    unique_ips = df["ip"].nunique()

    # Top 10 IP addresses
    top_ips = df["ip"].value_counts().head(10)

    # Top 10 requested endpoints
    top_endpoints = df["endpoint"].value_counts().head(10)

    # Count of each HTTP status code
    status_distribution = df["status"].value_counts().sort_index()

    # Count requests with status code 400 or above
    error_count = (df["status"] >= 400).sum()

    # Calculate error percentage
    error_rate = (error_count / total_requests) * 100

    # Count requests for every minute
    requests_per_minute = df.resample("1min").size()

    statistics = {
        "total_requests": total_requests,
        "unique_ips": unique_ips,
        "top_ips": top_ips,
        "top_endpoints": top_endpoints,
        "status_distribution": status_distribution,
        "error_count": error_count,
        "error_rate": error_rate,
        "requests_per_minute": requests_per_minute,
    }

    return statistics
