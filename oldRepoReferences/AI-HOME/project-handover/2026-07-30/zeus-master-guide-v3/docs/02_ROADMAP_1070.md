# Remaining 1070 roadmap

## Milestone 3: read-only inventory

- Minimal authenticated Home Assistant WebSocket client.
- Entity Registry, Device Registry and Area Registry reads.
- Alias and label reads when supported by the installed Home Assistant version.
- Join registry metadata with `/api/states` runtime state.
- In-memory TTL cache and forced refresh.
- Redacted inventory export.
- No Home Assistant writes.

## Milestone 4: house semantic resolution

- `lighting` capability across `light`, `switch`, group, script and scene.
- Area-aware resolution.
- Canonical target per area/capability.
- Exclude technical LED/RGB entities.
- Avoid group/member duplicates.
- Define corridor, entrance and spot policies.

## Milestone 5: safe actions and context

- Turn on/off by area and capability.
- Check real service result and post-action state.
- Confirmation for ambiguous or broad requests.
- Minimal follow-up context: capability, area, target and requested state.

## Milestone 6: hardening and Zeus Edge v1 close-out

- Route and latency telemetry.
- Structured errors.
- End-to-end Telegram tests.
- Reboot/recovery test.
- Final runbook, branch clean-up and release tag.

## Completion estimate by milestones

- Completed: 2 of 6 milestones.
- Remaining: 4 milestones.
- Functional reading/reporting is already usable; semantic control and production hardening remain.
