def generate_log():
    # existing generation logic
    import random
    from datetime import datetime, timedelta
    OUTPUT_FILE = "data/sample_access.log"
    TOTAL_REQUESTS = 10000

    START_TIME = datetime(2026, 9, 13, 10, 0, 0)

    IPS = ["192.168.1.10","192.168.1.20","192.168.1.30","192.168.1.40","192.168.1.50",]

    ENDPOINTS = ["/","/login","/products","/api/users","/api/orders","/about",]

    METHODS = ["GET", "GET", "GET", "POST"]

    NORMAL_STATUSES = [200, 200, 200, 201, 301, 404]
    ERROR_STATUSES = [500, 502, 503]

    SPIKE_MINUTES = {100, 250, 400, 500}
    ERROR_BURST_MINUTES = {180, 350}

    SUSPICIOUS_IPS = ["10.0.0.99","10.0.0.100",]
    def create_log_line(ip, timestamp, method, endpoint, status, size):
        timestamp_str = timestamp.strftime("%d/%b/%Y:%H:%M:%S +0530")
        return (f'{ip} - - [{timestamp_str}] 'f'"{method} {endpoint} HTTP/1.1" 'f'{status} {size} "-" "Mozilla/5.0"')

    logs = []

    current_time = START_TIME

    for minute in range(800):
        if minute in SPIKE_MINUTES:
            requests_this_minute = random.randint(100, 150)
        elif minute in ERROR_BURST_MINUTES:
            requests_this_minute = random.randint(10, 20)
        else:
            requests_this_minute = random.randint(5, 15)
        for _ in range(requests_this_minute):
            timestamp = current_time + timedelta(seconds=random.randint(0, 59))
            if minute in SPIKE_MINUTES:
                ip = random.choice(SUSPICIOUS_IPS)
            else:
                ip = random.choice(IPS)
            method = random.choice(METHODS)
            endpoint = random.choice(ENDPOINTS)
            if minute in ERROR_BURST_MINUTES:
                status = random.choice(ERROR_STATUSES)
            else:
                status = random.choice(NORMAL_STATUSES)
            size = random.randint(200, 5000)
            logs.append(
                create_log_line(
                    ip, timestamp, method, endpoint, status, size
                )
            )

        current_time += timedelta(minutes=1)

    random.shuffle(logs)

    malformed_count = int(len(logs) * 0.03)

    malformed_lines = [
        "this is a malformed log line",
        "192.168.1.10 invalid data",
        "BROKEN LOG ENTRY",
    ]
    for i in range(malformed_count):
        logs[i] = random.choice(malformed_lines)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        for log in logs:
            file.write(log + "\n")

    print(f"Generated {len(logs)} log lines.")
    print(f"Malformed lines: {malformed_count}")
    print(f"Saved to: {OUTPUT_FILE}")
