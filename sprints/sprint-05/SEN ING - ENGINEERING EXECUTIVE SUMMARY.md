# A. ENGINEERING EXECUTIVE SUMMARY

**Recommendation: HYBRID / REFOCUS**

La conclusione più importante è:

> **GAIA non dovrebbe costruire un nuovo general-purpose Agent Framework.**

Il materiale GAIA supporta già una separazione molto più sana:

```text
GAIA owns
    ↓
contracts
evidence semantics
governance
authority boundaries
GAIA-specific knowledge
validation semantics
bounded adapters
    ↓
OSS / external systems provide
    ↓
agent runtime
model serving
workflow execution
UI / host
durable state
tool transport
```

Questo è coerente con la ricerca GAIA già riconciliata: la filosofia recuperata è precisamente **research existing technology before rebuilding it**, mantenendo GAIA proprietaria dei contratti semantici, evidence/trace semantics e bounded adapter interfaces. 

Inoltre, Toolkit V0.1 è stato deliberatamente congelato come **analysis/evidence layer**, non come runtime. La specifica esclude esplicitamente Agent, Provider, Registry, Planner, Memory, Workflow, Plugin e orchestration architecture. 

Quindi non vedo oggi una giustificazione tecnica per trasformare GAIA Toolkit in un framework agente.

### La mia raccomandazione sintetica

| Area                   | Decisione                              |
| ---------------------- | -------------------------------------- |
| Agent runtime          | **ADOPT / ADAPT**                      |
| Coding-agent runtime   | **ADOPT / ADAPT**                      |
| Tool execution         | **ADOPT**, con GAIA policy wrapper     |
| Git                    | **ADAPT**                              |
| Testing                | **KEEP + ADAPT**                       |
| Evidence               | **BUILD / KEEP**                       |
| Governance             | **BUILD**                              |
| Authority              | **BUILD**                              |
| Project Knowledge      | **KEEP / ADAPT**                       |
| Memory                 | **DEFER / ADOPT later**                |
| Workflow               | **ADOPT**, only when actually needed   |
| Host UI                | **ADOPT**                              |
| Machine profiles       | **KEEP / ADAPT**                       |
| Model abstraction      | **ADOPT**                              |
| Skills                 | **ADAPT**, not a GAIA framework yet    |
| Collaborators          | **DEFER**                              |
| Deployment             | **ADOPT external infrastructure**      |
| Validation             | **KEEP / ADAPT**                       |
| Human approval         | **BUILD as GAIA policy boundary**      |
| Cross-host consistency | **BUILD semantic contract + adapters** |

---

# B. CURRENT GAIA COMPONENT ANALYSIS

## 1. Toolkit V0.1 — **KEEP**

Questo è uno dei componenti che **non eliminerei**.

Il suo valore non è essere un framework AI: è possedere i contratti GAIA per:

```text
Observation
Evidence
Requirement
Requirement Analysis
Candidate
Recommendation
Sanitization
```

La final review ha esplicitamente congelato questo boundary. 

### KEEP

Ma con una precisazione:

**non trasformarlo nel runtime dell'Agent.**

Il Toolkit deve rimanere un library/tooling boundary utilizzabile da runtime diversi.

---

## 2. Host Check V0.1 — **KEEP / INTEGRATE**

Non manterrei necessariamente tutta la sua implementazione storica come framework permanente.

Terrei:

* evidence schema;
* observation semantics;
* provenance;
* security/sanitization;
* validated fixtures;
* host-specific adapters dove servono.

Scarterei progressivamente:

* command implementation duplicata;
* host-specific orchestration;
* POC-specific control flow.

La stessa specifica Toolkit dice di estrarre **behavioral contracts**, non implementation details dei POC. 

---

## 3. Software / Skill Discovery V0.2 — **KEEP / INTEGRATE**

Stesso ragionamento.

Conserverei:

```text
requirement
→ deterministic mapping
→ evidence
→ candidate
→ recommendation
```

Non conserverei come architettura:

```text
legacy discovery implementation
research implementation
specific repository paths
specific candidate examples
```

La distinzione è già stata congelata: `UNKNOWN` non può diventare `AVAILABLE`, e candidate/recommendation non equivalgono a authorization. 

---

## 4. Local Engineer V0.1.1 — **WRAP / INTEGRATE**

Questo è più interessante.

Non lo trasformerei nel GAIA Agent runtime.

Lo vedrei come:

```text
external/local agent runtime
        ↓
Local Engineer capabilities
        ↓
GAIA Toolkit
        ↓
GAIA evidence/governance
```

La roadmap attuale identifica Local Engineer V0.1.1 come bounded, accepted implementation sopra Toolkit. 

Quindi **non buttare via il lavoro**.

Ma nemmeno elevarlo automaticamente a “GAIA Agent Framework”.

---

## 5. E2 / 3090 runtime — **ADOPT AS HOST CONTEXT, NOT ARCHITECTURE**

Il 3090 + Ollama + Qwen3-Coder è un deployment/runtime context.

Il documento E2 lo dice esplicitamente: E2 è una coding-agent continuity milestone, non una nuova GAIA architectural layer; Ollama è un local model-serving runtime e non un GAIA component. 

Quindi:

```text
3090
Ollama
Qwen
VS Code
```

sono sostituibili.

Non costruirei GAIA attorno a loro.

---

## 6. 1070 / HC tooling — **INTEGRATE**

Il lavoro 1070 ha prodotto una cosa preziosa:

**physical evidence**.

Questa deve rimanere GAIA-owned come **evidence contract**, non come host runtime framework.

La distinzione attuale è corretta:

```text
1070 = physical target
3090 = engineer environment
```

ma questi ruoli non devono diventare GAIA architecture.

---

# C. OSS LANDSCAPE

Ho verificato soprattutto i progetti che possono realmente eliminare lavoro infrastrutturale.

## 1. [Pydantic AI](https://github.com/pydantic/pydantic-ai?utm_source=chatgpt.com) — **STRONG ADAPT CANDIDATE**

È probabilmente il candidato più interessante per GAIA se si vuole un runtime Python relativamente piccolo.

Attualmente offre:

* agent loop;
* typed tools;
* model abstraction;
* MCP;
* human-in-the-loop approvals;
* capabilities;
* durable execution integrations;
* testing/evals;
* observability;
* local model providers inclusa Ollama. ([GitHub][1])

È MIT licensed e dichiara Python 3.10+ e stato `Production/Stable`. ([GitHub][2])

### Per GAIA

Non lo userei come “GAIA architecture”.

Lo userei eventualmente come:

```text
GAIA Engineer
    ↓
Pydantic AI runtime
    ↓
GAIA tools / Toolkit
```

**Recommendation: ADAPT**

È il candidato che meglio si adatta alla filosofia “GAIA owns contracts, external runtime owns agent loop”.

---

## 2. [LangGraph](https://github.com/langchain-ai/langgraph?utm_source=chatgpt.com) — **ADOPT ONLY IF WORKFLOW STATE BECOMES REAL**

LangGraph è molto forte per:

* graph/state execution;
* durable state;
* persistence;
* human-in-loop;
* resumability;
* complex agent workflows.

La documentazione attuale descrive checkpoint e stores per continuità, recovery e long-running workflows. ([GitHub][3])

È MIT licensed. ([GitHub][4])

Il repository mostra attività/release molto ampia. ([GitHub][5])

### Problema per GAIA

È facile usarlo per introdurre:

```text
Workflow
Planner
State machine
Orchestration
Memory
```

prima che GAIA abbia dimostrato di averne bisogno.

**Recommendation: DEFER / ADOPT LATER**

Non lo introdurrei ora.

---

## 3. [OpenHands](https://github.com/OpenHands/OpenHands?utm_source=chatgpt.com) — **ADOPT/ADAPT FOR CODING, NOT CORE**

OpenHands è molto più vicino all'esperienza E2.

Offre un coding-agent environment, terminal/tool interaction, local LLM support e sandbox/runtime concepts. La documentazione conferma supporto a local LLM tramite Ollama, vLLM, LM Studio e SGLang. ([GitHub][6])

La parte principale del repository è MIT licensed, con enterprise directory separata. ([GitHub][7])

### Potenziale

Potrebbe eliminare una quantità significativa di lavoro che GAIA rischierebbe di reinventare:

```text
coding loop
terminal interaction
repo interaction
agent execution
local model integration
```

### Ma

OpenHands è un **coding-agent product/runtime**, non un GAIA semantic/governance layer.

Quindi:

**ADAPT**, non **BUILD ON AS GAIA CORE**.

---

## 4. [Open WebUI](https://github.com/open-webui/open-webui?utm_source=chatgpt.com) — **ADOPT AS HOST/UI**

È molto interessante per il problema già emerso con:

```text
3090
1070
VS Code
Human Owner
local models
```

Open WebUI supporta Ollama e OpenAI-compatible APIs. ([GitHub][8])

Ma attenzione: la licenza attuale non è semplicemente MIT/BSD per tutto il repository. Le versioni recenti hanno una specifica branding restriction e una storia di licenze differenziata. ([GitHub][9])

### Recommendation

**ADOPT AS HOST**, non come GAIA runtime.

E farei una review legale/licensing prima di una distribuzione GAIA modificata.

---

## 5. MCP — **ADOPT**

MCP è probabilmente uno dei casi più chiari di:

> **non reinventare.**

GAIA non dovrebbe creare un proprio protocollo universale per tool/resource integration se MCP soddisfa il bisogno.

Il Toolkit può mantenere i propri semantic contracts sopra MCP.

Quindi:

```text
GAIA semantic tool contract
        ↓
MCP adapter
        ↓
external tool
```

**ADOPT selectively.**

---

## 6. OpenAI Agents SDK — **ADOPT/ADAPT, CONTEXT-DEPENDENT**

È un candidato valido per agent loop/tool/handoff/guardrail patterns.

Ma il problema GAIA non è trovare “un altro agent SDK”.

La domanda è:

> quale runtime minimizza il codice GAIA senza imporre una semantica incompatibile?

Per ora non abbiamo abbastanza evidence per preferirlo definitivamente a Pydantic AI.

**Recommendation: ADAPT candidate, not selected.**

---

## 7. Google ADK — **ADOPT/ADAPT candidate**

Stesso discorso.

Buon candidato per runtime/tools/workflows, ma non c'è evidence sufficiente per dire che GAIA debba standardizzarsi su ADK.

**DEFER selection.**

---

## 8. LlamaIndex — **ADOPT ONLY IF KNOWLEDGE/RETRIEVAL BECOMES REQUIRED**

LlamaIndex è interessante soprattutto per:

* retrieval;
* data connectors;
* RAG;
* knowledge-oriented applications;
* agent/tool composition.

Ma GAIA non ha ancora una Memory/Knowledge runtime architecture definitiva. La roadmap dichiara ancora Memory e Resource resolution come future/open. 

Quindi introdurlo oggi rischierebbe di trasformare una futura esigenza in architettura attuale.

**DEFER.**

---

## 9. CrewAI — **IGNORE FOR NOW**

È orientato molto verso multi-agent orchestration.

GAIA non ha evidence sufficiente per introdurre un Collaborator/Agent orchestration runtime.

**IGNORE for current phase.**

---

## 10. Microsoft Agent Governance Toolkit — **RESEARCH / ADAPT SELECTIVELY**

La parte interessante non sarebbe usarlo come runtime, ma confrontare le sue policy/governance patterns con il GAIA governance model.

**RESEARCH / ADAPT selectively.**

Non lo adotterei come core.

---

# D. BUILD / ADOPT MATRIX

| Capability             | Existing OSS                               | Engineering Cost to Build | Integration Cost | Recommendation                             |
| ---------------------- | ------------------------------------------ | ------------------------: | ---------------: | ------------------------------------------ |
| Agent runtime          | Pydantic AI / OpenHands / ADK / Agents SDK |                 Very High |         Moderate | **ADOPT/ADAPT**                            |
| Coding agent           | OpenHands                                  |                 Very High |         Moderate | **ADAPT**                                  |
| Tool execution         | Pydantic AI / MCP                          |                      High |     Low–Moderate | **ADOPT**                                  |
| Git interaction        | existing Git + OSS agent tooling           |                      High |              Low | **ADAPT**                                  |
| Testing                | pytest + existing GAIA tests               |                       Low |              Low | **KEEP**                                   |
| Evidence semantics     | no generic OSS substitute sufficient       |                      High |             High | **BUILD / KEEP**                           |
| Governance             | partial OSS options                        |                 Very High |             High | **BUILD GAIA layer**                       |
| Authority              | generic frameworks insufficient            |                      High |         Moderate | **BUILD**                                  |
| Project Knowledge      | RAG/knowledge tools exist                  |                      High |             High | **KEEP GAIA semantics; ADOPT infra later** |
| Memory                 | LangGraph/Pydantic/others                  |                      High |         Moderate | **DEFER**                                  |
| Workflow               | LangGraph/Temporal/etc.                    |                 Very High |             High | **DEFER**                                  |
| Host UI                | Open WebUI                                 |                 Very High |         Moderate | **ADOPT**                                  |
| Machine profile        | host-readiness tooling                     |                  Moderate |              Low | **KEEP/ADAPT**                             |
| Model abstraction      | Pydantic AI / LiteLLM-like layer           |                      High |              Low | **ADOPT**                                  |
| Skills                 | MCP/toolsets/capabilities                  |                      High |         Moderate | **ADAPT**                                  |
| Collaborators          | CrewAI/LangGraph/etc.                      |                 Very High |             High | **DEFER**                                  |
| Deployment             | Docker/systemd/etc.                        |                 Very High |         Moderate | **ADOPT external**                         |
| Validation             | pytest + GAIA Toolkit                      |                      High |              Low | **KEEP**                                   |
| Human approval         | framework features exist                   |                  Moderate |         Moderate | **BUILD GAIA policy boundary**             |
| Cross-host consistency | no OSS solution matches GAIA semantics     |                 Very High |             High | **BUILD contract + adapters**              |

---

# E. GAIA-SPECIFIC CODE

If we deleted most current infrastructure and maximized OSS reuse, **GAIA would still need a surprisingly small but important core**.

I would keep approximately these layers:

```text
                 GAIA SEMANTIC CORE
                        │
        ┌───────────────┼────────────────┐
        │               │                │
    Evidence        Governance       Knowledge
    contracts       / authority       contracts
        │               │                │
        └───────────────┼────────────────┘
                        │
                  GAIA Toolkit
                        │
                adapters / tools
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
   Agent runtime     MCP tools       host adapters
```

### GAIA should still own

**1. Evidence model**

Because this is one of the clearest GAIA-specific assets already demonstrated. Toolkit explicitly requires provenance and uncertainty. 

**2. Governance**

Because external frameworks cannot know GAIA's:

```text
Human Owner
Architect
Engineer
Project Knowledge
authorization
acceptance
```

hierarchy.

**3. Authority semantics**

Especially:

```text
recommendation ≠ authorization
evidence ≠ authorization
unknown ≠ available
```

These are GAIA contracts, not generic agent-runtime features.

**4. Validation semantics**

The exact meaning of GAIA evidence/result states remains GAIA-owned.

**5. Project Knowledge integration**

Not necessarily the database/vector engine, but:

```text
what is authoritative?
what is historical?
what is derived?
what is accepted?
what is proposed?
```

That semantic layer is GAIA-specific.

**6. Bounded adapters**

For:

* Toolkit;
* Git;
* MCP;
* host;
* physical target;
* future runtime.

---

# F. MAINTENANCE BURDEN

The biggest current risk is **not that GAIA has too little code**.

It is that GAIA could accidentally own too much infrastructure.

## Highest-risk reinvention

### 1. Agent runtime

**Do not build.**

An agent loop looks deceptively small:

```text
LLM
→ tool call
→ result
→ LLM
→ tool call
```

but production ownership expands into:

* retries;
* cancellation;
* state;
* tool schemas;
* streaming;
* persistence;
* approvals;
* model compatibility;
* tracing;
* concurrency;
* failure recovery;
* context management;
* security.

This is exactly the sort of infrastructure Pydantic AI, LangGraph and OpenHands already maintain. ([GitHub][1])

---

### 2. Workflow engine

**Do not build.**

If GAIA eventually needs durable workflows, use a mature external engine/runtime.

---

### 3. UI

**Do not build a GAIA UI first.**

Open WebUI already provides a useful self-hosted local-model interface, though its current licensing deserves explicit review before productization. ([GitHub][8])

---

### 4. Tool protocol

**Do not invent a GAIA-MCP equivalent.**

Adopt MCP where its semantics fit.

---

### 5. Model routing

**Do not build a model/provider abstraction prematurely.**

Use an existing runtime abstraction and keep GAIA's model selection semantics outside it.

---

# G. TECHNICAL RISKS

## 1. OSS lock-in — HIGH

Ironically, adopting everything could create the opposite problem:

```text
GAIA
 ↓
LangChain
 ↓
LangGraph
 ↓
Pydantic
 ↓
MCP
 ↓
provider abstraction
 ↓
model runtime
```

This can become an ecosystem stack rather than simplification.

### Mitigation

Adopt **interfaces**, not entire ecosystems.

---

## 2. Abandoned dependency — MEDIUM/HIGH

Open-source agent ecosystems move extremely quickly.

Example: OpenHands' standalone CLI repository now explicitly says it is no longer actively maintained and points users toward another project. ([GitHub][10])

This is exactly why GAIA should avoid making a particular runtime part of its identity.

---

## 3. Security — HIGH

Agent runtimes that execute:

```text
shell
filesystem
Git
network
```

are security-sensitive.

GAIA's current Toolkit security boundary is much stronger and should remain authoritative. The Toolkit explicitly prohibits secret values and mutation outside its boundary. 

---

## 4. Local model limitations — MEDIUM

Local agents are possible, but model quality and tool-use reliability vary.

OpenHands itself notes that effective local LLM use requires capable hardware and agent-capable models. ([GitHub][6])

Therefore:

```text
3090 + Qwen
```

should remain an empirical deployment configuration, not architecture.

---

## 5. Portability — MEDIUM

A runtime tightly coupled to:

* Ollama;
* Docker;
* NVIDIA;
* Linux;

will constrain GAIA unnecessarily.

The current E2 evidence already argues against that coupling. 

---

## 6. Upgrade burden — HIGH

Agent frameworks change rapidly.

Therefore:

```text
GAIA semantic contracts
        ↓
thin adapter
        ↓
runtime
```

is safer than:

```text
GAIA codebase
        ↓
deep framework internals
```

---

# H. MIGRATION DIFFICULTY

| Current capability              | Likely replacement        | Difficulty                      |
| ------------------------------- | ------------------------- | ------------------------------- |
| E2 coding loop                  | OpenHands/Pydantic AI     | **MODERATE**                    |
| Local model serving             | Ollama                    | **EASY**                        |
| Host UI                         | Open WebUI                | **EASY–MODERATE**               |
| Tool transport                  | MCP                       | **MODERATE**                    |
| Agent loop                      | Pydantic AI               | **MODERATE**                    |
| Durable workflow                | LangGraph/Temporal        | **HARD**                        |
| GAIA evidence semantics         | OSS replacement           | **VERY HARD / not recommended** |
| GAIA governance                 | OSS replacement           | **VERY HARD / not recommended** |
| Project Knowledge semantics     | RAG framework             | **HARD**                        |
| Validation                      | pytest + existing tooling | **EASY**                        |
| Git integration                 | native Git + adapter      | **EASY–MODERATE**               |
| Physical evidence               | current GAIA tooling      | **MODERATE**                    |
| Cross-host semantic consistency | custom GAIA contracts     | **HARD**                        |

The most important result is:

> **The things that are easiest to replace are precisely the things GAIA should avoid owning.**

And the things that are hardest to replace are precisely the things that appear to be genuinely GAIA-specific.

---

# I. RECOMMENDED STRATEGY

## **HYBRID / REFOCUS**

Not:

```text
BUILD GAIA Agent Framework
```

but:

```text
                         GAIA
                          │
        ┌─────────────────┼──────────────────┐
        │                 │                  │
    Semantics         Governance          Knowledge
        │                 │                  │
        └─────────────────┼──────────────────┘
                          │
                     GAIA Toolkit
                          │
                    thin adapters
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   Pydantic AI        OpenHands           MCP
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                 model/runtime layer
                          │
                Ollama / cloud / etc.
```

### Phase 1 — now

**KEEP**

* Toolkit V0.1;
* Local Engineer V0.1.1;
* evidence;
* validation;
* Git discipline;
* host-readiness evidence.

**DO NOT build**

* Agent framework;
* Memory;
* Workflow engine;
* Collaborator runtime;
* Provider registry;
* Plugin system.

---

### Phase 2 — targeted experiment

I would run **one bounded engineering experiment**:

> Replace only the E2 agent-loop implementation with an external runtime, while keeping GAIA Toolkit, evidence, validation and governance unchanged.

The strongest first candidate is **Pydantic AI**, with OpenHands as the alternative if the actual requirement is a full coding-agent environment rather than an SDK/runtime. Pydantic AI's typed tools, model abstraction, MCP, approvals, testing and durable-execution capabilities make it a particularly good fit for a thin GAIA adapter model. ([GitHub][1])

This experiment should answer:

```text
How much GAIA-specific code remains?
```

rather than:

```text
Which framework should GAIA adopt forever?
```

---

### Phase 3 — only if evidence demands it

Then investigate:

* LangGraph for durable workflows;
* Open WebUI for host/UI;
* MCP for tool interoperability;
* LlamaIndex for future knowledge/retrieval;
* external durable execution infrastructure.

Nothing here should become architecture merely because the experiment succeeds.

---

# J. QUESTIONS FOR ARCHITECT

These should **not** be resolved by engineering.

### Q1 — Is GAIA's strategic objective actually to own an Agent runtime?

Current evidence says **no demonstrated need**.

The Toolkit explicitly excludes it. 

---

### Q2 — Should GAIA standardize on one external Agent runtime?

I recommend **not yet**.

First establish the adapter contract.

---

### Q3 — Is Pydantic AI the preferred experimental runtime?

My engineering recommendation:

**Candidate: YES**

**Architecture decision: NOT YET**

---

### Q4 — Is OpenHands a runtime dependency or simply an engineering tool?

This distinction matters.

If OpenHands is merely:

```text
developer tool
```

GAIA doesn't need to integrate deeply with it.

If GAIA wants to operate a persistent autonomous coding loop, then its runtime model becomes relevant.

---

### Q5 — Does GAIA need durable workflow state?

Currently **not sufficiently demonstrated**.

LangGraph/Temporal should therefore remain deferred.

---

### Q6 — Does GAIA need a GAIA Memory architecture?

Current Project Knowledge still marks Memory as future/open. 

Therefore do not let a framework's built-in memory capability force the decision.

---

### Q7 — Should Open WebUI become the standard GAIA host?

Not yet.

It is technically attractive, especially for local models, but the current license/branding conditions require deliberate evaluation. ([GitHub][9])

---

# FINAL ENGINEERING POSITION

The strongest conclusion from this review is:

```text
GAIA SHOULD NOT BUILD WHAT THE ECOSYSTEM ALREADY MAINTAINS WELL.
GAIA SHOULD BUILD WHAT DEFINES GAIA.
```

And the current evidence gives a fairly clean boundary.

### GAIA should own

```text
Evidence
Governance
Authority
Validation semantics
Project Knowledge semantics
GAIA-specific contracts
Bounded adapters
```

### GAIA should reuse

```text
Agent loop
Tool protocol
Model interface
Coding environment
UI
Workflow engine
Durable execution
Vector/RAG infrastructure
Model serving
Container infrastructure
```

### GAIA should defer

```text
Memory architecture
Collaborator runtime
Workflow architecture
Provider registry
Plugin system
final runtime topology
```

That conclusion is strongly aligned with the frozen Toolkit boundary: GAIA has already explicitly decided that the demonstrated common denominator is **observation → evidence → requirement analysis → recommendation**, not an Agent runtime.

**Engineering recommendation: REFOCUS / HYBRID.**

No implementation, dependency installation, architecture adoption, repository change, commit or push is warranted by this review.

[1]: https://github.com/pydantic/pydantic-ai/?utm_source=chatgpt.com "GitHub - pydantic/pydantic-ai: How Python does AI: agents, realtime voice, image generation, embeddings. Every model, every interface, typed end to end. · GitHub"
[2]: https://github.com/pydantic/pydantic-ai/blob/main/LICENSE?utm_source=chatgpt.com "pydantic-ai/LICENSE at main · pydantic/pydantic-ai · GitHub"
[3]: https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/persistence.mdx?utm_source=chatgpt.com "docs/src/oss/langgraph/persistence.mdx at main · langchain-ai/docs · GitHub"
[4]: https://github.com/langchain-ai/langgraph/blob/main/LICENSE?utm_source=chatgpt.com "langgraph/LICENSE at main · langchain-ai/langgraph · GitHub"
[5]: https://github.com/langchain-ai/langgraph?utm_source=chatgpt.com "GitHub - langchain-ai/langgraph: Build resilient agents. · GitHub"
[6]: https://github.com/OpenHands/docs/blob/main/openhands/usage/run-openhands/local-setup.mdx?utm_source=chatgpt.com "docs/openhands/usage/run-openhands/local-setup.mdx at main · OpenHands/docs · GitHub"
[7]: https://github.com/OpenHands/OpenHands/blob/main/LICENSE?utm_source=chatgpt.com "OpenHands/LICENSE at main · OpenHands/OpenHands · GitHub"
[8]: https://github.com/open-webui/open-webui?utm_source=chatgpt.com "GitHub - open-webui/open-webui: User-friendly AI Interface (Supports Ollama, OpenAI API, ...) · GitHub"
[9]: https://github.com/open-webui/open-webui/blob/main/LICENSE?utm_source=chatgpt.com "open-webui/LICENSE at main · open-webui/open-webui · GitHub"
[10]: https://github.com/OpenHands/OpenHands-CLI?utm_source=chatgpt.com "GitHub - OpenHands/OpenHands-CLI: Lightweight OpenHands CLI in a binary executable · GitHub"

