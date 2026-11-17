import pytest
from src.collector import SystemCollector


def test_system_collector_initialization():
  collector = SystemCollector()
  assert collector.config is not None
  assert isinstance(collector.config, dict)


def test_collect_all_structure():
  collector = SystemCollector()
  payload = collector.collect_all()

  # Verify all expected enterprise telemetry keys exist
  expected_keys = [
      "cpu_percent",
      "memory_percent",
      "disk_percent",
      "max_disk_gb",
      "dns_resolved",
      "network_reachable",
      "health_status",
  ]

  for key in expected_keys:
    assert key in payload, f"Missing expected telemetry key: {key}"

  # Verify data types and ranges
  assert isinstance(payload["cpu_percent"], float)
  assert 0.0 <= payload["memory_percent"] <= 100.0
  assert payload["health_status"] in ["HEALTHY", "WARNING", "CRITICAL"]