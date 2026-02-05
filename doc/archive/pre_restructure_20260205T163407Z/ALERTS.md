ALERTS - Enabling Telegram / WhatsApp / Email for GAIA

This document explains how to enable real alerts for GAIA. The repo includes safe test scripts that require credentials set via environment variables.

1) Email (SMTP)
- Set env vars: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, optional `FROM_EMAIL`.
- Test send:

```powershell
$env:SMTP_HOST='smtp.example.com'; $env:SMTP_PORT='587'; $env:SMTP_USER='you@example.com'; $env:SMTP_PASS='s3cret'; python scripts\send_alert_email.py --to sbattywolf@hotmail.com --subject "GAIA: Connect" --body "Please connect via WhatsApp/Telegram."
```

2) Telegram Bot
- Create a bot with BotFather, obtain `BOT_TOKEN`.
- Get your `CHAT_ID` (use `@userinfobot` or send a message and query `getUpdates`).
- Set env vars: `TELEGRAM_BOT_TOKEN`, `CHAT_ID`.
- Test send:

```powershell
$env:TELEGRAM_BOT_TOKEN='123:ABC'; $env:CHAT_ID='-1001234567890'; python scripts\send_telegram_test.py --text "GAIA test: please reply to this chat"
```

3) WhatsApp via Twilio
- Sign up for Twilio, enable WhatsApp sandbox or request Business API.
- Set env vars: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `FROM_WHATSAPP` (e.g. whatsapp:+1415...), `TO_WHATSAPP` (whatsapp:+1...)
- Test send:

```powershell
$env:TWILIO_ACCOUNT_SID='AC...'; $env:TWILIO_AUTH_TOKEN='...'; $env:FROM_WHATSAPP='whatsapp:+1415...'; $env:TO_WHATSAPP='whatsapp:+1XXX...'; python scripts\send_whatsapp_twilio.py --text "GAIA test: please reply"
```

Message templates
- Email subject: "GAIA: Connection request"
- Email body:
  "Hello,

  This is an automated request from GAIA to establish a real-time connection.
  Please reply with your preferred channel (Telegram or WhatsApp) and ID/phone.

  Regards,
  GAIA Monitor"

- Telegram/WhatsApp text: "GAIA Monitor: please reply to confirm connection"

Approval flow via Telegram
- The approval phrase is the single word: `APPROVE`.
- To approve a dry-run and allow GAIA to proceed to apply, open the chat with the bot and send `APPROVE`.
- You can run the approval listener which waits for the APPROVE message and records it:

```powershell
$env:TELEGRAM_BOT_TOKEN='<BOT_TOKEN>'
$env:CHAT_ID='<CHAT_ID>'
python scripts\approval_listener.py --timeout 1800
```

When the bot receives `APPROVE` from the configured `CHAT_ID`, the listener writes the approval to `.tmp/approval.json`, appends an `approval.received` event to `events.ndjson`, and records a trace in `gaia.db`.

Security notes
- Never commit tokens or passwords to the repo. Use environment variables or a secrets manager.
- The provided scripts are minimal examples for operator use. Integrations (webhooks, long-running services) should store secrets securely and implement retries/backoff.

If you provide credentials (or a secure way to access them), I can wire the `gaia.alerts` helpers to send real messages and record the results in `gaia.db`. I will not use any credentials unless you explicitly supply them.
