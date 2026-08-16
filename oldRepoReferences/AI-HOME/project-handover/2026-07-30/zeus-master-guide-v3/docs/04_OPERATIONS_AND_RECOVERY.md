# Operations and recovery

## Official bot process

```bash
sudo systemctl is-active zeus-edge
pgrep -af 'telegram_agent.py'
```

Expected: active and one process.

Never run the bot manually while systemd is active:

```text
DO NOT run: python 1070/app/telegram_agent.py
```

Doing so creates a Telegram `getUpdates` conflict.

## Restart

```bash
sudo systemctl restart zeus-edge
sudo systemctl is-active zeus-edge
```

## Logs

```bash
sudo journalctl -u zeus-edge -n 100 --no-pager
```

## Tests

```bash
cd ~/github_repos/home_assistant_framework
source .venv/bin/activate
PYTHONPATH=1070/app python -m unittest discover -s 1070/tests -p 'test_*.py' -v
python -m py_compile 1070/app/*.py
```

## Git safety

- Never use `git add .` for milestone commits.
- Do not use `git reset --hard` as routine rollback.
- Do not use `git clean -fd` around local documents/backups.
- Before a commit, use targeted `git restore` and explicit file lists.
- After a commit, prefer `git revert <commit>`.

## Old stash

The old stash named `wip-followup-filters-before-ha-conversation` is reference-only. Do not apply it to the current runtime. Its contents may predate Milestones 1 and 2.
