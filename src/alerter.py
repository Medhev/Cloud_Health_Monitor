import logging
import requests


class AlertDispatcher:

  def __init__(self, webhook_url=None):
    """Initializes the alert dispatcher with an optional webhook URL (e.g., n8n)."""
    self.webhook_url = webhook_url

  def dispatch_alert(self, telemetry_payload):
    """Evaluates telemetry status and dispatches an alert payload if an anomaly is detected."""
    status = telemetry_payload.get("health_status")

    if status in ["WARNING", "CRITICAL"]:
      alert_message = (
          f"[ALERT] System health degraded! Status: {status} | CPU:"
          f" {telemetry_payload.get('cpu_percent')}% | RAM:"
          f" {telemetry_payload.get('memory_percent')}%"
      )
      logging.warning(alert_message)

      # If a webhook URL (like n8n) is configured, dispatch the HTTP payload
      if self.webhook_url:
        try:
          response = requests.post(
              self.webhook_url, json=telemetry_payload, timeout=3
          )
          if response.status_code == 200:
            logging.info("Incident webhook successfully dispatched to n8n.")
          else:
            logging.error(f"Failed to dispatch webhook. Status: {response.status_code}")
        except Exception as e:
          logging.exception(f"Error connecting to webhook endpoint: {e}")
    else:
      logging.info("System operating within normal parameters. No alert triggered.")