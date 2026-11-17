# ☁️ Enterprise Cloud Health & Telemetry Monitoring Daemon

![Cloud Monitor CI](https://github.com/Medhev/Cloud-Health-Monitor/actions/workflows/ci.yml/badge.svg?branch=main)
![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-teal.svg)

A lightweight, modular, enterprise-grade infrastructure monitoring daemon built in Python. Designed to collect real-time OS and network telemetry, evaluate health thresholds dynamically, persist logs securely via a relational data access layer, trigger automated webhooks (n8n/Slack), and expose live system health metrics over a high-performance **FastAPI** REST interface.

---

## 🏗️ Architectural Overview

This project adheres to a clean, decoupled **Domain-Driven Modular Architecture**, separating concerns across configuration, telemetry collection, persistent data storage, alerting, and API exposure.

```text
cloud_health_monitor/
├── .github/
│   └── workflows/
│       └── ci.yml             # Automated CI/CD pipeline (pytest & linter checks)
├── config/
│   └── thresholds.json        # Externalized alerting thresholds & operational limits
├── src/
│   ├── __init__.py
│   ├── collector.py           # OS (psutil) & Network/DNS telemetry collector
│   ├── database.py            # Secure SQLite Data Access Layer with context managers
│   ├── alerter.py             # Incident evaluation & webhook dispatch engine (n8n)
│   └── api.py                 # FastAPI REST server for live & historical queries
├── tests/
│   ├── __init__.py
│   └── test_collector.py      # Automated unit test suite (pytest)
├── export_db.py               # Utility script for exporting SQLite telemetry to CSV
├── main.py                    # Master orchestrator daemon loop
├── requirements.txt           # Explicit dependency manifest
└── README.md                  # Project documentation
```

## 🚀 Key Features

*   **Decoupled Telemetry Collection (`collector.py`)**: 
    *   Gathers live OS metrics (CPU usage, Virtual Memory, Disk I/O) and network health via `psutil` and socket-based DNS checks.
    *   Evaluates system state against externalized thresholds (`config/thresholds.json`) to compute real-time health statuses (HEALTHY, WARNING, CRITICAL).
*   **Secure Data Access Layer (`database.py`)**: 
    *   Implements robust SQLite persistence using parameterized SQL queries to entirely prevent SQL injection vulnerabilities.
    *   Utilizes Python context managers (`with` statements) to guarantee automatic connection teardown and transaction rollback safety.
*   **Incident Dispatcher (`alerter.py`)**: 
    *   Evaluates telemetry payloads for anomalies and dispatches automated webhook alerts (e.g., integrating with workflow automation tools like n8n or PagerDuty).
*   **High-Performance REST API (`api.py`)**: 
    *   Exposes clean endpoints (`/health/live` and `/health/history`) powered by FastAPI with automatic interactive Swagger UI documentation (`/docs`).
*   **Automated Testing & CI/CD (`ci.yml`)**: 
    *   Verified via `pytest` unit test suites and integrated into GitHub Actions continuous integration pipelines.

## ⚙️ Getting Started & Local Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Medhev/cloud_health_monitor.git
cd cloud_health_monitor
```

### 2. Set Up Virtual Environment 
#### for Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### for macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Unit Tests
Ensure path resolution is set to root:
```bash
PYTHONPATH=. pytest
```

## 🏃‍♂️ Usage & Execution

### Run the Monitoring Daemon
Execute the master orchestrator to initiate continuous monitoring cycles:
```bash
python main.py
```

### Launch the FastAPI REST Server
Start the high-performance ASGI server locally with auto-reload:

#### Windows (PowerShell)
```bash
$env:PYTHONPATH="."; uvicorn src.api:app --reload
```

#### macOS / Linux
```bash
PYTHONPATH=. uvicorn src.api:app --reload
```
Access the interactive API documentation in your browser at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 🛡️ Engineering Best Practices

*   **Zero Hardcoded Secrets/Configs**: Operational thresholds are strictly externalized into JSON configuration files.
*   **Defensive Programming**: Fault-tolerant file loading, graceful `KeyboardInterrupt` handling, and robust exception logging.
*   **Clean Git Workflow**: Structured semantic commit messages and automated pipeline checks.

## 👤 Author

**Medhev Raja S**  
*Aspiring Cloud & Infrastructure Engineer*