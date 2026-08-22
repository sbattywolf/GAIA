# GAIA P0 — 1070 Runtime Evidence

## Checkpoint Executed

Commit:
`1aba4ccd02db718c204a134468514926b013a11f`

Branch:
`ING_3090`

## Target

Physical target:
`NVIDIA GeForce GTX 1070 with Max-Q Design`

VRAM:
`8192 MB`

## Preflight

Overall:
`PASS`

Docker:
- available: YES
- daemon reachable: YES

Ollama:
- host installation: NO
- endpoint port 11434: LISTENING

## Model Inventory

Observed models included:

- qwen3:8b
- llama3.1:8b
- nomic-embed-text:latest
- qwen2.5-coder:7b
- qwen-domotica:latest
- mistral:7b
- gemma2:9b
- llava:7b
- qwen2.5:7b
- qwen2.5:3b

## Validation Execution

Step 5:
`Running Ollama runtime validation`

Observed result:

`VALIDATION_EXIT=2`

The runner reached cleanup.

## Evidence Generation

`validation_evidence.json`:

`NOT GENERATED`

## Classification

Physical validation:
`BLOCKED`

Evidence generation:
`MISSING`

This is runtime evidence from the 1070 target and is not a PASS claim.

## Source Log

The complete execution log is available from:

`/tmp/gaia_1070_validation.log`

