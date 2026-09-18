"""Date platform for Holiday Sensors."""

from __future__ import annotations

from datetime import date, timedelta

from homeassistant.components.date import DateEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_HOLIDAY_START, CONF_HOLIDAY_STOP, DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Holiday Sensors date entities."""
    async_add_entities(
        [
            HolidayStartDate(entry),
            HolidayStopDate(entry),
        ]
    )


class HolidayDateEntity(DateEntity):
    """Base class for Holiday Sensors date entities."""

    _attr_should_poll = False

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize a Holiday Sensors date entity."""
        self._entry = entry
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer="isimagan",
            model="Holiday Sensors",
            configuration_url="https://github.com/isimagan/HA-Holiday-sensors",
        )

    async def _async_store_value(self, key: str, value: date) -> None:
        """Store a date and reload all related entities."""
        data = dict(self._entry.data)
        data[key] = value.isoformat()
        if key == CONF_HOLIDAY_START:
            stop = date.fromisoformat(data[CONF_HOLIDAY_STOP])
            if stop <= value:
                data[CONF_HOLIDAY_STOP] = (value + timedelta(days=1)).isoformat()
        self.hass.config_entries.async_update_entry(self._entry, data=data)
        await self.hass.config_entries.async_reload(self._entry.entry_id)


class HolidayStartDate(HolidayDateEntity):
    """Editable holiday start date."""

    _attr_icon = "mdi:weather-sunny"
    _attr_name = "Holiday start"

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the holiday start date."""
        super().__init__(entry)
        self._attr_unique_id = f"{entry.entry_id}_holiday_start"

    @property
    def native_value(self) -> date:
        """Return the holiday start date."""
        return date.fromisoformat(self._entry.data[CONF_HOLIDAY_START])

    async def async_set_value(self, value: date) -> None:
        """Set departure, moving the home date forward when needed."""
        await self._async_store_value(CONF_HOLIDAY_START, value)


class HolidayStopDate(HolidayDateEntity):
    """Editable holiday stop date."""

    _attr_icon = "mdi:home"
    _attr_name = "Holiday stop"

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the holiday stop date."""
        super().__init__(entry)
        self._attr_unique_id = f"{entry.entry_id}_holiday_stop"

    @property
    def native_value(self) -> date:
        """Return the holiday stop date."""
        return date.fromisoformat(self._entry.data[CONF_HOLIDAY_STOP])

    async def async_set_value(self, value: date) -> None:
        """Set the holiday stop date."""
        start = date.fromisoformat(self._entry.data[CONF_HOLIDAY_START])
        if value <= start:
            raise HomeAssistantError("Holiday stop must be after holiday start")
        await self._async_store_value(CONF_HOLIDAY_STOP, value)
