# QNAP optional services

Current decision: no realtime dependency.

Draft folders:

- backup: repository and HA backups
- logs: offloaded JSONL/metrics
- monitoring: optional dashboards

Do not deploy Redis/PostgreSQL until a concrete shared-state or retention requirement exists.
