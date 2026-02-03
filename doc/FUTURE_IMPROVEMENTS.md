 # Future Improvements / Production Hardening

 This file captures recommended production hardening items for the GAIA prototype. These are intentionally deferred and documented here so they can be prioritized and implemented later.

 - Service supervision: provide systemd/service wrappers or a process supervisor for `approval_listener.py`, `monitor/app.py`, and agent processes.
 - Replace long-poll `getUpdates` mode with a webhook delivery option (HTTPS endpoint) for lower latency and fewer API calls.
 - Secrets handling: move secrets to a secret store (Vault/Bitwarden) or cloud KMS; avoid `.env` in shared workspaces; add rotation policies.
 - TLS and auth: enable TLS for the monitor UI and require strong API keys; consider OAuth for UI users.
 - Rate limiting & quotas: harden rate limits and persist counters in DB; add monitoring + alerting on failure spikes.
 - CI tests: add automated unhappy-path tests (invalid token, revoked token, wrong chat id) to CI, exercising `scripts/test_harness.py`.
 - Operational metrics: expose Prometheus-friendly metrics and logs; add structured logging.
 - Safe execution policies: require multi-approver confirmation for high-risk commands; add RBAC mapping beyond `TELEGRAM_APPROVER_IDS`.

 Record created: 2026-02-03
