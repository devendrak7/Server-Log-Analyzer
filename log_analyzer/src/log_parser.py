import re

LOG_PATTERN = re.compile(r'(?P<ip>\S+) - - \[(?P<timestamp>[^\]]+)\] 'r'"(?P<method>\S+) (?P<endpoint>\S+) HTTP/1\.1" 'r'(?P<status>\d{3}) (?P<size>\d+)')

def parse_log_line(line):
    match = LOG_PATTERN.match(line)
    if not match:
        return None
    return {
        "ip": match.group("ip"),
        "timestamp": match.group("timestamp"),
        "method": match.group("method"),
        "endpoint": match.group("endpoint"),
        "status": int(match.group("status")),
        "size": int(match.group("size")),
    }
