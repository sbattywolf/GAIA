# PM-002 Evidence

**Status:** ENGINEER VALIDATION PACKAGE — HUMAN OWNER AUTHORITATIVE VALIDATION PENDING

## Baseline

`f01a13a8fd6258f0f568b1ceecea82c9b8a62aa8`

## Evidence provenance

- **Deterministic:** PM-002 tests exercise the inherited W3 Policy/Approval gate, one Light Resource, bounded Capability, and explicit outcome semantics using controlled providers.
- **Local operational:** shell control scripts validate external configuration, disablement, rollback, and the real read-only Home Assistant Light adapter path when run in the Human Owner environment.
- **Human Owner authoritative:** NOT EXECUTED BY ENGINEER. The Human Owner must perform startup, normal read, restart, disablement, recovery, and final usability validation locally.

## PM2 matrix

| ID | Result in Engineer environment | Required Human Owner evidence |
|---|---|---|
| PM2-T01 | PASS — PM-002 harness preserves W3 gate semantics; full W3 suite requires Human Owner checkout | Run exact W3 T01–T10 regression |
| PM2-T02 | PASS — PM-002 harness preserves PM-001 contract; full PM-001 suite requires Human Owner checkout | Run exact PM-001 P01–P14 regression |
| PM2-T03 | PASS — missing configuration fails closed; configured startup requires HA environment | Successful configured startup |
| PM2-T04 | NOT EXECUTED — no private HA credentials available | One successful source-grounded Light read |
| PM2-T05 | PASS — restart procedure is stop then start | Stop → start → valid Light read |
| PM2-T06 | PASS — deterministic unavailable outcome | Optional local failure evidence |
| PM2-T07 | PASS — deterministic stale and malformed/error outcomes | Optional local failure evidence |
| PM2-T08 | PASS — denied/indeterminate/not-granted produce zero provider calls | Preserve zero-execution observation |
| PM2-T09 | PASS — disabled state blocks start/read | Disable locally and show no external read |
| PM2-T10 | NOT EXECUTED — Human Owner must select an actually observed local failure | Human Owner recovery evidence |
| PM2-T11 | PASS — bounded script output distinguishes disabled and read outcome | Inspect local diagnostics |
| PM2-T12 | PASS — repository package contains no literal credential/token values | Human Owner secret-hygiene inspection |
| PM2-T13 | NOT EXECUTED — Human Owner authoritative | Start/use/disable/recover |
| PM2-T14 | PASS — evidence + manifest contain baseline, matrix and provenance | Reconstruct after package application |

## Operational procedures

### Startup / normal read

```text
./gaia-bootstrap-poc/scripts/pm002_start.sh
```

The command validates external configuration and performs exactly one read-only Light observation. It emits only a sanitized outcome line.

### Restart

```text
./gaia-bootstrap-poc/scripts/pm002_stop.sh
./gaia-bootstrap-poc/scripts/pm002_rollback.sh
./gaia-bootstrap-poc/scripts/pm002_start.sh
```

The stop command disables the bounded slice. Rollback restores the known-good enabled state without performing an external read. Start then performs one read-only validation.

### Disablement

```text
./gaia-bootstrap-poc/scripts/pm002_stop.sh
```

While disabled, `pm002_start.sh` exits before loading runtime credentials or contacting Home Assistant.

### Recovery

Select one actually observed local failure. Document the observation, then perform the minimal local recovery. The package does not implement self-healing.

## Sanitization

No Home Assistant token, private endpoint, raw response payload, or household credential is stored in this package.

## Human Owner validation record

```text
Startup:       PENDING
Normal read:   PENDING
Restart:       PENDING
Disable:       PENDING
Recovery:      PENDING
Final usability:PENDING
```

## Architect review

Pending completion of Human Owner authoritative local validation.
