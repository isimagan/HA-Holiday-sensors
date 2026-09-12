# Holiday Sensors for Home Assistant

Holiday Sensors is a planned Home Assistant helper integration for keeping track of a holiday period, the journey home, and useful day counters for automations.

> [!IMPORTANT]
> The repository currently contains the HACS-compatible project scaffold. The holiday entities described below are not implemented yet.

## Planned entities

- `sensor.holiday_start`: first day of the holiday
- `sensor.holiday_stop`: day of the journey home
- `sensor.holiday_time_home`: expected arrival time
- `binary_sensor.holiday_now`: whether the holiday is currently active

The detailed design and example automations are available in the [plan directory](plan/).

## Installation with HACS

Until the repository is included in the default HACS catalogue:

1. Open HACS in Home Assistant.
2. Open the menu and choose **Custom repositories**.
3. Add `https://github.com/isimagan/HA-Holiday-sensors`.
4. Select **Integration** as the category.
5. Download **Holiday Sensors** and restart Home Assistant.

The integration files are installed from `custom_components/holiday_sensors`.

## Development status

The repository structure, manifests, and automated HACS/Home Assistant validation are in place. Entity implementation and a configuration flow are the next development steps.
