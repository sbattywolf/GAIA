# Private env workflow

Purpose
- Describe the `.private/` folder usage and how scripts prefer private envs.

Policy
- Store local secrets in `.private/` and never commit them.
- The repository's runtime scripts will check for `.private/telegram.env` first; if present and readable they will use it. If missing or unreadable they will fall back to `.tmp/telegram.env` or other workspace env files.
- Use `scripts/init_private_env.py` to seed the `.private/` env files from existing workspace envs.

How scripts should behave (developer guidance)
- Prefer `.private/telegram.env` when present. Example pseudo-flow:

  1. If `.private/telegram.env` exists and is readable -> load from it.
  2. Else if `.tmp/telegram.env` exists -> load from it.
 3. Else -> run in dry-run mode and log missing credentials.

Security notes
- Keep `.private/` in `.gitignore` (already added).
- On POSIX, set file mode `600` for env files.
- On Windows, restrict file ACLs to your user account.
