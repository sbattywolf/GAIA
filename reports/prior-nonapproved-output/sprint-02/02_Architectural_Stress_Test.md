# Architectural Stress Test

## Scenarios

- 3090 offline while 1070 must keep serving deterministic home queries;
- Home Assistant reachable but model runtime unavailable;
- Telegram sends duplicate or closely spaced updates;
- registry metadata is stale while runtime state is current;
- tool call times out after a side effect;
- capability policy changes during a long-running workflow;
- memory contains a corrected preference and an older contradiction;
- external framework checkpoint cannot be migrated;
- QNAP is offline during normal operation;
- user requests an ambiguous physical action.

## Expected properties

Graceful degradation, idempotency where possible, bounded retries, explicit uncertainty, post-action verification, no synchronous NAS dependency, deterministic fast paths for known queries and human confirmation for ambiguous high-impact action.

## Architectural pressure revealed

Recovery, state ownership and post-action verification are first-class concerns even if they are not first-class elements of the conceptual model.
