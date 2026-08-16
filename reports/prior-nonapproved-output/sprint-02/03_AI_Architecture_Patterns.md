# AI Architecture Patterns

## Recommended pattern palette

- deterministic route before LLM;
- classifier/router with structured output;
- bounded tool calling with schema validation;
- human approval gate;
- evaluator/critic loop for high-value outputs;
- adapter anti-corruption layer;
- immutable execution trace;
- snapshot-then-filter for consistent aggregate reads;
- canonical resource target resolution;
- graceful local-first degradation.

## Use cautiously

- autonomous open-ended loops;
- shared mutable blackboards;
- unconstrained multi-agent conversation;
- framework-owned long-term state;
- prompt-only permissions;
- one universal memory store.

## Selection rule

Use the simplest pattern that fits task structure and risk. Predictable tasks should remain chained or routed. Multi-agent orchestration needs evidence that responsibility or tool sets exceed a simpler design.
