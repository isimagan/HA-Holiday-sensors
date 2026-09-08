# Plan for HA Holiday Sensors
- Integrasjon
- Brukes i HACS gjennom "Tilpassede pakkelagre"
- Egen integrasjonsside
- **Ikon:** `mdi:tsunami`

## sensor.holiday_start
- Dato uten tid
- Ved installering er standard: To dager før dagens dato
- Ikon: `mdi:weather-sunny`

## sensor.holiday_stop
- Dato uten tid
- Ved installering er standard: En dag før dagens dato
- Ikon: `mdi:home`

## sensor.holiday_time_home
- Kun tidspunkt
- Ved installering er standard: 12:00:00

### Attributter
| Attributt | Beskrivelse |
|---|:---|
| `homeDate` | Sensorens state og `sensor.holiday_stop` smeltet sammen til et tidspunkt som kan leses av HomeAssistant |

## binary_sensor.holiday_now
`true` hvis *dagen i dag* er på eller etter `sensor.holiday_start`, og før `sensor.holiday_stop`, ellers false.

Følgende har vært brukt med `input_datetime`:
``` yaml
{% set home = as_datetime(states('input_datetime.ferie_avreise')).date() %}
{% set home = as_datetime(states('input_datetime.ferie_hjemreise')).date() %}
{{ avreise <= now().date() < hjemreise }}
```

### Ikon
| State | Ikon |
|---|---|
| `true` | `mdi:weather-sunny` |
| `false` | `mdi:weather-sunny-off` |

### Attributter
| Attributt | Beskrivelse |
|---|---|
| `lastDay` | `true` hvis dagen i dag er lik `sensor.holiday_stop`, ellers `false` |
| `dayNumber` | Dagens dato minus `sensor.holiday_start` |
| `daysLeft` | `sensor.holiday_stop` minus dagens dato |
| `numberOfDays` | `sensor.holiday_stop` minus `sensor.holiday_start` |
