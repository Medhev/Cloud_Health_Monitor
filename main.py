import time
import logging
from src.collector import SystemCollector
from src.database import DatabaseManager
from src.alerter import AlertDispatcher


def main():
  # Configure enterprise-grade logging
  logging.basicConfig(
      level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
  )

  logging.info(
      "Initializing Enterprise Cloud Health & Telemetry Monitoring Daemon..."
  )

  # Instantiate modules
  collector = SystemCollector()
  db = DatabaseManager()
  alerter = AlertDispatcher()  # Instantiates the incident dispatcher

  logging.info(
      "Daemon successfully started. Entering continuous monitoring loop..."
  )

  try:
    # Running 3 simulated cycles for demonstration (you can change this to a `while True:` loop later)
    for cycle in range(1, 4):
      logging.info(f"--- Monitoring Cycle {cycle} Initiated ---")

      # 1. Collect OS and Network Telemetry (with threshold evaluation)
      telemetry_payload = collector.collect_all()
      logging.info(
          f"Telemetry Captured -> Status: {telemetry_payload.get('health_status')}"
          f" | CPU: {telemetry_payload.get('cpu_percent')}%"
      )

      # 2. Persist Payload securely to SQL Database
      db.save_metrics(telemetry_payload)

      # 3. Check and dispatch alerts if health is degraded (e.g., Warning/Critical)
      alerter.dispatch_alert(telemetry_payload)

      # 4. Sleep interval before the next health check cycle (e.g., 5 seconds)
      if cycle < 3:
        logging.info("Sleeping for 5 seconds before next check...\n")
        time.sleep(5)

    logging.info(
        "All metrics logged."
    )

  except KeyboardInterrupt:
    logging.warning("Daemon interrupted by user. Shutting down gracefully.")


if __name__ == "__main__":
  main()