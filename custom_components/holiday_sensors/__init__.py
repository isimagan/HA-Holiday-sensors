"""Holiday Sensors integration."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "holiday_sensors"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up Holiday Sensors from YAML."""
    return True
