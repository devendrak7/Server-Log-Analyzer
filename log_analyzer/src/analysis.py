import pandas as pd

def calculate_statistics(df):
    total_requests = len(df)
    unique_ips = df["ip"].nunique()

    top_ips = df["ip"].value_counts().head(10)
    top_endpoints = df["endpoint"].value_counts().head(10)

    status_distribution = df["status"].value_counts().sort_index()

    error_count = (df["status"] >= 400).sum()
    error_rate = (error_count / total_requests) * 100

    requests_per_minute = df.resample("1min").size()

    return {
        "total_requests": total_requests,
        "unique_ips": unique_ips,
        "top_ips": top_ips,
        "top_endpoints": top_endpoints,
        "status_distribution": status_distribution,
        "error_count": error_count,
        "error_rate": error_rate,
        "requests_per_minute": requests_per_minute,
    }
