# Plan for HA Holiday Sensors
- Integrasjon
- Brukes i HACS gjennom "Tilpassede pakkelagre"
- Egen integrasjonsside
- **Ikon:** `mdi:tsunami`

## date.holiday_start
- Redigerbar dato uten tid
- Ved installering er standard: To dager før dagens dato
- Ikon: `mdi:weather-sunny`

## date.holiday_stop
- Redigerbar dato uten tid
- Ved installering er standard: En dag før dagens dato
- Ikon: `mdi:home`

## time.holiday_time_home
- Redigerbart tidspunkt
- Ved installering er standard: 12:00:00
- «Mer info» viser hjemkomstdatoen under tidsvelgeren, midtstilt og med større skrift

### Attributter
| Attributt | Beskrivelse |
|---|:---|
| `homeDate` | Entitetens state og `date.holiday_stop` smeltet sammen til et tidspunkt som kan leses av Home Assistant |

## binary_sensor.holiday_now
`true` hvis *dagen i dag* er på eller etter `date.holiday_start`, og før `date.holiday_stop`, ellers false. Entiteten er utilgjengelig når dagens dato er etter `date.holiday_stop`.

Følgende har vært brukt med `input_datetime`:
``` yaml
{% set avreise = as_datetime(states('input_datetime.ferie_avreise')).date() %}
{% set hjemreise = as_datetime(states('input_datetime.ferie_hjemreise')).date() %}
{{ avreise <= now().date() < hjemreise }}
```

### Ikon
| State | Ikon |
|---|---|
| `true` | `mdi:weather-sunny` |
| `false` | `mdi:weather-sunny-off` |

### Attributter
| Attributt | Beskrivelse |
|---|:---|
| `lastDay` | `true` hvis dagen i dag er lik `date.holiday_stop`, ellers `false` |
| `dayNumber` | Dagens dato minus `date.holiday_start`, der avreisedagen er dag 0 |
| `daysLeft` | `date.holiday_stop` minus dagens dato |
| `numberOfDays` | `date.holiday_stop` minus `date.holiday_start` |

Eksempel: Avreise fredag og hjemreise søndag gir `dayNumber` 0 fredag, 1 lørdag og 2 søndag. `numberOfDays` er 2.
