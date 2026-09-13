# Server Log Analyzer & Anomaly Dashboard

A Python-based CLI project for analyzing Apache/Nginx-style access logs, identifying unusual traffic patterns, and generating statistical and visual reports.

## Overview

The **Server Log Analyzer & Anomaly Dashboard** takes raw server access logs and processes them through a complete data-analysis pipeline:

```text
Raw Access Logs
      │
      ▼
Regex Parsing
      │
      ▼
Data Cleaning
      │
      ▼
Pandas DataFrame
      │
      ▼
Statistical Analysis
      │
      ▼
Requests Per Minute
      │
      ▼
Rolling Z-Score Anomaly Detection
      │
      ▼
Charts + Terminal Summary + Anomaly Report
```

The project is designed as a **CLI/batch data-analysis project** and focuses on practical usage of Python's data-processing and visualization libraries.

---

## Features

### Log Parsing
- Parses Apache/Nginx-style access logs using Python `re`
- Extracts:
  - IP address
  - Timestamp
  - HTTP method
  - Endpoint
  - HTTP status code
  - Response size
- Safely skips malformed log lines

### Data Analysis
Calculates:
- Total requests
- Unique IPs
- Top 10 IPs
- Top 10 endpoints
- HTTP status-code distribution
- Error count
- Error rate
- Requests per minute

### Anomaly Detection
Detects unusual traffic spikes using:
- Rolling mean
- Rolling standard deviation
- Z-score
- Minimum request threshold

### Visualization
Generates four charts:
1. Requests over time with anomalies
2. HTTP status-code distribution
3. Top 10 IPs
4. Top 10 endpoints

### Reporting
- Terminal summary
- `anomaly_report.txt` containing detected anomalies

---

## Tech Stack

| Library | Purpose |
|---|---|
| Python | Core programming language |
| `re` | Regular-expression based log parsing |
| `pandas` | Data cleaning, grouping and time-series analysis |
| `numpy` | Numerical calculations |
| `matplotlib` | Data visualization |

No external web framework, database, ML framework, or dashboard framework is required for V1.

---

## Project Structure

```text
log_analyzer/
│
├── data/
│   └── sample_access.log
│
├── src/
│   ├── log_parser.py
│   ├── data_cleaner.py
│   ├── analysis.py
│   ├── anomaly.py
│   ├── visualize.py
│   └── main.py
│
├── output/
│   ├── charts/
│   └── anomaly_report.txt
│
├── generate_sample_log.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## How It Works

### 1. Generate Synthetic Logs

The project includes a synthetic log generator that creates Apache/Nginx-style access logs.

The generated dataset contains:
- Normal traffic
- Traffic spikes
- Error bursts
- High-frequency/suspicious IP activity
- Malformed log lines

Run:

```bash
python generate_sample_log.py
```

This generates:

```text
data/sample_access.log
```

---

### 2. Parse the Logs

`src/log_parser.py` uses a regular expression to extract useful fields from each log line.

Malformed lines return `None` instead of crashing the program.

The valid records are stored as dictionaries:

```text
[
    {
        "ip": "...",
        "timestamp": "...",
        "method": "GET",
        "endpoint": "/api/users",
        "status": 200,
        "size": 1234
    }
]
```

---

### 3. Create the DataFrame

`src/data_cleaner.py` converts the parsed records into a Pandas DataFrame.

The timestamp is converted into a proper datetime value and used as the DataFrame index.

This allows Pandas time-series operations such as:

```python
df.resample("1min").size()
```

---

### 4. Calculate Statistics

`src/analysis.py` calculates the main server statistics.

Examples:

```python
df["ip"].nunique()
```

finds the number of unique IPs.

```python
df["endpoint"].value_counts().head(10)
```

finds the most frequently requested endpoints.

```python
df.resample("1min").size()
```

calculates the number of requests received each minute.

---

## Anomaly Detection

The project uses a **rolling z-score** approach.

Instead of comparing every minute against one global average, the analyzer compares the current traffic with its recent history.

Conceptually:

```text
z = (current_value - rolling_mean) / rolling_std
```

An anomaly is flagged when:

```text
z-score > 3
AND
requests per minute >= minimum threshold
```

### Why Rolling Statistics?

Server traffic can naturally change over time.

For example:

```text
Morning   → Low traffic
Afternoon → Medium traffic
Evening   → High traffic
```

A rolling baseline adapts to these changes better than a single global mean.

### Why Shift the Rolling Statistics?

The current observation is excluded from its own baseline.

Otherwise, a large traffic spike can increase its own rolling mean and standard deviation, making the spike appear less unusual.

### Why Use a Minimum Request Threshold?

A very quiet period can produce a high z-score because of a small standard deviation.

The minimum request threshold reduces these false positives.

---

## Generated Output

### Charts

Four PNG files are generated inside:

```text
output/charts/
```

```text
requests_over_time.png
status_distribution.png
top_ips.png
top_endpoints.png
```

### Anomaly Report

Detected anomalies are saved to:

```text
output/anomaly_report.txt
```

Example:

```text
===== Anomaly Report =====

Timestamp : 2026-09-13 11:40:00+05:30
Requests  : 135
Z-score   : 32.21

Timestamp : 2026-09-13 14:10:00+05:30
Requests  : 133
Z-score   : 33.86

Total anomalies: 4
```

---

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
```

Move into the project directory:

```bash
cd log_analyzer
```

Create a virtual environment:

```bash
python -m venv .venv
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

### Step 1 — Generate Logs

```bash
python generate_sample_log.py
```

### Step 2 — Run the Analyzer

From the project root:

```bash
python -m src.main
```

---

## Example Terminal Output

```text
===== Server Log Analyzer =====
Total requests : 8359
Unique IPs     : 7
Error rate     : 16.99%
Malformed lines: 258
Anomalies      : 4
===============================
```

---

## Learning Outcomes

This project provides practical experience with:

- Python modules and functions
- Regular expressions
- File handling
- Pandas DataFrames
- Pandas `groupby`
- Pandas `value_counts`
- Pandas `resample`
- Pandas `rolling`
- NumPy numerical operations
- Statistical anomaly detection
- Matplotlib visualization
- CLI/batch data-processing workflows

---

## V1 Scope

The first version intentionally focuses on a simple and understandable data-analysis pipeline.

### Included in V1

- Synthetic log generation
- Regex-based parsing
- Malformed-line handling
- Pandas DataFrame creation
- Server statistics
- Per-minute request analysis
- Rolling z-score anomaly detection
- Four visualizations
- Terminal summary
- Anomaly report

### Not Included in V1

- Web dashboard
- Database
- REST API
- Live log monitoring
- Machine-learning anomaly detection
- GeoIP analysis
- Docker deployment

---

## Future Improvements

After V1, the project could be extended with:

- FastAPI-based API
- Live log monitoring
- Database storage
- Web dashboard
- Machine-learning anomaly detection
- GeoIP-based analysis
- Docker deployment

These improvements are intentionally kept outside the V1 scope.

---

## Author

**Devendra Kumawat**

Built as a practical Python data-analysis project focused on understanding the complete workflow from raw server logs to anomaly detection and visualization.
