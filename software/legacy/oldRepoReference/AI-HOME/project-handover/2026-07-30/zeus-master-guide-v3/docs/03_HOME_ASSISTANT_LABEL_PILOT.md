# Home Assistant label pilot

Create manually in Home Assistant:

- `zeus_cap_lighting`
- `zeus_control_allowed`
- `zeus_exclude`

## Initial safe assignments

### Bedroom wall switch main entity

Apply:

- `zeus_cap_lighting`
- `zeus_control_allowed`

Candidate previously identified:

```text
switch.wall_switch_camera_letto_switch
```

Do not apply those labels to power-outage memory, flip indicator, LED-disable or other configuration entities belonging to the same device.

### Explicit technical exclusions

Apply `zeus_exclude` to known technical light entities, including the indicator/status lights already identified. Review every assignment in Home Assistant before saving.

## Do not label as unrestricted controls yet

- Corridor
- Entrance
- Spot 1
- Spot 2
- Office group/member combinations

For these, determine the canonical control target first.

## Rule

Labels on areas, devices and entities are separate metadata. The future inventory provider must read them separately and must not assume inheritance.
