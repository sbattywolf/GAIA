**GUI — Story**

Overview:
- Purpose: provide a minimal local UI for operators to view pending commands, approvals, and event history. The UI is primarily a monitoring surface (SSE tail) with links into the CLI actions.

Backlog mapping:
- `scripts/monitor_index.html` and `scripts/serve_events_sse.py` (existing) are the starting point.
- Backlog items: monitor, open pending list, approve/deny buttons (links to CLI invocation), per-item details and logs.

Acceptance criteria:
- Live SSE view of `events.ndjson` updates in real time.
- Pending commands page that shows `pending_commands.json` entries and provides CLI copy-paste actions for approve/deny/execute.
- Localized UI strings (EN/IT) toggled via URL param or per-chat preference.

Next steps:
- Add a `Pending` tab to `monitor_index.html` and fetch `.tmp/pending_commands.json` server-side.
- Wire monitor buttons to copy CLI snippets (no direct exec in UI) unless running in a secure, local-only mode.
- Add Italian translations for UI labels.
