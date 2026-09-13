"""Holiday Sensors integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN, PLATFORMS


def _remove_legacy_sensor_entities(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Remove sensor registry entries replaced by date and time entities."""
    registry = er.async_get(hass)
    for suffix in ("holiday_start", "holiday_stop", "holiday_time_home"):
        unique_id = f"{entry.entry_id}_{suffix}"
        entity_id = registry.async_get_entity_id(Platform.SENSOR, DOMAIN, unique_id)
        if entity_id is not None:
            registry.async_remove(entity_id)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Holiday Sensors from a config entry."""
    _remove_legacy_sensor_entities(hass, entry)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Holiday Sensors config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
