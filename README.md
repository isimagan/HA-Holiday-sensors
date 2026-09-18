# Holiday Sensors for Home Assistant

Holiday Sensors is a Home Assistant integration for keeping track of a holiday period, the journey home, and useful day counters for automations.

## Entities

The integration creates:

- `date.holiday_sensor_start`: editable first day of the holiday
- `date.holiday_sensor_stop`: editable day of the journey home
- `time.holiday_sensor_time_home`: editable expected arrival time, with `homeDate` containing the home date and time as an ISO timestamp
- `binary_sensor.holiday_sensor_now`: on from the start date up to, but not including, the home date; unavailable after the home date

The time entity also provides `homeToday`, which is true when the local date matches the date portion of `homeDate` and updates at local midnight.

The more-info dialog for `time.holiday_sensor_time_home` displays the localized home date below the time control.

`binary_sensor.holiday_sensor_now` provides these attributes:

- `lastDay`: whether today is the home date
- `dayNumber`: whole days since the start date; the start date is day 0
- `daysLeft`: whole days until the home date
- `numberOfDays`: the difference in whole days between the start and home dates

For a holiday starting Friday with a home date on Sunday, `dayNumber` is 0 on Friday, 1 on Saturday, and 2 on Sunday. `numberOfDays` is 2.

The detailed design and example automations are available in the [plan directory](plan/).

## Installation with HACS

Until the repository is included in the default HACS catalogue:

1. Open HACS in Home Assistant.
2. Open the menu and choose **Custom repositories**.
3. Add `https://github.com/isimagan/HA-Holiday-sensors`.
4. Select **Integration** as the category.
5. Download **Holiday Sensors** and restart Home Assistant.
6. Go to **Settings → Devices & services → Add integration** and select **Holiday Sensors**.

## Configuration

During setup, choose:

- Departure date
- Home date
- Expected arrival time

The initial defaults are two days before today, one day before today, and `12:00:00`. The three values can be changed directly from their date and time entities or by opening Holiday Sensors under **Devices & services** and choosing **Configure**.

## Entity naming

Entity names are Start, Stop, Time home, and Now. New default entity IDs use the `holiday_sensor_` prefix. Known previous default IDs are migrated on setup, while custom IDs and occupied target IDs are preserved. Unique IDs remain unchanged. Review dashboards, automations, scripts, and templates that reference old entity IDs after upgrading; YAML references are not rewritten by this integration.
