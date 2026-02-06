# Git history, searchable text, and labels — strategy

Goal: prefer searchable text (commits, PR bodies, `events.ndjson`) for history and discovery while using a minimal, well-defined label set only when it meaningfully reduces cognitive load or enables automation. Optimize for simplicity and minimal Git metadata bloat.

Recommendations
- Primary search surface:
  - Commit messages: use a short subject + structured metadata line when helpful.
  - PR title and description: include reproducer steps, task IDs, and short rationale.
  - `events.ndjson`: append structured NDJSON events for agent actions and important lifecycle steps (already used by this repo).
- Commit message template (recommended):

  Subject line (<=72 chars)

  Structured metadata (single line, optional):
  "type:task task:123 agent:copilot session:20260206"

  Longer description / rationale / test notes

- Labeling policy (minimal):
  - Only use labels that drive actions or filtering: `security`, `breaking-change`, `needs-review`, `wip`.
  - Keep label names short and canonical; add a single sentence label descriptions in `doc/labels.md` if needed.
  - Avoid creating per-task labels; use text and `events.ndjson` for history instead.

- Storage / git-size guidance:
  - Do not commit large artifacts; use `git-lfs` or external artifact storage.
  - Prefer squashing or rebasing topic branches before merge to avoid noisy intermediate commits in mainline history.

- Search tooling:
  - Use `git log --grep` and `rg`/`ripgrep` across the repo and `events.ndjson` for fast text search.
  - Example: `rg "task:123" --hidden` will find structured metadata across commits/PR text if stored in files or appended events.

Practical tradeoffs
- Pros of text-first approach:
  - Easy to search with standard tools, no extra Git metadata to manage.
  - Works offline and is future-proof across platforms.
- When to add labels:
  - Labels are useful when a UI or automation filter depends on them (e.g., auto-merge, security triage).
  - When adding labels, prefer a short canonical set and document meanings.

Implementation notes
- Start: prefer the commit message template and `events.ndjson` entries; reduce label churn.
- Add a small helper (agent or script) to append canonical `git.action` events to `events.ndjson` on important steps (branch created, PR opened, secret rotated).
- Keep a compact `doc/labels.md` if labels are introduced for automation.

Example event entry (append to `events.ndjson`):

```
{"type":"git.action","action":"create_branch","branch":"session/20260206-copilot/desc","task":"123","agent":"copilot","timestamp":"2026-02-06T12:00:00Z"}
```

This provides searchable text without needing many labels and keeps Git metadata small.
