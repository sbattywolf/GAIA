# Sprint: Token Rotation & Validation

Sprint goal
- Complete secure rotation of automation credentials for GAIA, replace expired automation token, and validate consumers.

Scope
- Create least-privilege tokens via GitHub App or manual PATs
- Persist tokens to `SecretsManager` under canonical names
- Update CI and repo secrets to use new tokens
- Validate agent and CI consumers; revoke temporary admin PAT

Mini-sprints
- Mini-sprint 1: Prepare helpers & docs (done)
- Mini-sprint 2: Token generation + token-cache (current)
- Mini-sprint 3: CI updates and consumer validation

Tracking
- See `doc/sprints/mini_sprint_create_tokens.md` for task breakdown and acceptance criteria.
