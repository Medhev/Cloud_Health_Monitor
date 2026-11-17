import json
import os
from pathlib import Path
import platform
import socket
import subprocess
import psutil
import logging


class SystemCollector:

  def __init__(self, config_path=None):

    if config_path is None:
      config_path = Path(__file__).parent.parent / "config" / "thresholds.json"
    self.config = self._load_config(config_path)

  def _load_config(self, config_path):

    try:
      with open(config_path, "r", encoding="utf-8") as file:
        logging.debug(
          "config file found\n"
          "retrieving information...")
        return json.load(file)
    except FileNotFoundError:
      logging.warning(
          f"Config file not found at {config_path}. Using safe"
          " default configurations."
      )
      return {
          "cpu_threshold_percent": 80.0,
          "memory_threshold_percent": 85.0,
          "disk_threshold_percent": 90.0,
          "max_disk": 10,
          "monitored_endpoint": "1.1.1.1", # NOSONAR
          "dns_test_domain": "google.com"
      }

  def get_os_metrics(self):

    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    max_disk = self.config.get("max_disk", 10)
    
    logging.debug("OS metrics receiving...")

    return {
        "cpu_percent": cpu_percent,
        "memory_percent": memory.percent,
        "disk_percent": disk.percent,
        "max_disk_gb": max_disk
    }

  def check_network_connectivity(self):

    host = os.getenv("MONITORED_ENDPOINT") or self.config["monitored_endpoint"]
    domain = os.getenv("DNS_TEST_DOMAIN") or self.config["dns_test_domain"]

    # 1. DNS Resolution Check
    dns_status = True
    try:
      socket.gethostbyname(domain)
    except socket.gaierror:
      dns_status = False
    logging.debug("DNS resolved")

    # 2. Host Reachability Check
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]

    network_reachable = False
    try:
      output = subprocess.run(
          command, capture_output=True, text=True, timeout=2, check=False
      )
      if output.returncode == 0:
        logging.debug("Network checked")
        network_reachable = True
    except Exception:
      network_reachable = False

    return {"dns_resolved": dns_status, "network_reachable": network_reachable}

  def collect_all(self):

    os_metrics = self.get_os_metrics()
    network_metrics = self.check_network_connectivity()
    cpu_limit = self.config.get("cpu_threshold_percent")
    current_cpu = os_metrics["cpu_percent"]
    
    if(current_cpu > cpu_limit):
      health_status = "CRITICAL"
    elif(current_cpu == cpu_limit):
      health_status = "WARNING"
    else:
      health_status = "HEALTHY"
    logging.debug("Metrics collected.")
    return {**os_metrics, **network_metrics, "health_status": health_status}


if __name__ == "__main__":
  
  logging.basicConfig(
    level = logging.WARNING, format = "%(asctime)s [%(levelname)s] %(message)s"
  )
  
  collector = SystemCollector()
  print("Telemetry Payload Preview:", collector.collect_all())