# Security / Sanitization

Mandatory invariants:

- NO_NETWORK
- NO_MUTATION
- NO_SECRET_COLLECTION
- NO_FILE_EXECUTION

Discovery root is an explicit task authorization boundary.

Known credential-bearing paths and private-key artifacts are blocked from
read/search/list collection. No shell or subprocess execution is implemented.

Delivery hygiene blocks:
- `__pycache__`
- `*.pyc`
- `.env` / secret-name artifacts
- private-key/certificate key artifacts
- credential-name artifacts

A sanitized delivery contains no such artifacts.
