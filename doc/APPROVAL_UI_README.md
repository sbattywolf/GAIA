Approval UI — Quick commands and safety checklist

Purpose
- Short reference for approving checkpoints and running notifier dry-runs.

Interactive options (planned UI mapping)
- 1  List checkpoints: show `CHECKPOINT_*.md` files.
- 2  View checkpoint: `type CHECKPOINT_<n>.md` or open in editor.
- 3  Approve (interactive):
     python scripts/approve_checkpoint.py --checkpoint <n> --signer "Your Name"
     then type APPROVATO when prompted.
- 4  Approve (non-interactive):
     python scripts/approve_checkpoint.py --checkpoint <n> --signer "Your Name" --yes
- 5  One-shot notifier DryRun (prints snapshot):
     python scripts/telegram_realtime.py --interval 0
- 6  Enable autonomy (manual): create `.tmp/autonomous_mode.json` with:
     { "autonomous": true }
     (Recommended: only after approval and allowlist checks.)

Safety checklist (must pass before enabling sends)
1. Confirm `CHECKPOINT_<n>.md` contains APPROVATO entry (or run approve CLI).
2. Verify `config/agent_mode_allowlist.json` includes required commands (e.g., `send_telegram`).
3. Run `python scripts/telegram_realtime.py --interval 0` and inspect outputs — ensure no outbound network calls.
4. If ready, enable autonomy by creating `.tmp/autonomous_mode.json` and re-run DryRun with `--send` if confident.

Quick examples
```
# interactive approve
python scripts/approve_checkpoint.py --checkpoint 2 --signer "Carlo"

# non-interactive approve
python scripts/approve_checkpoint.py --checkpoint 2 --signer "Carlo" --yes

# single snapshot dry-run
python scripts/telegram_realtime.py --interval 0

# enable autonomy (manual)
python - <<'PY'
from pathlib import Path
Path('.tmp').mkdir(exist_ok=True)
Path('.tmp/autonomous_mode.json').write_text('{"autonomous": true}', encoding='utf-8')
PY
```

Notes
- Approvals append audit events to `events.ndjson`.
- Non-interactive approval (`--yes`) skips the human token check — use only when automating with additional controls.
