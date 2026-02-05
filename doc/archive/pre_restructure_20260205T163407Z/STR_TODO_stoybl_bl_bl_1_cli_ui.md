**STR_TODO_stoybl_bl_bl_1_cli_ui**

Purpose
- Improve CLI ergonomics and monitor UI controls for inspecting, claiming, approving, releasing, and requeueing queued commands.

Acceptance criteria
- `scripts/claim_cli.py` exposes clear commands: `inspect`, `claim`, `refresh`, `release`, `approve`, `takeover`.
- Monitor UI shows per-item state (queued, claimed by, TTL remaining) and provides approve/deny/requeue buttons that call authenticated endpoints.

Minimum steps
1. Standardize `claim_cli.py` CLI flags and help text; return machine-readable JSON when `--json` is passed.
2. Update `scripts/monitor_server.py` to fetch item state and TTL from `scripts/claims.py` (via `claim_cli.py inspect --json`) and render in UI.
3. Add endpoint `/api/item/<id>/approve` that invokes `claim_cli.py approve --id <id> --token $MONITOR_ADMIN_TOKEN` (server-side token forwarding only when authorized).
4. Add unit tests for endpoint auth and CLI JSON output.

UI notes
- Show TTL countdown and highlight items close to expiry.
- Add audit link that opens `gaia.db` trace for the item.
