# GUI Improvements & Todo (saved snapshot)

Status: PAUSED (GUI implementation paused per request)

This document captures the current todo list and proposed GUI improvements for the GAIA Monitor. It is a snapshot of outstanding work and suggested priorities. The UI work is paused — do not make further UI changes until the user resumes this list.

## Summary of completed work

- Per-agent detail modal with log preview, Restart/Start/Stop/Probe/Compare controls (`monitor/templates/index.html`).
- Backend endpoints: `/api/agents/log_preview` and `/api/agents/compare` added to `monitor/app.py`.
- Client wiring for Start/Stop/Restart/Probe/Compare and SSE streams for `events` and `agent-state`.
- Integration test script: `scripts/test_integration.py` (Start → Probe → Compare → Restart → Stop).

## Outstanding items (proposed, ordered by priority)

1) UI: tweak menu width and spacing (medium priority)
   - Goal: provide more room for the content column (Overview/Agents etc.).
   - Files: `monitor/templates/index.html` (CSS grid column sizes).
   - Acceptance: content column visually larger; manual sign-off.

2) UI: preserve selected page across reload (low-medium)
   - Goal: store last-opened page in `localStorage` and restore on load.
   - Files: `monitor/templates/index.html` (JS `setActiveTab` enhancements).
   - Acceptance: page selection is restored after refresh.

3) UI: quick status badges in sidebar (high)
   - Goal: show live/total agent counts and simple health indicators in the left sidebar for quick at-a-glance status.
   - Files: `monitor/templates/index.html` and wiring to `/api/agents/pids_status`.
   - Acceptance: counts update on poll and SSE.

4) Validation: manual UI test (high)
   - Goal: run manual tests to exercise navigation, modal open, log preview, compare payloads, and Start/Stop flows.
   - Steps: Start monitor, open UI, navigate pages, open Agents → Open modal, run Probe and Compare, verify DB persisted state in `gaia.db`.

5) Docs update (medium)
   - Goal: document the per-agent panel features and the `compare` payload schema in `doc/HANDOFF.md` and `README.md`.
   - Acceptance: brief docs entries with example JSON for `/api/agents/compare`.

6) Cleanup & manual validation fixes (medium)
   - Goal: fix event handler edge cases, SSE reconnection robustness, and any aesthetic layout issues found during manual tests.

## Small API improvements (backend)

- Add `/api/agents/log_preview?id=&lines=` (already implemented) — consider adding `download=1` and `format=text|json` flags.
- Add `/api/agents/compare?id=` (already implemented) — consider adding `history=true` to include recent persisted snapshots.
- Consider a `/api/agents/restart` endpoint that performs stop→start with a single server call (safer than client stop then start).

## Suggested next actions (when you resume work)

1. Run manual validation and capture issues (use `scripts/test_integration.py` and manual UI checks). List any bugs.
2. Implement quick sidebar badges (high impact, small change).
3. Fix small layout spacing and optionally increase the content column width.
4. Add localStorage page persistence and menu active highlighting (already partially implemented).
5. Write short docs in `doc/HANDOFF.md` describing the new endpoints and UI features.

## Notes

- The monitor server must be running locally to exercise the UI and tests: `python monitor/app.py`.
- The PID map is stored at `.tmp/agents_pids.json`. Agent logs are under `.tmp/logs/`.
- The persistent DB is `gaia.db` in the repo root (contains `agents_state` / `agents_state_history`).

---
Document saved to `doc/GUI_TODO.md`. GUI implementation is paused; awaiting next instruction.
