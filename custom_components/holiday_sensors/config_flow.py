"""Config flow for Holiday Sensors."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.selector import DateSelector, TimeSelector
from homeassistant.util import dt as dt_util

from .const import (
    CONF_HOLIDAY_START,
    CONF_HOLIDAY_STOP,
    CONF_HOLIDAY_TIME_HOME,
    DEFAULT_TIME_HOME,
    DOMAIN,
)


def _default_values() -> dict[str, str]:
    """Return defaults relative to the Home Assistant local date."""
    today = dt_util.now().date()
    return {
        CONF_HOLIDAY_START: (today - timedelta(days=2)).isoformat(),
        CONF_HOLIDAY_STOP: (today - timedelta(days=1)).isoformat(),
        CONF_HOLIDAY_TIME_HOME: DEFAULT_TIME_HOME,
    }


def _schema(defaults: dict[str, Any]) -> vol.Schema:
    """Build the setup form schema."""
    return vol.Schema(
        {
            vol.Required(
                CONF_HOLIDAY_START, default=defaults[CONF_HOLIDAY_START]
            ): DateSelector(),
            vol.Required(
                CONF_HOLIDAY_STOP, default=defaults[CONF_HOLIDAY_STOP]
            ): DateSelector(),
            vol.Required(
                CONF_HOLIDAY_TIME_HOME, default=defaults[CONF_HOLIDAY_TIME_HOME]
            ): TimeSelector(),
        }
    )


def _normalized_input(user_input: dict[str, Any]) -> dict[str, str]:
    """Normalize selector values for config-entry storage."""
    return {
        CONF_HOLIDAY_START: str(user_input[CONF_HOLIDAY_START]),
        CONF_HOLIDAY_STOP: str(user_input[CONF_HOLIDAY_STOP]),
        CONF_HOLIDAY_TIME_HOME: str(user_input[CONF_HOLIDAY_TIME_HOME]),
    }


def _dates_are_valid(values: dict[str, str]) -> bool:
    """Return whether the stop date is after the start date."""
    start = date.fromisoformat(values[CONF_HOLIDAY_START])
    stop = date.fromisoformat(values[CONF_HOLIDAY_STOP])
    return stop > start


class HolidaySensorsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Holiday Sensors."""

    VERSION = 1
    MINOR_VERSION = 0

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle initial setup."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        errors: dict[str, str] = {}
        values = _default_values()

        if user_input is not None:
            values = _normalized_input(user_input)
            if _dates_are_valid(values):
                return self.async_create_entry(title="Holiday Sensors", data=values)
            errors["base"] = "stop_not_after_start"

        return self.async_show_form(
            step_id="user",
            data_schema=_schema(values),
            errors=errors,
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Allow the holiday dates and home time to be changed."""
        entry = self._get_reconfigure_entry()
        errors: dict[str, str] = {}
        values = dict(entry.data)

        if user_input is not None:
            values = _normalized_input(user_input)
            if _dates_are_valid(values):
                return self.async_update_reload_and_abort(
                    entry,
                    data_updates=values,
                )
            errors["base"] = "stop_not_after_start"

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=_schema(values),
            errors=errors,
        )
