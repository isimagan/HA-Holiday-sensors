# Automasjoner for Bob til ferie
``` yaml
alias: Bob Ferie
description: ''
triggers:
  - trigger: time
    at: '10:00:00'
conditions:
  - condition: template
    value_template: >-
      {% set avreise =
      as_datetime(states('input_datetime.ferie_avreise')).date() %}

      {% set hjemreise =
      as_datetime(states('input_datetime.ferie_hjemreise')).date() %}

      {{ avreise <= now().date() < hjemreise }}
actions:
  - choose:
      - conditions:
          - condition: template
            value_template: |-
              {{
                (now().date() - (states('input_datetime.ferie_avreise') | as_datetime | as_local).date()).days > 0
                and
                (now().date() - (states('input_datetime.ferie_avreise') | as_datetime | as_local).date()).days % 9 == 0
              }}
        sequence:
          - action: script.bob_vac_and_mop
            metadata: {}
            data:
              fan_speed: turbo
              mop_mode: standard
              mop_intensity: 'off'
          - action: vacuum.start
            metadata: {}
            target:
              entity_id: vacuum.bob
            data: {}
        alias: Hver 9.dag
      - conditions:
          - condition: template
            value_template: |-
              {{
                (now().date() - (states('input_datetime.ferie_avreise') | as_datetime | as_local).date()).days > 0
                and
                (now().date() - (states('input_datetime.ferie_avreise') | as_datetime | as_local).date()).days % 3 == 0
              }}
        sequence:
          - action: script.bob_vac_and_mop
            metadata: {}
            data:
              fan_speed: balanced
              mop_mode: standard
              mop_intensity: 'off'
          - action: vacuum.start
            metadata: {}
            target:
              device_id: 37fe2b2cab810e2685756bf26b1ed10d
            data: {}
        alias: Hver 3.dag
mode: single

alias: Bob Ferie ankomst
description: ''
triggers:
  - trigger: time
    at:
      entity_id: input_datetime.ferie_hjemreise
      offset: '-02:00:00'
conditions:
  - condition: numeric_state
    entity_id: sensor.feriedager
    above: 2
actions:
  - action: script.bob_vac_and_mop
    metadata: {}
    data:
      fan_speed: turbo
      mop_mode: fast
      mop_intensity: 'off'
  - action: vacuum.start
    metadata: {}
    target:
      device_id: 37fe2b2cab810e2685756bf26b1ed10d
    data: {}
  - wait_for_trigger:
      - trigger: vacuum.returned_to_dock
        target:
          device_id: 37fe2b2cab810e2685756bf26b1ed10d
        options:
          behavior: each
          for:
            hours: 0
            minutes: 2
            seconds: 0
  - action: script.bob_vac_and_mop
    metadata: {}
    data:
      fan_speed: 'off'
      mop_mode: fast
      mop_intensity: standard
  - action: vacuum.start
    metadata: {}
    target:
      device_id: 37fe2b2cab810e2685756bf26b1ed10d
    data: {}
mode: single
```
