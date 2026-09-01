# GAIA Node Pairing Setup - 1070 to 3090

## Current Status

### 3090 Gateway
- Running with bind=lan on port 18789
- Authentication: token-based (source = env, id = OPENCLAW_GATEWAY_TOKEN)
- No devices currently paired or connected

### 1070 Node
- Has OpenClaw container configured in compose file

## Steps to Pair Node

### Step 1: Prepare 1070 Node Connection
The 1070 node must connect using:
```
openclaw node run --host 10.16.10.41 --port 18789
```

With the authentication token provided through environment variable (token has been rotated and is now secure). The previous token value was removed from this documentation.

### Step 2: Watch 3090 for Pending Request
After starting the node, on 3090 run:
```
docker exec gaia-3090-openclaw openclaw devices list
```

Look for a new pending request with role=node.

### Step 3: Approve Device Pairing
Once the device request appears, approve it:
```
docker exec gaia-3090-openclaw openclaw devices approve <REQUEST_ID>
```

### Step 4: Verify Node Connection
After approval, check node status:
```
docker exec gaia-3090-openclaw openclaw nodes status
```

If there's a pending capability request, approve it:
```
docker exec gaia-3090-openclaw openclaw nodes approve <NODE_REQUEST_ID>
```

### Step 5: Test Node Capabilities
Once connected and approved, test with:
```
docker exec gaia-3090-openclaw openclaw nodes describe --node GAIA-1070
```

## Important Notes

- Do NOT use `--pair` or `openclaw connect` as these commands don't exist in 2026.7.1
- Keep both Ollama and OpenWebUI containers running on 1070
- Do NOT start the old 1070 Gateway container