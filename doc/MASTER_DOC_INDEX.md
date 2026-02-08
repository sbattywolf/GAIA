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

## Special Analysis Documents

**GPS 2026 Analysis** (Italian Education System):

A comprehensive analysis of the Italian GPS (Graduatorie Provinciali per Supplenze - Provincial Rankings for Substitute Teachers) 2026 update has been added to demonstrate GAIA's research and documentation capabilities:

- `GPS_2026_ANALISI.md` — Complete analysis in Italian (409 lines, 14 KB)
- `GPS_2026_ANALYSIS_EN.md` — Complete analysis in English (409 lines, 13 KB)
- `GPS_2026_ANALYSIS_SUMMARY_EN.md` — Executive summary in English (197 lines, 5.7 KB)
- `GPS_2026_INDEX.md` — Navigation index and document guide (158 lines, 5.5 KB)
- `GPS_2026_QUICK_REFERENCE.md` — Quick reference guide with checklists (191 lines, 5.8 KB)

Total: 1,364 lines of comprehensive policy analysis and operational guidance.
<<<<<<< HEAD
=======

## GitHub Projects Integration

**GitHub Projects V2 Integration** documentation added (2026-02-07):

A complete integration guide for using GitHub Projects with GAIA, including automatic issue addition, database sync, and team collaboration features:

- `GITHUB_PROJECTS_INTEGRATION.md` — Complete integration guide (329 lines, 10.9 KB)
  - Architecture and data flow
  - Step-by-step setup instructions
  - Token management and security
  - Troubleshooting guide
  - Configuration reference

- `GITHUB_PROJECTS_QUICKSTART.md` — Quick reference (276 lines, 8.4 KB)
  - Integration status overview
  - 2-minute setup guide
  - Common workflows and usage examples
  - Command reference
  - FAQ

**Related Files:**
- `.github/workflows/sprint_onboard.yml` — Automatic issue addition workflow (existing)
- `agents/github_sessions_sync.py` — Database to GitHub sync agent (existing)
- `scripts/setup_github_projects.py` — Configuration helper script (NEW, 400 lines)

**Status**: ✅ Integration implemented and documented. Optional feature, ready to use.
>>>>>>> f9cfb76b837e2e31b0c3e4f6dc4d476459fc8b2f
