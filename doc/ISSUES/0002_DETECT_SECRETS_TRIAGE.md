Title: Triage: detect-secrets findings and automation

Summary:
Create a triage script and workflow for `detect-secrets` findings. Produce sanitized NDJSON output and integrate triage steps into contributor flow.

Why:
Automating triage reduces noise, speeds remediation, and ensures consistent handling of secrets findings.

Acceptance criteria:
- Triage script that parses `detect-secrets` output and produces NDJSON with `sanitized: true|false` and rationale.
- `doc/ISSUES/sensitive_files_candidates.txt` generated and reviewed.
- A sample triage run documented in `doc/` and added to CI for scheduled scans.

Suggested labels: security, triage, automation

Suggested assignees: security-team
