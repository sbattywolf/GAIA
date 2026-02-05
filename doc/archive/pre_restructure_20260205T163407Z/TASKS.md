GAIA — Consolidated Tasks and Next Steps
======================================

Purpose
-------
This document consolidates the work done so far and lays out the next small set
of focused, testable tasks to finish the local controller + sequence workflow
and deploy it to a constrained device (MyNAS).

Background (short)
- Sequences are created and optimized into composite steps by `scripts/sequence_manager.py`.
- Large sequences are proposed into `doc/SEQUENCE_PROPOSALS.md` and an active task
  is recorded in `.tmp/active_task.json` with granular todos in `.tmp/sequence_todos.json`.
- `agents/sequence_worker.py` processes todos and merges proposals when complete.
- `agents/controller_agent.py` is a lightweight local coordinator that can assign
  todos, notify via Telegram, and run in `--simulate` or live mode.
- A monitor UI page `/sequences` and SSE endpoints were added to inspect state.

Goals
-----
1. Provide a small controller that can run reliably on low-resource devices (MyNAS).
2. Provide simple control surfaces (HTTP + UI) so humans can inspect and operate tasks.
3. Provide a documented, repeatable deployment path and lightweight systemd unit.

Planned Steps (small batches)
-----------------------------
1) Consolidate docs & plan (this file) — DONE

2) Controller HTTP API & monitor integration
   - Add a minimal REST API for the controller so UI or other agents can:
     * view active task and todos
     * claim/assign a todo
     * mark todo done (with optional notes)
   - Expose endpoints under `/api/controller/*` in `monitor/app.py`.

3) UI controls for `/sequences`
   - Add buttons in the `monitor/templates/sequences.html` page to claim/complete
     specific todos (POST to the controller API).

4) Systemd & deployment readiness
   - Provide a pre-filled `doc/gaia-controller.service` and `scripts/run_controller.sh` (done)
   - Add optional logging redirect and example unit with `User`/`WorkingDirectory` placeholders.

5) Local validation & tuning
   - Run the controller in `--simulate` and observe CPU/memory; tune `CONTROLLER_POLL` and batch.
   - Run realistic load with several large sequences to stress-test the todo flow.

6) MyNAS deploy & acceptance
   - Deploy to MyNAS, run in simulate then live mode, collect logs and adjust.

Acceptance criteria
-------------------
- Controller runs under small resource envelope (low CPU, low memory) on MyNAS during simulated runs.
- Monitor UI shows active sequence and todos; user can claim and mark todos via UI.
- Proposal merge flow completes and archives proposals to `doc/SEQUENCE_ARCHIVE.md`.

Notes
-----
- All coordination is file-based (`.tmp/*`); this keeps dependencies minimal for MyNAS.
- Environment variables allow tuning (see `scripts/run_controller.sh` and `doc/DEPLOYMENT.md`).

Next immediate action
---------------------
- Implement the Controller HTTP API endpoints and wire them into the monitor UI (step 2).
