### Implement mocked Telegram harness and CI-local runner

Problem
- Integration tests and local CI runs need a deterministic mocked Telegram API to avoid flaky network calls and to enable acceptance testing.

Goal
- Implement a lightweight mocked Telegram harness (local HTTP server) and a CI-local runner to exercise acceptance flows.

Acceptance criteria
- A test helper exposes a configurable local Telegram-like endpoint.
- CI can start the harness and run integration tests against it.
- Documentation describes how to run the harness locally for development.

Notes
- This is related to existing issue #61; consider consolidating work and referencing that issue.
- Label: `integration`, `high`