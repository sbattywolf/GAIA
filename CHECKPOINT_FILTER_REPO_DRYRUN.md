# CHECKPOINT: Filter-repo — Dry-run commands & safety checklist

Purpose
- Provide a safe, reviewer-friendly set of commands to perform a full dry-run of the history rewrite in a mirror clone. This does not affect `origin` — the rewrite happens inside `repo-mirror.git` and produces artifacts (analysis, bundle) for review.

Prerequisites
- `git-filter-repo` installed and on PATH. Install via `pip install git-filter-repo` if needed.
- Work is performed in a mirror clone: `repo-mirror.git` (already present in repo root).
- Candidate paths file: `.tmp/filter-repo-paths.txt` (path list to remove) — already prepared.
- Keep a backup of the mirror before any rewrite.

High-level plan
1. Backup the existing mirror (safe copy).
2. Run an analysis limited to the candidate paths to estimate impact.
3. If reviewers approve, run the rewrite inside the mirror (local-only). Do NOT push to `origin` without approvals.
4. Produce an artifact (`.bundle`) that contains the rewritten repo for maintainers to inspect or push to a staging remote.

Commands (PowerShell) — run from workspace root

```powershell
# 1) Enter the mirror and verify current state
Set-Location E:/Workspaces/Git/GAIA/repo-mirror.git
git status --short

# 2) Backup the mirror (fast copy of the bare repo)
Set-Location ..
Copy-Item -Recurse -Force repo-mirror.git repo-mirror-backup.git

# 3) Quick sanity: ensure the candidate paths file exists
Test-Path .\.tmp\filter-repo-paths.txt

# 4) ANALYZE only (no rewrite) to estimate deletions for the listed paths
Set-Location E:/Workspaces/Git/GAIA/repo-mirror.git
git filter-repo --analyze --paths-from-file ..\.tmp\filter-repo-paths.txt

# Inspect analysis results under repo-mirror.git\filter-repo\analysis\
Get-ChildItem .\filter-repo\analysis\* | Select-Object Name, Length
Get-Content .\filter-repo\analysis\path-deleted-sizes.txt | Select-Object -First 50

# 5) If reviewers approve, run the rewrite locally in this mirror (this will rewrite the mirror only)
#    This removes the listed paths from ALL history inside this mirror.
git filter-repo --invert-paths --paths-from-file ..\.tmp\filter-repo-paths.txt --replace-refs delete-no-add --force

# 6) After rewrite, produce a bundle of the filtered repository for reviewers to fetch and inspect
Set-Location ..
git clone --mirror repo-mirror.git repo-filtered.git
Set-Location repo-filtered.git
git bundle create ..\gaia-filtered-2026-02-07.bundle --all

# 7) Provide the bundle and the analysis files to reviewers (attach to PR or upload to a release asset)

# Safety notes:
# - DO NOT push rewritten refs to `origin` until explicit approval from reviewers.
# - Keep `repo-mirror-backup.git` as the rollback point.
# - If you must share rewritten refs remotely, push them to a temporary remote (or upload the bundle) and request a short-lived review window.
```

Recommended reviewer checklist
- Confirm `filter-repo` analysis output and sample of deleted paths.
- Verify no required assets will be lost (large binaries, docs needed for release tags).
- Approve a single maintainer to perform the push step or to accept the bundle.

Deliverables produced by these steps
- `repo-mirror.git/filter-repo/analysis/*` (analysis before/after)
- `repo-mirror-backup.git` (backup of mirror before rewrite)
- `repo-filtered.git` and `gaia-filtered-2026-02-07.bundle` (rewritten bundle for review)

Next steps after approval
- Push rewritten refs to a staging remote or open a PR with the bundle attached and the rewrite summary for final verification.
