# OpenClaw quick scan

Cloned from: https://github.com/openclaw/openclaw

Summary:
- Large, mature project for a multi-channel personal AI assistant written primarily in TypeScript/Node.
- Supports many channels including Telegram; includes gateway, CLI, UI, and many integrations.
- Has CI, docs, and many scripts; preferred runtime Node >= 22 and uses `pnpm`.

Key places of interest for integrating Telegram-driven command control:
- `telegram/` directory under root — channel integration code and examples.
- `scripts/` — many operational helpers and shell scripts for packaging and running.
- `docs/` — detailed documentation (security, gateway, channels) to follow best practices for pairing and DM policies.

Notes for GAIA integration:
- OpenClaw already implements safe DM policies (pairing/allowlist). Mirror that approach in GAIA: enforce pairing/allowlist or single `CHAT_ID` enforcement.
- Prefer writing adapters (small gateway shim) that route select inbound messages into GAIA's queue rather than running arbitrary commands directly.
- For an initial prototype: only accept commands enclosed in code blocks or `run:` prefixes; enqueue for manual approval; require explicit APPROVE in same chat to execute.
