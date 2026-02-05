Purge leaked tokens from repository history.

See `doc/todo-archive.ndjson` and `doc/issue-drafts.md` for background.

Planned steps:
1. Run `detect-secrets` baseline to identify leaked occurrences.
2. Draft `git filter-repo` replacement map and test in a local clone.
3. Coordinate force-push window with maintainers and mirrors.
4. Rotate any credentials discovered to be leaked.

Priority: critical
Est hours: 24
Scrum points: 13
