# GAIA 1070 Credentials Strategy

## Overview
The 1070 runtime requires separate credentials from the 3090 reference to maintain security boundaries and prevent cross-contamination between environments.

## Required Credentials

### Open WebUI Secret Key
- Name: WEBUI_SECRET_KEY
- Purpose: Authentication for Open WebUI
- Source: Local environment variable
- Security: Should be randomly generated and kept secret

### OpenClaw Gateway Token (1070)
- Name: OPENCLAW_GATEWAY_TOKEN_1070
- Purpose: Authentication for OpenClaw gateway service
- Source: Local environment variable
- Security: Should be unique per 1070 instance

## Credential Management

### Generation Process
1. Generate unique WEBUI_SECRET_KEY for 1070
2. Generate unique OPENCLAW_GATEWAY_TOKEN_1070 for 1070
3. Store in .env file (not committed to repository)
4. Use environment variable expansion in compose.yaml

### Security Boundaries
- 1070 credentials are completely separate from 3090 credentials
- No credential reuse between environments
- Credentials stored outside of Git repository
- Environment files are added to .gitignore

## Migration Notes
- Do not reuse any 3090 credentials
- Each environment (3090 and 1070) has independent credential management
- This ensures isolation and prevents accidental cross-contamination

## Future Considerations
- When integrating with 3090, credentials for remote access can be added separately
- Remote 3090 connection should use separate authentication tokens
- All connections to remote services should be explicitly configured