**GUI — Extra: mapping and next steps**

Summary:
- The GUI provides a lightweight operator view (SSE monitor + pending commands UI). The current monitor exists under `scripts/monitor_index.html` and `scripts/serve_events_sse.py`.

Backlog items:
- Add `Pending` tab that shows `.tmp/pending_commands.json` and provides copyable CLI actions.
- Localized UI strings (EN/IT) via URL param or saved preference.

Acceptance tests:
- UI shows live events from `events.ndjson` and shows updated pending list when commands are enqueued/approved.

Next step:
- Implement Pending tab and an API endpoint to fetch `pending_commands.json` content from server-side.
