# GAIA Engineer Local v0.1 — E2 Bounded Tool Correction Manifest

## Milestone

E2 — Controlled Coding Agent

## Status

`CORRECTION PREPARED`

## Correction baseline

Original supplied package SHA-256:

`a6a1a95a92da550b54e2eff4929b1bd77e56d472be6cd2e323aafeb245d29564`

The exact supplied package was used as the correction baseline.

## Scope

Exactly two bounded implementation corrections:

1. `git_inspect` filesystem-path arguments are workspace-bounded through the
   authoritative E2 workspace resolver while preserving read-only Git inspection,
   the `status` / `diff` / `log` allowlist, and `shell=False`.
2. `run_tests` uses the minimum explicit pytest argument allowlist required by E2,
   rejecting configuration, plugin, import-path, environment/config-redirection,
   and related execution escape mechanisms.

Directly necessary regression tests were added for both corrections.

## Preserved constraints

- No GAIA production architecture changes
- No ADR-0001 / ADR-0003 changes
- No W3 / PM-001 / PM-002 changes
- No generic Git abstraction
- No generic shell executor
- No Git mutation
- No expanded E2 tool surface

## Validation

- E2 boundary suite: PASS, 32/32
- `git diff --check`: PASS
- protected-file verification: PASS

## Delivery model

Engineer workspace → implementation/validation → complete replacement ZIP →
Human Owner application to authoritative local VS Code checkout → Human Owner
re-validation → Architect implementation re-review.

## Non-claims

This package does not claim Human Owner validation, Architect approval, commit,
push, merge, or PR creation.
