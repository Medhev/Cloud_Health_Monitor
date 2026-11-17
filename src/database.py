import logging
import sqlite3
from datetime import datetime
from pathlib import Path


class DatabaseManager:

  def __init__(self, db_path=None):
    """Initializes the database connection path and ensures tables exist."""
    if db_path is None:
      self.db_path = Path(__file__).parent.parent / "server_metrics.db"
    else:
      self.db_path = db_path

    self._initialize_database()

  def _initialize_database(self):
    """Creates the health_logs table if it does not already exist."""
    with sqlite3.connect(self.db_path) as conn:
        cursor = conn.cursor()

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS health_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    cpu_percent REAL,
                    memory_percent REAL,
                    disk_percent REAL,
                    max_disk_gb REAL,
                    dns_resolved INTEGER,
                    network_reachable INTEGER,
                    health_status TEXT
                )
            """)

  def save_metrics(self, telemetry_data):
    """Saves a telemetry payload securely using parameterized SQL statements."""
    with sqlite3.connect(self.db_path) as conn:
        cursor = conn.cursor()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            """
            INSERT INTO health_logs (
                timestamp, cpu_percent, memory_percent, disk_percent, 
                max_disk_gb, dns_resolved, network_reachable, health_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                timestamp,
                telemetry_data.get("cpu_percent"),
                telemetry_data.get("memory_percent"),
                telemetry_data.get("disk_percent"),
                telemetry_data.get("max_disk_gb"),
                1 if telemetry_data.get("dns_resolved") else 0,
                1 if telemetry_data.get("network_reachable") else 0,
                telemetry_data.get("health_status"),
            ),
        )
    logging.info("Metrics successfully persisted to database.")


if __name__ == "__main__":
  db = DatabaseManager()
  
  logging.basicConfig(
      level = logging.WARNING, format = "%(asctime)s [%(levelname)s] %(message)s"
    )
  
  sample_payload = {
      "cpu_percent": 15.5,
      "memory_percent": 45.2,
      "disk_percent": 12.0,
      "max_disk_gb": 10,
      "dns_resolved": True,
      "network_reachable": True,
      "health_status": "HEALTHY",
  }
  db.save_metrics(sample_payload)