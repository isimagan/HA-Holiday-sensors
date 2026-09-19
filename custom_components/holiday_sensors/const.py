"""Constants for the Holiday Sensors integration."""

from datetime import time

from homeassistant.const import Platform

DOMAIN = "holiday_sensors"

ATTR_CUSTOM_UI_MORE_INFO = "custom_ui_more_info"

CONF_HOLIDAY_START = "holiday_start"
CONF_HOLIDAY_STOP = "holiday_stop"
CONF_HOLIDAY_TIME_HOME = "holiday_time_home"

DEFAULT_TIME_HOME = time(12, 0).isoformat()

FRONTEND_MODULE_URL = (
    "/api/holiday_sensors/holiday-time-more-info.js?rev=3"
)
FRONTEND_STATIC_URL = "/api/holiday_sensors/holiday-time-more-info.js"
MORE_INFO_ELEMENT = "holiday-time-more-info"

PLATFORMS = [Platform.BINARY_SENSOR, Platform.DATE, Platform.TIME]
