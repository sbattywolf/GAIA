# GAIA — PROJECT KNOWLEDGE READ-ONLY OPEN-SOURCE LANDSCAPE REVIEW

**Mode:** READ-ONLY reconciliation
**Repository changes:** none
**Architecture changes:** none
**Implementation recommendation:** deliberately withheld

Ho trattato il documento fornito come **operating prompt**, non come contenuto da riassumere. Ho triangolato il Project Knowledge disponibile, il repository GAIA corrente e una ricerca aggiornata dell'open-source landscape.

La conclusione principale è abbastanza netta:

> **GAIA non sta principalmente cercando di inventare un nuovo agent framework.**
>
> Sta cercando di definire una **semantic/governance layer personale e local-first** sopra capacità agentiche, runtime, tool, modelli, host e infrastruttura che in larga parte esistono già.

Questa distinzione cambia molto il rapporto **BUILD vs ADOPT**.

---

# A. WHAT GAIA IS ACTUALLY TRYING TO SOLVE

## A.1 Ricostruzione

La traiettoria storica mostra tre problemi diversi che nel tempo sono stati trattati insieme:

```text
1. COME FAR LAVORARE UN AGENT
        ↓
2. COME FARLO LAVORARE IN SICUREZZA E CON EVIDENZA
        ↓
3. COME INSERIRLO NEL MODELLO SEMANTICO PERSONALE DI GAIA
```

Il primo problema è largamente risolto dall'ecosistema OSS.

Il secondo è **parzialmente** risolto da framework e governance tooling.

Il terzo è quello in cui emerge la vera specificità GAIA.

---

## A.2 Cosa GAIA ha effettivamente stabilito

Il materiale riconciliato indica come già consolidate queste idee:

* GAIA è local-first;
* è human-controlled;
* è collaborator-based;
* Collaborator non equivale a LLM/processo/framework;
* Capability è separata dalla sua execution binding;
* Resource e authority devono restare distinguibili;
* Context non è automaticamente authority;
* evidence non equivale a architecture;
* historical material non equivale a current state;
* Engineer non equivale Architect;
* Project Knowledge non è un quarto authority layer.

La documentazione di identità è particolarmente esplicita: GAIA deve restare riconoscibile anche se cambiano modello, framework, runtime, UI o integrazione.

La riconciliazione post-W3 conferma inoltre che **Collaborator** e **Capability** sono concetti GAIA già dimostrati in forma bounded, mentre lifecycle completo dei Collaborator, Memory, Resource resolution e runtime topology restano aperti. 

---

# B. DURABLE REQUIREMENTS

Ho classificato i requisiti ricorrenti distinguendo **GAIA requirement** da **implementation choice**.

| Requirement                               | Lineage / evidence               | Status                                           | GAIA-specific?                                           | OSS already helps?                                       | Confidence |
| ----------------------------------------- | -------------------------------- | ------------------------------------------------ | -------------------------------------------------------- | -------------------------------------------------------- | ---------- |
| Durable behavioral identity               | `IDENTITY.md`, architecture work | Accepted/current                                 | **YES**                                                  | No, not in GAIA sense                                    | High       |
| Human ownership / authority               | governance + identity            | Accepted/current                                 | **YES**                                                  | Partially                                                | High       |
| Evidence vs authority separation          | W3 + engineering reconciliation  | Current                                          | **YES**                                                  | Partially                                                | High       |
| Historical/current separation             | ING_3090 + PK reviews            | Current                                          | **YES as governance rule**                               | Partially                                                | High       |
| Bounded Collaborator responsibility       | W3                               | Demonstrated                                     | **YES semantically**                                     | Runtime implementation exists elsewhere                  | High       |
| Capability independent from execution     | W3                               | Demonstrated                                     | **YES semantically**                                     | Tool/agent frameworks provide mechanisms                 | High       |
| Resource / external authority distinction | post-W3 model                    | Accepted/conceptual                              | **YES**                                                  | Not directly                                             | High       |
| Context as bounded information            | Context Model                    | Draft refinement, underlying concept established | **YES semantically**                                     | Many frameworks implement context                        | High       |
| Project Knowledge authority/lifecycle     | recent PK work                   | Current governance direction                     | **YES**                                                  | Knowledge systems exist, but not this authority model    | High       |
| Model neutrality                          | identity + research              | Current principle                                | **YES as constraint**                                    | Frameworks can support it                                | High       |
| Host neutrality                           | identity + agent review          | Current principle                                | **YES as constraint**                                    | OpenHands/Pydantic/etc. support multi-interface patterns | High       |
| Machine neutrality                        | 3090/1070 history                | Current principle                                | **YES as constraint**                                    | External runtimes support it                             | High       |
| Local-first                               | identity                         | Accepted identity                                | **YES**                                                  | OSS can support it                                       | High       |
| Safe tool execution / approval            | W3 + governance                  | Demonstrated boundedly                           | Not uniquely                                             | **Yes**                                                  | High       |
| Agent orchestration                       | historical implementation need   | Capability needed, ownership not established     | **NO**                                                   | **Yes, strongly**                                        | High       |
| Model/runtime selection                   | E2/3090                          | Open                                             | **NO**                                                   | **Yes**                                                  | High       |
| Host readiness                            | 1070/3090 experience             | Reusable engineering capability                  | **NO**                                                   | Generic system tooling can help                          | High       |
| Git/evidence packaging                    | E2 engineering process           | Current process                                  | **NO**                                                   | Git/CI/evidence tooling already exists                   | High       |
| Agent memory                              | post-W3                          | Unknown/open                                     | Requirement may be GAIA-specific; implementation unknown | **Yes, partially**                                       | High       |
| Cross-agent protocol                      | future                           | Proposed/future                                  | Not established                                          | **Yes: MCP/A2A/etc.**                                    | Medium     |
| Domain semantics                          | Domotics direction               | Future                                           | **Potentially YES**                                      | Frameworks do not define GAIA domain semantics           | High       |

### Important distinction

The project history explicitly identifies reusable capabilities such as host discovery, runtime/container/model inventory, security preflight, evidence/package generation and bounded Engineer tooling. 

Those are **valuable engineering assets**.

They are not evidence that GAIA needs to own an agent runtime.

---

# C. ACCIDENTAL / CONTEXTUAL REQUIREMENTS

This is where ING_3090 is particularly informative.

## C.1 RTX 3090

The 3090 became the environment for:

* engineering;
* model experimentation;
* E2;
* benchmark work;
* local Engineer execution.

The current evidence explicitly describes the final 3090 role as still open/partial. 

Therefore:

**3090 ≠ GAIA architecture.**

---

## C.2 GTX 1070

The 1070 was driven by:

* constrained target validation;
* physical host evidence;
* Domotics direction;
* legacy/ZEUS discovery.

The 1070 work was preparation, not a migration, and ZEUS evidence was explicitly not architectural authority. 

Therefore:

**1070 ≠ GAIA architecture.**

---

## C.3 Qwen3-Coder 30B

The 3090 work selected Qwen3-Coder 30B as a **provisional** primary candidate, with alternatives remaining experimental. 

Therefore:

**model choice ≠ durable requirement.**

---

## C.4 Ollama / Docker / Compose

These became engineering/runtime concerns because of the available hosts.

The 1070 work even uncovered a specific false-negative caused by distinguishing legacy `docker-compose` from the Compose plugin. That is an excellent engineering lesson.

But it is not a GAIA semantic requirement.

---

## C.5 VS Code / `.agent.md`

This became relevant because the Engineer was being operated through a host integration.

The repository currently contains multiple agent definitions, including model-specific ones.

This is evidence for a **host/role integration problem**, not evidence that GAIA needs its own proprietary agent runtime.

---

# D. OPEN-SOURCE LANDSCAPE

The landscape is considerably more mature than GAIA's historical implementation work may have implied.

## D.1 OpenHands

[OpenHands repository](https://github.com/OpenHands/OpenHands?utm_source=chatgpt.com)

OpenHands V1 now has a composable Software Agent SDK with explicit separation between:

* agent core;
* tools;
* workspace;
* agent server.

Its design explicitly addresses composability, context, tool execution and optional isolation. ([GitHub][1])

It can operate against local workspaces or remote/ephemeral environments, and its Agent Server can be run on different hosts. ([GitHub][2])

### GAIA relevance

**Very high for Engineer capability.**

It potentially replaces a large amount of GAIA-specific coding-agent scaffolding.

It does **not** replace:

* GAIA Identity;
* GAIA authority model;
* GAIA Project Knowledge;
* GAIA semantic Collaborator model.

---

# D.2 PydanticAI

[PydanticAI repository](https://github.com/pydantic/pydantic-ai?utm_source=chatgpt.com)

This is arguably one of the closest matches to the *engineering substrate* GAIA has been trying to construct.

It provides:

* typed agents;
* tools/toolsets;
* dependencies;
* structured outputs;
* model/provider neutrality;
* reusable capabilities;
* MCP;
* observability;
* evals;
* durable execution integrations;
* human-in-the-loop support. ([GitHub][3])

Importantly, PydanticAI explicitly treats capabilities as composable bundles of tools, hooks, instructions and model settings. ([GitHub][4])

### GAIA relevance

**Very high as a candidate substrate.**

Especially interesting because GAIA's semantic distinction:

```text
Collaborator
Capability
Context
Execution
```

could sit **above** such a typed runtime rather than requiring GAIA to implement all mechanics itself.

---

# D.3 LangGraph

[LangGraph repository](https://github.com/langchain-ai/langgraph?utm_source=chatgpt.com)

LangGraph focuses on orchestration:

* durable execution;
* persistence;
* streaming;
* human-in-the-loop;
* stateful workflows;
* graph-based agent execution. ([GitHub][5])

### GAIA relevance

**High for orchestration.**

But this is precisely where GAIA should be careful.

LangGraph can implement execution topology.

It does not establish that:

```text
GAIA Collaborator
=
LangGraph Agent
```

That would invert the abstraction boundary.

---

# D.4 Google ADK

[Google ADK repository](https://github.com/google/adk-python?utm_source=chatgpt.com)

ADK now provides:

* agents;
* tools;
* workflows;
* sessions;
* memory;
* multi-agent delegation;
* human-in-the-loop;
* task agents;
* local development UI;
* deployment mechanisms. ([GitHub][6])

Its architecture explicitly separates Agent, Runner, Tool, Session and Memory. ([GitHub][7])

### GAIA relevance

**Very high feature overlap.**

But Google-centric defaults and ADK's own conceptual model mean adoption would require careful boundary mapping.

---

# D.5 OpenAI Agents SDK

[OpenAI Agents SDK repository](https://github.com/openai/openai-agents-python?utm_source=chatgpt.com)

Provides:

* Agents;
* tools;
* handoffs;
* guardrails;
* human-in-the-loop;
* sessions;
* tracing;
* sandbox agents. ([GitHub][8])

### GAIA relevance

**High capability overlap, lower strategic fit** if GAIA intends to remain strongly model/provider neutral.

The technology can be useful, but making it GAIA's conceptual foundation would conflict with GAIA's stated model/framework neutrality.

---

# D.6 CrewAI

[CrewAI repository](https://github.com/crewAIInc/crewAI?utm_source=chatgpt.com)

CrewAI explicitly models agents as specialized team members with roles, goals, tools, collaboration and delegation. ([GitHub][9])

### GAIA relevance

**Conceptually relevant, architecturally dangerous as a definition.**

GAIA already has a Collaborator concept.

Therefore CrewAI can demonstrate that this capability is **not technically unique**.

But adopting CrewAI's terminology/model wholesale risks making:

```text
Crew
Agent
Role
Task
Process
Memory
```

become GAIA's architecture by accident.

---

# D.7 Open WebUI

[Open WebUI repository](https://github.com/open-webui/open-webui?utm_source=chatgpt.com)

Open WebUI already provides a substantial self-hosted interface layer with:

* tools;
* functions;
* memory;
* knowledge retrieval;
* MCP;
* OpenAPI;
* model routing;
* custom integrations. ([GitHub][10])

### GAIA relevance

**Very high as a host/UI/integration layer.**

It is particularly interesting for GAIA because GAIA does **not** need to invent a conversational UI merely to expose agents.

But Open WebUI should remain:

```text
HOST / INTERFACE
```

rather than:

```text
GAIA IDENTITY
```

---

# D.8 MCP

[Model Context Protocol specification](https://github.com/modelcontextprotocol/modelcontextprotocol?utm_source=chatgpt.com)

MCP now standardizes:

* Resources;
* Prompts;
* Tools;
* capability negotiation;
* client/server boundaries;
* context exposure.

Its current specification explicitly distinguishes:

```text
Resources → application-controlled
Tools     → model-controlled
Prompts   → user-controlled
```

and emphasizes user consent/control. ([GitHub][11])

### GAIA relevance

**Very high as an interoperability boundary.**

This is probably one of the clearest examples of something GAIA should **not reinvent**.

But MCP does not define:

* GAIA authority;
* GAIA Resource semantics;
* GAIA Collaborator identity;
* Project Knowledge lifecycle.

MCP is a protocol.

GAIA's semantic model can sit above it.

---

# D.9 Microsoft Agent Governance Toolkit

[Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit?utm_source=chatgpt.com)

This project is particularly important because it attacks an area GAIA has spent substantial engineering effort on:

* runtime policy enforcement;
* identity;
* audit;
* zero-trust;
* execution controls;
* reliability governance.

It is designed to operate across agent frameworks and is MIT licensed. ([GitHub][12])

### GAIA relevance

**Very high for governance infrastructure.**

It does not remove the need for GAIA's semantic ownership model.

But it substantially weakens the case for GAIA building its own low-level runtime governance mechanisms.

---

# D.10 LlamaIndex

LlamaIndex remains relevant primarily for:

* knowledge/data access;
* retrieval;
* agent workflows;
* data-oriented agent applications.

The important architectural observation is the same:

**knowledge/retrieval infrastructure is increasingly commodity infrastructure.**

GAIA's Project Knowledge authority model remains a different question.

---

# E. BUILD vs ADOPT

| GAIA Requirement                       | Existing OSS                              | Evidence                |                 Adopt |      Adapt |                     Build | Confidence  |
| -------------------------------------- | ----------------------------------------- | ----------------------- | --------------------: | ---------: | ------------------------: | ----------- |
| Agent execution loop                   | OpenHands / PydanticAI / ADK / Agents SDK | mature OSS              |               **YES** |      maybe |                    **NO** | High        |
| Tool calling                           | MCP / PydanticAI / ADK / others           | mature                  |               **YES** |      maybe |                    **NO** | High        |
| Agent delegation                       | ADK / OpenAI / LangGraph / CrewAI         | mature                  |               **YES** |      maybe |                    **NO** | High        |
| Workflow orchestration                 | LangGraph / ADK / Pydantic Graph          | mature                  |               **YES** |      maybe |                    **NO** | High        |
| Coding-agent workspace                 | OpenHands                                 | mature                  |               **YES** |    **YES** |                    **NO** | High        |
| Host/UI                                | Open WebUI / OpenHands Canvas             | mature                  |               **YES** |    **YES** |                    **NO** | High        |
| Tool interoperability                  | MCP                                       | standardizing ecosystem |               **YES** |    **YES** |                    **NO** | High        |
| Runtime governance                     | Microsoft AGT / framework guardrails      | increasingly mature     |               **YES** |    **YES** |          **NO initially** | High        |
| Typed agent contracts                  | PydanticAI                                | mature                  |               **YES** |    **YES** |                    **NO** | High        |
| Agent tracing/evals                    | PydanticAI / OpenAI / ADK                 | mature                  |               **YES** |    **YES** |                    **NO** | High        |
| Local model execution                  | Ollama / llama.cpp / vLLM etc.            | mature                  |               **YES** |    **YES** |                    **NO** | High        |
| Host readiness                         | system tooling + GAIA experience          | generic engineering     | adopt generic tooling |    **YES** | limited GAIA wrapper only | High        |
| Evidence packaging                     | Git/CI/artifact tooling                   | generic                 |               **YES** |    **YES** |            no new runtime | High        |
| GAIA Agent Identity                    | no direct equivalent                      | GAIA identity docs      |                     — |          — |                   **YES** | High        |
| GAIA Authority semantics               | no direct equivalent                      | governance + ADRs       |                     — |          — |                   **YES** | High        |
| GAIA Collaborator semantic contract    | frameworks have approximations            | W3                      |                     — |    **YES** |    **YES semantic layer** | High        |
| GAIA Capability semantic contract      | partial equivalents                       | W3                      |                     — |    **YES** |    **YES semantic layer** | High        |
| GAIA Resource/authority model          | no direct equivalent                      | post-W3                 |                     — |          — |                   **YES** | High        |
| GAIA Project Knowledge authority model | no direct equivalent found                | recent PK work          |                     — |          — |                   **YES** | High        |
| GAIA durable identity across hosts     | not solved by frameworks                  | `IDENTITY.md`           |                     — |          — |                   **YES** | High        |
| GAIA domain semantics                  | domain-specific                           | future Domotics         |                     — |    **YES** |    **YES where semantic** | Medium/High |
| GAIA Memory architecture               | many OSS solutions                        | GAIA currently OPEN     |          **evaluate** | **likely** |     **not justified yet** | High        |
| GAIA cross-host behavior               | components support interfaces             | identity requirement    |   **adopt substrate** |  **adapt** |       semantic layer only | High        |

---

# F. GAIA DIFFERENTIATION

This is the most important result.

After maximum reasonable OSS reuse, GAIA's differentiating layer is **not**:

* an LLM runtime;
* a workflow engine;
* a tool protocol;
* a coding agent;
* a chat UI;
* a sandbox;
* an agent graph;
* an MCP server framework;
* a model router.

Those are increasingly available.

## GAIA's likely differentiating core

```text
                 GAIA
                   │
        ┌──────────┴──────────┐
        │                     │
   SEMANTIC MODEL          GOVERNANCE
        │                     │
 Collaborator             Authority
 Capability               Human ownership
 Resource                 Evidence
 Context                  Approval
 Domain                   Provenance
        │                     │
        └──────────┬──────────┘
                   │
             PROJECT KNOWLEDGE
                   │
             CURRENT / HISTORY
             / PROVENANCE
                   │
        ┌──────────┴──────────┐
        │                     │
    OSS RUNTIME           OSS HOSTS
        │                     │
 OpenHands/Pydantic      Open WebUI/etc.
 LangGraph/ADK/etc.
        │
       MCP
        │
 tools / models / systems
```

### In other words

**GAIA should own the meaning.**

External software can own much of the machinery.

That is strongly consistent with the project's already-established principle that GAIA should remain independent of frameworks and that research must not silently become architecture. 

---

# G. KNOWLEDGE GAPS

Only genuine gaps are listed.

## GAP-001 — Final runtime substrate

GAIA has not established whether it should use:

* OpenHands;
* PydanticAI;
* LangGraph;
* ADK;
* another runtime;
* composition of several.

**Why it matters:** large amounts of historical engineering work could become unnecessary if a mature substrate is selected.

**Status:** UNKNOWN / OPEN.

---

## GAP-002 — Collaborator lifecycle

The Project Knowledge authority matrix explicitly marks creator/lifecycle as **OPEN / PARTIAL**. 

This is more important than choosing a framework.

Until this is defined, mapping:

```text
GAIA Collaborator
→ framework Agent
```

would be premature.

---

## GAP-003 — Memory architecture

Still **UNKNOWN / OPEN**. 

OSS has many memory mechanisms, but GAIA has not yet established what *memory means semantically*.

Therefore:

**do not select a memory technology merely because it exists.**

---

## GAP-004 — Project Knowledge implementation boundary

The governance model is increasingly clear.

The implementation mechanism is not.

The current documentation reconciliation explicitly identifies Git ↔ Project Knowledge synchronization as a process gap rather than an implemented architecture. 

---

## GAP-005 — Final 3090 role

Still open/partial. 

This matters because otherwise hardware topology risks influencing architecture.

---

## GAP-006 — Final model policy

Still open/partial.

The current Qwen3-Coder 30B selection is explicitly provisional. 

---

## GAP-007 — Complete historical software research

The software research reconciliation itself says complete software/tool inventory remains partial/unknown. 

This review materially reduces that gap, but does not close it.

---

# H. CONTRADICTIONS

## H.1 No fundamental architectural contradiction found

I do **not** find evidence that GAIA's accepted semantic architecture conflicts with the current OSS landscape.

Quite the opposite.

The landscape now makes the separation clearer.

---

## H.2 Historical tension: building runtime vs semantic architecture

There is, however, a **historical tension**:

```text
GAIA historically:
    needed an Engineer
        ↓
    needed a runtime
        ↓
    built bounded runtime/tooling
```

versus the current landscape:

```text
Mature OSS now provides:
    agent runtime
    workspace
    tools
    orchestration
    tracing
    governance
    MCP
    host/UI
```

The correct conclusion is **not** that historical work was wrong.

It established:

* requirements;
* operational constraints;
* evidence discipline;
* failure modes;
* acceptance boundaries.

But it may no longer justify owning all of the implementation.

This is exactly the ING_3090 lesson the prompt asks us to apply.

---

# I. ING_3090 LESSON — WHAT SHOULD SURVIVE?

## Things GAIA actually needed

These appear durable:

* bounded Engineer execution;
* explicit authority;
* evidence;
* Git provenance;
* human handoff;
* security preflight;
* reproducibility;
* test lineage;
* historical/current distinction;
* safe stop conditions.

The recent Engineer reconstruction calls out evidence-vs-architecture, technical capability-vs-authorization, Human Owner validation, legacy-as-evidence and reusable host/security tooling as major lessons. 

## Things that were primarily environmental

* RTX 3090-specific setup;
* GTX 1070-specific preparation;
* Ollama details;
* Qwen-specific selection;
* Docker/Compose topology;
* VS Code integration;
* local packaging mechanics.

## Things that were scaffolding

Potentially:

* portions of the custom coding-agent runtime;
* custom orchestration mechanisms;
* duplicated host abstractions;
* custom tool plumbing where MCP/framework tooling is now mature.

This requires a future artifact-by-artifact comparison before declaring anything obsolete.

---

# J. THE BIG RECONCILIATION

The project appears to have been solving **two layers simultaneously**:

### Layer 1 — Agent machinery

```text
LLM
↓
agent loop
↓
tools
↓
workspace
↓
execution
↓
tests
↓
evidence
```

### Layer 2 — GAIA meaning

```text
Human Owner
↓
Authority
↓
Collaborator
↓
Capability
↓
Resource
↓
Context
↓
Domain
↓
Project Knowledge
↓
Evidence / provenance
```

The first layer is increasingly commoditized.

The second remains substantially GAIA-specific.

That is the strongest conclusion of this landscape review.

---

# K. RECOMMENDATION TO TRIANGULATION

Not an implementation recommendation.

These are the questions I would put to **Architect + Senior Engineer**.

## TRI-001 — What exactly must GAIA own?

Ask:

> Which current GAIA components exist because they express GAIA semantics, rather than because the project needed an implementation vehicle?

This should be answered component-by-component.

---

## TRI-002 — Can the existing E2 runtime be replaced?

Not:

> "Can we use OpenHands?"

Instead:

> "Which E2 contracts must survive independently of the runtime?"

Then compare those contracts against:

* OpenHands;
* PydanticAI;
* LangGraph;
* ADK.

---

## TRI-003 — What is the canonical Collaborator contract?

Before choosing a runtime:

```text
What makes something a GAIA Collaborator?
```

If the answer can be expressed independently of Python classes, framework Agents, prompts or models, GAIA has preserved its architectural boundary.

---

## TRI-004 — What is the canonical Capability contract?

Likewise:

```text
Capability
    ≠
tool
    ≠
function
    ≠
MCP tool
    ≠
framework action
```

The OSS ecosystem can implement execution.

GAIA should determine whether the semantic Capability contract remains GAIA-owned.

---

## TRI-005 — Is Project Knowledge a semantic subsystem or a repository view?

The current evidence strongly suggests the former conceptually, but the implementation is unresolved.

Architect should answer:

> Is Project Knowledge merely curated context, or is it a first-class GAIA semantic concept with lifecycle/provenance/authority?

---

## TRI-006 — What should disappear?

This is the question GAIA historically has not been able to answer confidently.

For each custom component:

```text
KEEP
REPLACE WITH OSS
WRAP OSS
DEPRECATE
UNKNOWN
```

That should be decided from evidence, not enthusiasm for a particular framework.

---

# FINAL STATUS

## WHERE IS GAIA TODAY?

GAIA is **not at the beginning of the agent-runtime problem anymore**.

It has:

* a durable identity;
* a bounded conceptual architecture;
* demonstrated W3 semantics;
* demonstrated bounded Capability/Collaborator concepts;
* operational Engineer experience;
* strong evidence/governance discipline;
* physical 1070 evidence;
* a functioning 3090 engineering environment;
* reusable host-readiness/process knowledge;
* a clarified Project Knowledge authority boundary.

At the same time:

* Collaborator lifecycle is open;
* Memory is open;
* Resource resolution is partial;
* final runtime topology is open;
* final 3090 role is open;
* model policy is open;
* Project Knowledge synchronization is not established. 

---

# WHAT CHANGED SINCE THE OLD SPRINT 4/5 BASELINE?

The major change is conceptual maturity.

Old trajectory:

```text
GAIA
 ↓
need agents
 ↓
need runtime
 ↓
need host
 ↓
need model
 ↓
build infrastructure
```

Current trajectory:

```text
GAIA identity
      ↓
semantic contracts
      ↓
authority / governance
      ↓
evidence
      ↓
select/adapt external runtime
      ↓
models / tools / hosts become replaceable
```

The project has consequently accumulated **much more evidence that it should own the semantic and governance boundary, and much less evidence that it should own the entire agent machinery**.

---

# DECISION SPACE FOR THE HUMAN OWNER

I would **not** conclude "STOP GAIA".

I would also **not** conclude "continue building the current custom runtime".

The evidence points toward:

## **REFOCUS + ADOPT / ADAPT**

with this conceptual direction:

```text
DO NOT REBUILD
    agent runtime
    orchestration
    generic tool protocol
    generic UI
    generic tracing
    generic governance
    generic model execution

DO BUILD / OWN
    GAIA identity
    GAIA semantic contracts
    GAIA authority model
    GAIA Project Knowledge semantics
    GAIA-specific provenance / evidence semantics
    GAIA domain semantics where genuinely unique

ADOPT / ADAPT
    agent runtime
    coding workspace
    orchestration
    MCP
    UI/host
    model runtime
    governance primitives
    observability/evaluation
```

**Confidence: HIGH on the direction; MEDIUM on which specific OSS substrate should eventually be selected.**

The next architectural question is therefore **not "Which framework should GAIA use?"**

It is:

> **"What is the smallest GAIA-owned semantic kernel that remains after we deliberately remove everything an existing mature open-source component can responsibly provide?"**

That is the triangulation question most likely to prevent GAIA from rebuilding infrastructure that the ecosystem now already supplies.

[1]: https://github.com/OpenHands/docs/blob/main/sdk/arch/design.mdx?utm_source=chatgpt.com "docs/sdk/arch/design.mdx at main · OpenHands/docs · GitHub"
[2]: https://github.com/OpenHands/OpenHands/blob/main/README.md?plain=1&utm_source=chatgpt.com "OpenHands/README.md at main · OpenHands/OpenHands · GitHub"
[3]: https://github.com/pydantic/pydantic-ai/?utm_source=chatgpt.com "GitHub - pydantic/pydantic-ai: How Python does AI: agents, realtime voice, image generation, embeddings. Every model, every interface, typed end to end. · GitHub"
[4]: https://github.com/pydantic/pydantic-ai/blob/main/docs/agent.md?utm_source=chatgpt.com "pydantic-ai/docs/agent.md at main · pydantic/pydantic-ai · GitHub"
[5]: https://github.com/langchain-ai/langgraph/blob/main/libs/langgraph/README.md?utm_source=chatgpt.com "langgraph/libs/langgraph/README.md at main · langchain-ai/langgraph · GitHub"
[6]: https://github.com/google/adk-python?utm_source=chatgpt.com "GitHub - google/adk-python: An open-source, code-first Python toolkit for building, evaluating, and deploying sophisticated AI agents with flexibility and control. · GitHub"
[7]: https://github.com/google/adk-python/blob/main/AGENTS.md?utm_source=chatgpt.com "adk-python/AGENTS.md at main · google/adk-python · GitHub"
[8]: https://github.com/openai/openai-agents-python/blob/main/docs/index.md?utm_source=chatgpt.com "openai-agents-python/docs/index.md at main · openai/openai-agents-python · GitHub"
[9]: https://github.com/crewaiinc/crewai/blob/main/docs/en/concepts/agents.mdx?utm_source=chatgpt.com "crewAI/docs/en/concepts/agents.mdx at main · crewAIInc/crewAI · GitHub"
[10]: https://github.com/open-webui/docs/blob/main/docs/features/extensibility/plugin/tools/index.mdx?utm_source=chatgpt.com "docs/docs/features/extensibility/plugin/tools/index.mdx at main · open-webui/docs · GitHub"
[11]: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/index.mdx?utm_source=chatgpt.com "modelcontextprotocol/docs/specification/2026-07-28/index.mdx at main · modelcontextprotocol/modelcontextprotocol · GitHub"
[12]: https://github.com/microsoft/agent-governance-toolkit/blob/main/README.md?utm_source=chatgpt.com "agent-governance-toolkit/README.md at main · microsoft/agent-governance-toolkit · GitHub"

