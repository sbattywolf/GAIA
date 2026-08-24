# Zeus + Home Assistant Strategy Guide

## Executive Summary

Current architecture:
- Raspberry Pi 4 = Home Assistant
- GTX 1070 = Zeus Edge (Telegram, Router, Ollama, real-time actions)
- RTX 3090 = Zeus Brain (future coding, automation design, dashboard generation, MCP, OpenWebUI)

Key lesson learned:

Do NOT model the house using Home Assistant domains (light, switch, binary_sensor).
Model the house using user intent:

Area -> Function -> Entity

Example:

'Accendi luci camera'

becomes

Area=Camera da letto
Function=Lighting

then resolves to switches, lights, groups or automations.

## Design Principles

1. Python First
2. Home Assistant Second
3. LLM Third

Use LLM only for ambiguity and follow-up context.

## Future Roles

Zeus Edge:
- realtime control
- Telegram
- Home Assistant
- inventory

Zeus Brain:
- coding
- dashboard generation
- automation optimization
- research
- MCP
