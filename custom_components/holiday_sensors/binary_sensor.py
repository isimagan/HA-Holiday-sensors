"""Binary sensor platform for Holiday Sensors."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.event import async_track_time_change
from homeassistant.util import dt as dt_util

from .const import CONF_HOLIDAY_START, CONF_HOLIDAY_STOP, DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the current-holiday binary sensor."""
    async_add_entities([HolidayNowBinarySensor(entry)])


class HolidayNowBinarySensor(BinarySensorEntity):
    """Whether today falls within the configured holiday period."""

    _attr_name = "Now"
    _attr_should_poll = False
    _attr_has_entity_name = True

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the holiday binary sensor."""
        self._entry = entry
        self.entity_id = "binary_sensor.holiday_sensor_now"
        self._attr_unique_id = f"{entry.entry_id}_holiday_now"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer="isimagan",
            model="Holiday Sensors",
            configuration_url="https://github.com/isimagan/HA-Holiday-sensors",
        )

    @property
    def _start(self) -> date:
        """Return the configured holiday start date."""
        return date.fromisoformat(self._entry.data[CONF_HOLIDAY_START])

    @property
    def _stop(self) -> date:
        """Return the configured holiday stop date."""
        return date.fromisoformat(self._entry.data[CONF_HOLIDAY_STOP])

    @property
    def _today(self) -> date:
        """Return today's date in Home Assistant's time zone."""
        return dt_util.now().date()

    @property
    def available(self) -> bool:
        """Return whether the holiday has not ended."""
        return self._today <= self._stop

    @property
    def is_on(self) -> bool:
        """Return whether the holiday is active."""
        return self._start <= self._today < self._stop

    @property
    def icon(self) -> str:
        """Return an icon matching the current state."""
        return "mdi:weather-sunny" if self.is_on else "mdi:weather-sunny-off"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return holiday counters and flags."""
        today = self._today
        start = self._start
        stop = self._stop
        return {
            "lastDay": today == stop,
            "dayNumber": (today - start).days,
            "daysLeft": (stop - today).days,
            "numberOfDays": (stop - start).days,
        }

    async def async_added_to_hass(self) -> None:
        """Update the state when the local date changes."""
        await super().async_added_to_hass()
        self.async_on_remove(
            async_track_time_change(
                self.hass,
                self._handle_midnight,
                hour=0,
                minute=0,
                second=0,
            )
        )

    @callback
    def _handle_midnight(self, now: datetime) -> None:
        """Write a fresh state at local midnight."""
        self.async_write_ha_state()
