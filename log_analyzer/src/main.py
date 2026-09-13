import os
from generate_sample_log import generate_log
from src.log_parser import parse_log_line
from src.data_cleaner import create_dataframe
from src.analysis import calculate_statistics
from src.anomaly import detect_anomalies
from src.visualize import (
    plot_requests_over_time,
    plot_status_distribution,
    plot_top_ips,
    plot_top_endpoints,
)
generate_log()

LOG_FILE = "data/sample_access.log"
CHARTS_DIR = "output/charts"
REPORT_FILE = "output/anomaly_report.txt"


def load_logs(file_path):
    parsed_logs = []
    malformed_count = 0

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            parsed_line = parse_log_line(line.strip())

            if parsed_line is None:
                malformed_count += 1
            else:
                parsed_logs.append(parsed_line)

    return parsed_logs, malformed_count


def main():
    os.makedirs(CHARTS_DIR, exist_ok=True)

    parsed_logs, malformed_count = load_logs(LOG_FILE)

    df = create_dataframe(parsed_logs)

    statistics = calculate_statistics(df)

    _, _, z_scores, anomalies = detect_anomalies(statistics["requests_per_minute"])
    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        file.write("===== Anomaly Report =====\n\n")

        for timestamp in statistics["requests_per_minute"].index[anomalies]:
            request_count = statistics["requests_per_minute"].loc[timestamp]
            z_score = z_scores.loc[timestamp]

            file.write(f"Timestamp : {timestamp}\n")
            file.write(f"Requests  : {request_count}\n")
            file.write(f"Z-score   : {z_score:.2f}\n")
            file.write("\n")

        file.write(f"Total anomalies: {anomalies.sum()}\n")

    plot_requests_over_time(
        statistics["requests_per_minute"],
        anomalies,
        f"{CHARTS_DIR}/requests_over_time.png",
    )

    plot_status_distribution(
        statistics["status_distribution"],
        f"{CHARTS_DIR}/status_distribution.png",
    )

    plot_top_ips(
        statistics["top_ips"],
        f"{CHARTS_DIR}/top_ips.png",
    )

    plot_top_endpoints(
        statistics["top_endpoints"],
        f"{CHARTS_DIR}/top_endpoints.png",
    )

    print("\n===== Server Log Analyzer =====")
    print(f"Total requests : {statistics['total_requests']}")
    print(f"Unique IPs     : {statistics['unique_ips']}")
    print(f"Error rate     : {statistics['error_rate']:.2f}%")
    print(f"Malformed lines: {malformed_count}")
    print(f"Anomalies      : {anomalies.sum()}")
    print("===============================\n")


if __name__ == "__main__":
    main()
