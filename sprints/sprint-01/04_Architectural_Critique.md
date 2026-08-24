# Architectural Critique

> Recovery status: Reconstructed  
> Source basis: surviving Sprint references, Architecture Discussion Guide, repository structure specification, and conversation history  
> Confidence: Medium  
> Preservation rule: This file retains its original role. Reconstructed passages are not presented as verbatim recovery.

## Primary challenge

The proposal to keep a minimal Core is directionally sound but unproven. Policy, memory, approval, audit, registry and recovery can accumulate until the Core becomes the monolith the design intended to avoid.

## Weak assumptions

- orchestration may be more central than expected;
- memory may become the highest-value subsystem rather than an adapter;
- Telegram may shape conversational state even if called “just a channel”;
- Home Assistant may become a dominant runtime rather than a simple adapter;
- MCP can simplify integration while widening authority and trust boundaries;
- local-first can remain aspirational unless degraded operation is tested;
- replaceability is not achieved by interfaces alone when state and operations are coupled.

## Required evidence

- bounded end-to-end scenarios;
- restart and degraded-mode tests;
- explicit state ownership map;
- tool trust and approval classification;
- framework replacement spikes;
- operational burden measurement;
- proof that one human can still understand and recover the system.

## Critic's conclusion

Do not reject frameworks categorically and do not adopt them for convenience. Force every candidate to reveal what state it owns, how it fails, how it is replaced and which GAIA concept it attempts to redefine.
