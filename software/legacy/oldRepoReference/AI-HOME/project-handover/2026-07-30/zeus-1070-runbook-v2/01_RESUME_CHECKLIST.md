# Resume checklist

On the 1070, run only:

```bash
cd ~/github_repos/home_assistant_framework
git branch --show-current
sudo systemctl is-active zeus-edge
pgrep -af 'telegram_agent.py'
```

Expected: bootstrap branch, active, one process.

Smoke test Telegram:

```text
quante automazioni ci sono?
fammi un report dello stato della casa
ci sono luci accesse?
```

Do not run the bot manually while systemd is active.

Current next task: Milestone 3 read-only inventory.
