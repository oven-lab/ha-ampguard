"""Constants for the Amp Guard integration."""

from datetime import timedelta

CONFIGURATION_URL = "https://my.charge.space"
DOMAIN = "ampguard"
DEFAULT_SCAN_INTERVAL = timedelta(seconds=5)
MANUFACTURER = "Charge Amps AB"
PLATFORMS = ["binary_sensor", "sensor"]
