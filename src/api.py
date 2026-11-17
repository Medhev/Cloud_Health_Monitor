from fastapi import FastAPI
from src.collector import SystemCollector
from src.database import DatabaseManager

app = FastAPI(
    title="Cloud Health Monitoring API",
    version="1.0.0",
    description=(
        "Enterprise infrastructure telemetry and health monitoring REST API."
    ),
)

collector = SystemCollector()
db = DatabaseManager()


@app.get("/")
def read_root():
  """Root endpoint confirming API operational status."""
  return {
      "status": "online",
      "service": "Cloud Health & Telemetry Daemon",
  }


@app.get("/health/live")
def get_live_telemetry():
  """Fetches real-time OS and network telemetry on-demand."""
  return collector.collect_all()


@app.get("/health/history")
def get_historical_logs(limit: int = 5):
  """Queries recent historical health logs from the SQLite database."""
  # We use our DatabaseManager connection to fetch recent logs
  import sqlite3

  with sqlite3.connect(db.db_path) as conn:
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM health_logs ORDER BY id DESC LIMIT ?", (limit,)
      )
    rows = [dict(row) for row in cursor.fetchall()]

  return {"recent_logs_count": len(rows), "logs": rows}