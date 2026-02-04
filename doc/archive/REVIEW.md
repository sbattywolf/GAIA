# Archive Review — Draft & Merge-related Documents

Created: 2026-02-05 00:13 (UTC)

Summary
- Action performed: copied draft / merge-related documentation files from `doc/` into `doc/archive/` with timestamped `.archived.<yyyymmddHHMM>` suffixes.
- Purpose: preserve a non-destructive snapshot of all draft and merge-artifact files so the main `doc/` folder can be cleaned up and consolidated.

What was archived (high-level)
- Files matching draft patterns: `*.draft*`, `*stoy_auto.draft.json`, `STR_Telegram.draft`, and related draft/current variants.
- Many `EPC_Telegram.*` feature drafts and `STR_Telegram.*` drafts/current snapshots were copied.
- Previously archived files under `doc/archive/` were also copied again with an additional `.archived.<timestamp>` suffix so no history was lost.

How to review the archived set
1. Inspect names and dates:

```powershell
Get-ChildItem -Path doc\archive | Sort-Object LastWriteTime | Format-Table Name,Length,LastWriteTime
```

or (bash)

```bash
ls -l doc/archive | sort
```

2. Open representative samples to confirm contents:

```powershell
notepad doc\archive\STR_Telegram.draft.archived.202602050013
```

3. If you want a plain list of original filenames that were targeted by the archival run:

```bash
find doc/archive -type f -printf '%f\n' | sed -E 's/\.archived\.[0-9]{12}(\.archived\.[0-9]{12})?$//g' | sort -u
```

Recommended workflow for deletion (safe, auditable)
1. Review period: keep originals for review for at least 48 hours (or one sprint planning meeting) so stakeholders can inspect archived copies.
2. Prepare a candidate deletion PR: create a branch `chore/archive-cleanup` that moves originals to `doc/archive/originals-to-delete/` or deletes them, and include `doc/archive/REVIEW.md` in the PR describing the change and review notes.
3. In the PR description, reference the archival timestamp (see `Created:` above) and list the top-level patterns (e.g., `*.draft*`, `*stoy_auto.draft.json`, `STR_Telegram.draft`).
4. Require at least one reviewer from the `docs-maintainers` team and sign-off from the rotation pilot owners before merging.

Commands to create a safe cleanup PR (example)

```bash
git checkout -b chore/archive-cleanup
# Option A: move originals into an 'originals-to-delete' folder for one-PR review
mkdir -p doc/originals-to-delete
git mv doc/*.draft* doc/originals-to-delete/ || true
git mv doc/*stoy_auto.draft.json doc/originals-to-delete/ || true
git add doc/originals-to-delete doc/archive/REVIEW.md
git commit -m "docs: move draft/merge artifacts to doc/originals-to-delete for review (archived)"
git push origin HEAD
# Open PR on GitHub and request review
```

Or to delete originals after sign-off (use only after approval):

```bash
git rm doc/*.draft* || true
git rm doc/*stoy_auto.draft.json || true
git commit -m "docs: remove archived draft/merge artifacts after review"
git push origin HEAD
```

Retention & versioning notes
- All archived files also have timestamped suffixes; we keep them indefinitely in the repo unless you approve safe removal.
- When merging docs into canonical versions (per `doc/MASTER_DOC_INDEX.md`), move superseded docs into `doc/archive/` with a note in `CHANGELOG.md` describing the consolidation.

Next steps (recommended)
- Review `doc/archive/` within the next 48 hours and list files you want removed or kept.
- I can prepare the `chore/archive-cleanup` branch and a PR draft that moves candidates into `doc/originals-to-delete/` for review if you want me to.
