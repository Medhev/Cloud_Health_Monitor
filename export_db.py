import csv
import sqlite3
from pathlib import Path

# 1. Connect to your database
db_path = Path(__file__).parent / "server_metrics.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 2. Fetch all health logs
cursor.execute("SELECT * FROM health_logs")
rows = cursor.fetchall()

# Extract column headers dynamically
column_names = [description[0] for description in cursor.description]

# 3. Write data directly to a clean CSV file
csv_filename = "server_metrics_export.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
  writer = csv.writer(csv_file)
  writer.writerow(column_names)  # Write headers
  writer.writerows(rows)  # Write all rows

conn.close()
print(f"Success! Database exported to {csv_filename}.")