# OpenClaw Gateway Access Diagnosis

## Observed State
- OpenClaw container is running (gaia-3090-openclaw)
- Authentication token present in environment variables
- Container network: gaia_3090_model_stack_gaia-3090-model-stack

## Authentication Path
- Browser → https://gateway.openclaw.ai
- Gateway endpoint: 10.16.20.13:18789
- Authentication mechanism: Token-based (OPENCLAW_GATEWAY_TOKEN)
- Credential source: Environment variable in container

## Root Cause Analysis
Primary hypothesis: NETWORK_BIND - The Gateway is listening on an internal IP address (10.16.20.13) that's not accessible from the browser, which was changed from a public-facing address.

## Verification
- Container is running
- Token is present in environment
- Gateway listening on internal IP (not public)
- No external port mapping configured

## Next Steps
- Confirm if network binding change was intentional
- If not intentional, configure proper port mapping for external access
- Document the expected configuration for browser access
