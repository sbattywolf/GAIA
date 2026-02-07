**History Rewrite Summary (2026-02-07 UTC)**

- **Action:** Rewrote repository history on `origin` by applying a filtered history produced with `git filter-repo`, then force-pushing the filtered mirror to `origin`.
- **Purpose:** Remove large and transient test artifacts (pytest temp files) and canonicalize backlog artifacts to reduce repo size and improve history clarity.

What changed

- A filtered mirror was prepared and validated with dry-run artifacts and mapping files.
- A full origin mirror backup was created before any destructive action.
- The filtered refs were pushed to `origin` (mirror, force) to replace history.

Artifacts & recovery

- Release (filtered bundle): https://github.com/sbattywolf/GAIA/releases/tag/filter-repo-dryrun-2026-02-07
- Local workspace archives: `archives/gaia-filtered-2026-02-07/` contains:
  - `gaia-filtered-2026-02-07.bundle`
  - `repo-filtered-2026-02-07.zip`
  - `repo-mirror-backup-2026-02-07.zip`
  - `repo-origin-backup-2026-02-07.zip`

Minimal recovery steps

1. To restore the original origin from the backup zip: unpack `repo-origin-backup-2026-02-07.zip` and from the unpacked mirror run:

```
git push --mirror https://github.com/<owner>/GAIA
```

2. To re-apply the filtered bundle elsewhere:

```
git clone /path/to/gaia-filtered-2026-02-07.bundle repo-filtered
cd repo-filtered
git push --mirror https://github.com/<owner>/GAIA
```

Notes

- CI was triggered by the push; please review recent workflow runs in Actions for failures.
- Consumers and maintainers should re-clone the repository after this history rewrite.
- If you want, I can open a status PR (this PR) and ping collaborators for awareness.

Contacts

- Repository operator: @sbattywolf
