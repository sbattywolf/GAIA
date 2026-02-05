# Branch Management Approval Process (draft)

Purpose
- Define a human-in-the-loop approval flow for branches/PRs before merges to protected branches.

Goals
- Prevent accidental merges to `main`/`release` without an explicit approval.
- Allow approvals via Telegram or repository-local ack files for air-gapped environments.
- Keep the flow simple so it can run locally or be moved to a NAS.

Flow (high level)
1. Developer opens a branch/PR and pushes changes.
2. CI job (or local script) invokes `scripts/branch_approval_manager.py --branch BRANCH --pr PR_NUM` which:
   - Emits an `approval.request` event to `events.ndjson` and writes `.tmp/branch_approval_{BRANCH}.json`.
   - Optionally posts a Telegram message with approve/reject buttons (if Telegram configured).
3. An approver replies via Telegram (or places `.tmp/branch_approval_ack_{BRANCH}.json`) to approve.
4. The manager converts approval into an ack file and emits `approval.received` event.
5. CI or local merge step detects the ack and proceeds with the merge.

Operational details
- Approvals should record approver identity (Telegram chat id or username) and timestamp in the ack file.
- Add a TTL to approval requests (e.g., expire after 24 hours) and require re-approval if changes happen.
- Protect `main`/`release` with branch protection rules that require the manager to write a verified status file before merge.

Implementation notes
- We'll start with a file-based manager (`scripts/branch_approval_manager.py`) that integrates with existing `approval_listener` to accept Telegram approvals.
- Later: add GitHub Checks API integration to set PR status programmatically.

Next steps
1. Implement `scripts/branch_approval_manager.py` (scaffolded) and test locally.
2. Add CI hook to call the manager when a PR targets protected branches.
3. Add explicit audit writes to `gaia.db` for compliance.
