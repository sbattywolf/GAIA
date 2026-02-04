# Documentation Strategy and Index

Purpose
- Provide a single place describing how docs are organized, versioned and maintained for GAIA.

Principles
- Repo is source-of-truth: keep structured docs under `doc/` and treat Git history as canonical.
- Preserve important historical docs: never delete old docs — mark superseded files with `-deprecated` suffix.
- Versioning: use Git tags for released snapshots and a `CHANGELOG.md` for user-visible changes.
- Wiki: GitHub Wiki may be used for high-level how-tos and as a browsable index, but keep detailed technical docs in `doc/`.

Timestamp policy
- When adding or updating docs, include an ISO date+time stamp in 24h format: `YYYY-MM-DD HH:MM` (UTC preferred).
- Do not overwrite older timestamps: when updating, add a new header `Updated: YYYY-MM-DD HH:MM` and leave older `Created:` lines intact.

Doc grooming
- Maintain `doc/MASTER_DOC_INDEX.md` with short descriptions and links to important documents.
- Periodically (quarterly) review `doc/` to consolidate duplicative content and mark obsolete files with `-deprecated`.
- Add a small `doc/MAINTAINERS.md` describing who owns what area and how to request doc changes.

Automation & CI
- Add a lightweight CI check that ensures changed docs include `Created:` or `Updated:` header lines and follow the timestamp format.
- Generate `doc/MASTER_DOC_INDEX.md` from a simple script that scans `doc/` and lists filenames + first paragraph.

Migration / merging strategy
- When merging multiple docs into a single canonical doc, keep the original files as `name-archived.md` in `doc/archive/`.
- Add a short release note entry in `CHANGELOG.md` describing the merge and list files archived.

Usage notes
- For quick team edits and conversational content the GitHub Wiki is acceptable, but all operational runbooks and audit-facing docs must remain in `doc/`.

Contact
- For doc ownership or to propose doc reorg, open an issue using the `docs/` label and mention the `docs-maintainers` team.
