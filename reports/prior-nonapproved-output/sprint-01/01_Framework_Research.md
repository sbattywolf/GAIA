# Framework Research

## Question

Which existing frameworks, SDKs, protocols and platforms can GAIA reuse without surrendering identity, state ownership or replaceability?

## Evaluation lens

- local operation and model independence;
- explicit state and recoverability;
- tool/capability boundaries;
- observability and human approval;
- modular adoption rather than all-or-nothing runtime commitment;
- maintenance burden for a very small team;
- ability to keep Home Assistant, Telegram and model runtimes behind adapters.

## Candidate families

- graph/state orchestration: LangGraph-like systems;
- role/conversation multi-agent systems: CrewAI and AutoGen-like systems;
- SDK/plugin orchestration: Semantic Kernel and related Microsoft tooling;
- direct model runtime/API: Ollama and compatible local runtimes;
- integration protocols: MCP as an optional boundary, not a mandatory Core primitive;
- home-domain platform: Home Assistant as source of truth and external runtime.

## Working conclusion

Reuse concrete capabilities at the edges before adopting a framework as the Core. Validate real workflows first. A framework is acceptable when it can be bounded, replaced and prevented from owning GAIA's identity or canonical state.
