"""Sensor platform for Holiday Sensors."""

from __future__ import annotations

from datetime import date, datetime, time

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import (
    CONF_HOLIDAY_START,
    CONF_HOLIDAY_STOP,
    CONF_HOLIDAY_TIME_HOME,
    DOMAIN,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Holiday Sensors sensor entities."""
    async_add_entities(
        [
            HolidayStartSensor(entry),
            HolidayStopSensor(entry),
            HolidayTimeHomeSensor(hass, entry),
        ]
    )


class HolidaySensorEntity(SensorEntity):
    """Base class for Holiday Sensors sensors."""

    _attr_should_poll = False

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize a Holiday Sensors sensor."""
        self._entry = entry
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer="isimagan",
            model="Holiday Sensors",
            configuration_url="https://github.com/isimagan/HA-Holiday-sensors",
        )


class HolidayStartSensor(HolidaySensorEntity):
    """Holiday start date."""

    _attr_device_class = SensorDeviceClass.DATE
    _attr_icon = "mdi:weather-sunny"
    _attr_name = "Holiday start"

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the start-date sensor."""
        super().__init__(entry)
        self._attr_unique_id = f"{entry.entry_id}_holiday_start"

    @property
    def native_value(self) -> date:
        """Return the holiday start date."""
        return date.fromisoformat(self._entry.data[CONF_HOLIDAY_START])


class HolidayStopSensor(HolidaySensorEntity):
    """Holiday stop date."""

    _attr_device_class = SensorDeviceClass.DATE
    _attr_icon = "mdi:home"
    _attr_name = "Holiday stop"

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the stop-date sensor."""
        super().__init__(entry)
        self._attr_unique_id = f"{entry.entry_id}_holiday_stop"

    @property
    def native_value(self) -> date:
        """Return the holiday stop date."""
        return date.fromisoformat(self._entry.data[CONF_HOLIDAY_STOP])


class HolidayTimeHomeSensor(HolidaySensorEntity):
    """Expected time of arrival home."""

    _attr_icon = "mdi:home-clock"
    _attr_name = "Holiday time home"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the arrival-time sensor."""
        super().__init__(entry)
        self._hass = hass
        self._attr_unique_id = f"{entry.entry_id}_holiday_time_home"

    @property
    def native_value(self) -> str:
        """Return the expected time of arrival."""
        return self._entry.data[CONF_HOLIDAY_TIME_HOME]

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return the combined local home date and time."""
        stop = date.fromisoformat(self._entry.data[CONF_HOLIDAY_STOP])
        arrival = time.fromisoformat(self._entry.data[CONF_HOLIDAY_TIME_HOME])
        timezone = dt_util.get_time_zone(self._hass.config.time_zone)
        home_date = datetime.combine(stop, arrival, tzinfo=timezone)
        return {"homeDate": home_date.isoformat()}
