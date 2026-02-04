**STR_TODO_stoybl_bl_bl_1_governance**

Purpose
- Capture the governance task `t_final` to finalize the todo-list best-practice rule and ensure safe story closure.

Acceptance criteria
- A documented governance note exists in `doc/HANDOFF.md` and `doc/STR_TODO_stoybl_bl_bl_1.md` linking the rule.
- Before closing the story, an archived snapshot of `.tmp/todolists/...current` is created and referenced.

Steps
1. Add governance section to `doc/HANDOFF.md` describing the immutable-last-task rule and rationale.
2. Add a small script `scripts/archive_todolist_snapshot.py` (optional) to snapshot `.tmp/todolists/...current` to `.tmp/todolists/archive/` with timestamp.
3. Require explicit PR comment `t_final: ready-to-close` before the story is marked closed.

Acceptance test
- Confirm snapshot created and `doc/HANDOFF.md` contains the governance entry; PR includes the `t_final` acceptance checklist completed.
