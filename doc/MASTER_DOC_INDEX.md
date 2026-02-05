# MASTER_DOC_INDEX

This document defines the new concise documentation structure, naming conventions and where archived material lives.

Structure (top-level folders):

- `01_onboarding` — what new contributors or agents need to get started. Minimal runnable steps.
- `02_technical` — API specs, architecture, data models, design decisions.
- `03_procedural` — runbooks, playbooks, operational procedures, approvals.
- `04_reference` — configs, schemas, examples, CLI usage.
- `05_backlog` — consolidated backlog and prioritized stories/tasks mapped to features.
- `06_archives` — pointers to archived material (large/old docs) and historical notes.

Quick start Overviews:

- `02_technical/OVERVIEW.md` — curated reading order for core technical topics: architecture, multi-agent patterns, Telegram integration, secrets handling, and CI setup.
- `03_procedural/OVERVIEW.md` — curated reading order for operational runbooks: CI/audit capture, scheduler runbooks, deployment, alerts, and session procedures.

Naming convention (filename slug):

`<category>-<feature-or-area>-<short-description>.md`

Examples:

- `technical-api-auth.md`
- `procedural-deploy-release-checklist.md`
- `onboarding-agent-quickstart.md`

Archive policy:

- All existing docs are moved to `doc/archive/pre_restructure_<timestamp>/` and left intact.
- New documents should be concise, focused, and cross-referenced to archived originals when needed.

Backlog approach:

- The `05_backlog/MASTER_BACKLOG.md` will contain a single consolidated backlog grouped by feature, with links to archived detail documents and referenced GitHub issues.
