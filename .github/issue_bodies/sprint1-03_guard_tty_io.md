### Guard/remove TTY/ioctl calls from scripts used in CI

Problem
- CI logs show `OSError: [Errno 25] Inappropriate ioctl for device` from scripts that assume a TTY. These cause errors in non-interactive CI environments.

Goal
- Make scripts safe for non-interactive environments by guarding calls that require a TTY or by detecting `sys.stdin.isatty()`.

Acceptance criteria
- Scripts that previously raised ioctl errors behave gracefully in CI (skip TTY-only actions or use non-interactive fallbacks).
- No new test failures caused by these guards.

Notes
- Review scripts in `scripts/` and `agents/` that interact with the terminal. Add `if sys.stdin.isatty():` guards where appropriate.
- Label: `ci`, `medium`