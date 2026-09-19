"""Holiday Sensors integration."""

from pathlib import Path
from typing import Any

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import entity_registry as er

from .const import (
    DOMAIN,
    FRONTEND_MODULE_URL,
    FRONTEND_STATIC_URL,
    PLATFORMS,
)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Set up the Holiday Sensors frontend module."""
    frontend_path = Path(__file__).parent / "frontend"
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                FRONTEND_STATIC_URL,
                str(frontend_path / "holiday-time-more-info.js"),
                True,
            )
        ]
    )
    add_extra_js_url(hass, FRONTEND_MODULE_URL)
    return True


def _remove_legacy_sensor_entities(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Remove sensor registry entries replaced by date and time entities."""
    registry = er.async_get(hass)
    for suffix in ("holiday_start", "holiday_stop", "holiday_time_home"):
        unique_id = f"{entry.entry_id}_{suffix}"
        entity_id = registry.async_get_entity_id(Platform.SENSOR, DOMAIN, unique_id)
        if entity_id is not None:
            registry.async_remove(entity_id)


def _rename_default_entity_ids(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Shorten known default IDs while preserving custom IDs and collisions."""
    registry = er.async_get(hass)
    for platform, suffix in (
        (Platform.DATE, "start"),
        (Platform.DATE, "stop"),
        (Platform.TIME, "time_home"),
        (Platform.BINARY_SENSOR, "now"),
    ):
        unique_id = f"{entry.entry_id}_holiday_{suffix}"
        entity_id = registry.async_get_entity_id(platform, DOMAIN, unique_id)
        old_ids = {
            f"{platform}.holiday_{suffix}",
            f"{platform}.holiday_sensor_holiday_{suffix}",
            f"{platform}.holiday_sensors_holiday_{suffix}",
        }
        if entity_id not in old_ids:
            continue
        new_entity_id = f"{platform}.holiday_sensor_{suffix}"
        if registry.async_get(new_entity_id) is None and hass.states.get(new_entity_id) is None:
            registry.async_update_entity(entity_id, new_entity_id=new_entity_id)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Holiday Sensors from a config entry."""
    _remove_legacy_sensor_entities(hass, entry)
    _rename_default_entity_ids(hass, entry)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Holiday Sensors config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
