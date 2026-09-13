import matplotlib.pyplot as plt

def plot_requests_over_time(requests_per_minute,anomalies,output_path):
    plt.figure(figsize=(12, 6))
    plt.plot( requests_per_minute.index, requests_per_minute.values,label="Requests per minute")
    plt.scatter(requests_per_minute.index[anomalies],requests_per_minute[anomalies],label="Anomaly")

    plt.xlabel("Time")
    plt.ylabel("Requests")
    plt.title("Requests Over Time")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_status_distribution(status_distribution, output_path):
    plt.figure(figsize=(8, 5))

    status_distribution.plot(kind="bar")

    plt.xlabel("HTTP Status")
    plt.ylabel("Requests")
    plt.title("HTTP Status Distribution")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_top_ips(top_ips, output_path):
    plt.figure(figsize=(10, 6))

    top_ips.sort_values().plot(kind="barh")

    plt.xlabel("Requests")
    plt.ylabel("IP Address")
    plt.title("Top 10 IPs")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_top_endpoints(top_endpoints, output_path):
    plt.figure(figsize=(10, 6))

    top_endpoints.sort_values().plot(kind="barh")

    plt.xlabel("Requests")
    plt.ylabel("Endpoint")
    plt.title("Top 10 Endpoints")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
