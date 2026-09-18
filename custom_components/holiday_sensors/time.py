"""Time platform for Holiday Sensors."""

from __future__ import annotations

from datetime import date, datetime, time

from homeassistant.components.time import TimeEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.event import async_track_time_change
from homeassistant.util import dt as dt_util

from .const import (
    ATTR_CUSTOM_UI_MORE_INFO,
    CONF_HOLIDAY_STOP,
    CONF_HOLIDAY_TIME_HOME,
    DOMAIN,
    MORE_INFO_ELEMENT,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Holiday Sensors time entity."""
    async_add_entities([HolidayTimeHome(entry)])


class HolidayTimeHome(TimeEntity):
    """Editable expected arrival time."""

    _attr_icon = "mdi:home-clock"
    _attr_name = "Holiday time home"
    _attr_should_poll = False

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the expected arrival time."""
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_holiday_time_home"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer="isimagan",
            model="Holiday Sensors",
            configuration_url="https://github.com/isimagan/HA-Holiday-sensors",
        )

    @property
    def native_value(self) -> time:
        """Return the expected arrival time."""
        return time.fromisoformat(self._entry.data[CONF_HOLIDAY_TIME_HOME])

    async def async_set_value(self, value: time) -> None:
        """Set the expected arrival time."""
        data = dict(self._entry.data)
        data[CONF_HOLIDAY_TIME_HOME] = value.isoformat()
        self.hass.config_entries.async_update_entry(self._entry, data=data)
        await self.hass.config_entries.async_reload(self._entry.entry_id)

    @property
    def extra_state_attributes(self) -> dict[str, str | bool]:
        """Return the combined local home date and frontend metadata."""
        stop = date.fromisoformat(self._entry.data[CONF_HOLIDAY_STOP])
        timezone = dt_util.get_time_zone(self.hass.config.time_zone)
        home_date = datetime.combine(stop, self.native_value, tzinfo=timezone)
        return {
            "homeDate": home_date.isoformat(),
            "homeToday": dt_util.now().date() == home_date.date(),
            ATTR_CUSTOM_UI_MORE_INFO: MORE_INFO_ELEMENT,
        }

    async def async_added_to_hass(self) -> None:
        """Refresh the date flag at local midnight."""
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
        """Write a fresh state when the local date changes."""
        self.async_write_ha_state()
