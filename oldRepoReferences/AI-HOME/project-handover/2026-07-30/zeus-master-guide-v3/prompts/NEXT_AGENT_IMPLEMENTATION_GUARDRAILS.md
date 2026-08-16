# Implementation guardrails after the Milestone 3 plan is approved

Use Agent mode only for one approved tranche at a time.

First tranche should contain only:

- lightweight registry models;
- minimal read-only WebSocket client;
- command/result correlation;
- synthetic contract tests;
- no Telegram wiring;
- no Home Assistant mutation;
- no label-based actions.

Required final output:

- modified files;
- tests and result;
- `py_compile` result;
- `git diff --check` result;
- complete diff;
- deviations and risks;
- no commit or push.
