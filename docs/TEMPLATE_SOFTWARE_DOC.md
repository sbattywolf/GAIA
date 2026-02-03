# Software Project Documentation Template

Purpose
- A concise, reusable documentation template for small-to-medium CLI-first Python projects. Keep focused, maintainable, and size-conscious.

Scope
- Covers repository layout, setup, development workflow, testing strategy, error prevention, iteration patterns, review cadence, and when to add external ad-hoc docs.

Repository layout (recommended)
- `README.md`: high-level project purpose and quickstart.
- `docs/`: living documentation derived from this template and project-specific docs.
- `agents/` or `src/`: implementation code.
- `scripts/`: developer helpers and tooling.
- `events.ndjson` or `logs/`: append-only runtime artifacts (never rewrite).
- `.env` and `.venv` excluded from git.

Setup & environment
- Provide exact, copy-paste commands for supported OS (Windows PowerShell and POSIX). Example (Windows):

  ```powershell
  python -m venv .venv
  & .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```

- Document required CLI tools (e.g., `gh`, `bw`) and whether they are optional or required for tests.

Development workflow
- Prefer CLI-first agents: parse args, attempt external action, then append an immutable event record (NDJSON) with a stable schema.
- Keep side-effects optional in tests by exposing a flag/env var like `PROTOTYPE_USE_LOCAL_EVENTS=1`.

Event / Audit strategy
- Use append-only NDJSON for events. Schema fields to standardize: `type`, `source`, `target`, `task_id`, `payload`, `timestamp`, `trace_id`.
- Maintain an audit DB (SQLite) for authoritative records. Keep schema simple and migratable.

Testing & iteration
- Isolate external interactions (wrap `gh`/network calls) so unit tests can stub them.
- Use environment flags to switch to local-only behavior during CI and developer testing.
- Add small integration tests that run in a disposable venv and assert `events.ndjson` lines appended.

Error prevention & resilience
- Validate inputs early and return non-zero exit codes for CLI tools.
- When writing files, prefer atomic appends or tempfile-then-rename patterns to avoid corruption.
- Guard DB writes with retries where appropriate and use simple transactions.

Documentation size & maintenance
- Keep in-repo docs small (< few MB). For deep or large guides, store externally and link from `docs/`.
- Use short, versioned docs and include a `Last-updated` timestamp and `author` metadata.

Review cadence & automation
- Add a short `docs/REVIEW.md` checklist and a scheduled `docs review` todo entry (weekly or monthly depending on activity).
- Automate linting (markdown + code) in CI and surface docs-changes in PRs.

When to split into ad-hoc docs
- Complex architecture diagrams, long migration guides, or large datasets should live outside the small docs folder and be linked.

References & examples
- Include concrete examples of CLI usage, event JSON samples, and minimal SQL snippets for audit writes.

Template maintenance notes
- Keep this template generic and maintain a project-specific derived doc (see `docs/GAIA_DETAILED_DOC.md`).

## Free-software policy & install sequence

This template prefers only free and open-source software for developer tooling
and runtime components. If a non-free tool is proposed, include a short
justification and a comparison to free alternatives.

Recommended install sequence (cross-platform):

1. Install Git
2. Install Python 3.10+
3. Create a virtualenv (`python -m venv .venv`) and activate it
4. Install runtime dependencies: `pip install -r requirements.txt`
5. Install developer/test deps: `pip install -r requirements-dev.txt`
6. Install `gh` (GitHub CLI) only if you accept its use; it's free/open-source.

Add commands per-OS under the System requirements section.
