"""Constants for the Holiday Sensors integration."""

from datetime import time

DOMAIN = "holiday_sensors"

CONF_HOLIDAY_START = "holiday_start"
CONF_HOLIDAY_STOP = "holiday_stop"
CONF_HOLIDAY_TIME_HOME = "holiday_time_home"

DEFAULT_TIME_HOME = time(12, 0).isoformat()
PLATFORMS = ["binary_sensor", "sensor"]
