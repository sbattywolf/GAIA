# GAIA — PROJECT KNOWLEDGE / OPEN-SOURCE LANDSCAPE REVIEW

## A. WHAT GAIA IS ACTUALLY TRYING TO SOLVE

Dalla traiettoria documentale condivisa, GAIA non sembra principalmente un tentativo di costruire “un altro agent framework”.

Il problema più durevole è piuttosto:

> **come mantenere un sistema di agenti locali, governati e verificabili, con identità/ruoli/autorità stabili, separazione fra modello–runtime–hardware–dominio, evidenza verificabile e controllo umano, pur permettendo di cambiare modelli, macchine, strumenti e componenti software senza perdere coerenza.**

Questo produce almeno cinque esigenze ricorrenti:

1. **Identity & governance**

   * chi è un agent;
   * quale ruolo svolge;
   * cosa può/non può fare;
   * quando deve fermarsi;
   * cosa richiede Human Owner approval.

2. **Evidence-driven engineering**

   * guard → test → validation → evidence → status;
   * distinzione fra observed/current/historical;
   * provenance e riproducibilità.

3. **Local/private operation**

   * 3090/1070 e futuri target;
   * Ollama/local models;
   * rete domestica;
   * futura integrazione QNAP/Raspberry Pi/Home Assistant.

4. **Separation of concerns**

   * Agent;
   * Model;
   * Runtime;
   * Hardware;
   * Target;
   * Domain;
   * Skill/Capability;
   * Mission.

5. **Controlled human authority**

   * l'agent può proporre;
   * può eseguire operazioni bounded;
   * alcune operazioni richiedono approval;
   * Git rimane delivery/versioning authority, non necessariamente runtime communication bus.

Questa è la parte che appare realmente GAIA-specifica.

---

# B. DURABLE REQUIREMENTS

| Requirement                      | Stato                       |          GAIA-specifico? | OSS già utile? |
| -------------------------------- | --------------------------- | -----------------------: | -------------- |
| Agent identity / role separation | DURABLE                     |         **Sì, in parte** | Parzialmente   |
| Authority / approval boundaries  | DURABLE                     |                   **Sì** | Parzialmente   |
| Evidence/provenance discipline   | DURABLE                     |                   **Sì** | Parzialmente   |
| Human Owner as authority         | DURABLE                     |                   **Sì** | Parzialmente   |
| Model neutrality                 | DURABLE                     |        No, ma importante | Sì             |
| Hardware/runtime neutrality      | DURABLE                     |        No, ma importante | Sì             |
| Local-first/private operation    | DURABLE                     |      **GAIA constraint** | Sì             |
| Target/domain separation         | DURABLE                     | **Sì come modello GAIA** | Parzialmente   |
| Progressive engineering loop     | DURABLE engineering pattern | **Sì nel contesto GAIA** | Parzialmente   |
| Network capability               | FUTURE/DURABLE candidate    |                       No | Sì             |
| Agent↔agent communication        | FUTURE                      |                       No | Sì             |
| Memory system                    | NOT YET PROVEN              |                       No | Moltissimo     |
| Agent orchestration framework    | NOT PROVEN                  |                       No | Moltissimo     |
| Agent registry                   | NOT PROVEN                  |                       No | Moltissimo     |
| Provider abstraction             | NOT GAIA-specific           |                       No | Sì             |

### Osservazione importante

La storia E2/3090/1070 dimostra soprattutto che GAIA ha bisogno di **guardrails e validation**, non necessariamente che debba possedere un runtime agentico proprietario.

Questa distinzione è fondamentale:

> **GAIA needs the behavior ≠ GAIA needs to implement the infrastructure.**

---

# C. ACCIDENTAL / CONTEXTUAL REQUIREMENTS

Alcune cose sono fortemente legate all'evoluzione concreta del progetto e non dovrebbero essere elevate automaticamente ad architettura.

### 3090

* Qwen3-Coder 30B
* Ollama
* Docker vs native Ollama
* specific GPU/VRAM handling
* local Engineer implementation details.

### 1070

* qwen2.5-coder:7b
* GTX 1070 constraints
* physical VRAM/RAM behavior
* target-host preflight
* specific Ollama port/runtime configuration.

### E2

* VS Code/GitHub agent mechanism;
* `.agent.md`;
* bounded workspace tooling;
* shell restrictions;
* specific protected-path implementation.

Questi sono **evidence-rich implementation lessons**, ma non dimostrano da soli che GAIA debba creare un framework proprietario corrispondente.

---

# D. OPEN-SOURCE LANDSCAPE

La ricerca aggiornata conferma che il panorama OSS copre già una parte molto ampia dell'infrastruttura che GAIA rischierebbe di reinventare.

### OpenHands

È particolarmente interessante per la parte **engineering agent + sandbox + execution + model agnosticism + self-hosting**. OpenHands dichiara esplicitamente di essere open-source, model-agnostic e deployable nell'ambiente dell'utente, con sandbox runtime e SDK per agent specializzati. ([OpenHands][1])

**Possibile riuso GAIA:** engineering execution substrate.

**Non sostituisce:** GAIA governance/authority/evidence philosophy.

### LangGraph

È molto forte sul lato **stateful agent runtime, durable execution, persistence, human-in-the-loop e workflow orchestration**. ([LangChain][2])

**Possibile riuso:** se GAIA avrà davvero bisogno di workflow agentici persistenti.

**Rischio:** adottarlo troppo presto significherebbe introdurre proprio l'orchestration framework che GAIA sta cercando di evitare finché non emerge una necessità reale.

### PydanticAI

È probabilmente uno dei candidati più interessanti come **minimal agent substrate**: model/provider agnostic, type-safe, composable capabilities e integrazione con tool/MCP/capabilities. ([GitHub][3])

Inoltre supporta Ollama e numerosi provider. ([Pydantic][4])

**Possibile riuso:** molto alto, se GAIA arriverà a implementare un runtime agentico Python.

### CrewAI

È orientato a multi-agent systems, task assignment e workflows. ([Wikipedia][5])

**Possibile riuso:** coordinamento multi-agent.

**Priorità GAIA:** bassa per ora, perché il requisito multi-agent runtime non è ancora dimostrato.

### Google ADK

È un altro framework open-source orientato allo sviluppo di agenti, con agent types, Runner, servizi, loop e tooling locale. ([YouTube][6])

**Possibile riuso:** future experimentation.

**Non c'è ancora evidenza GAIA debba adottarlo.**

### MCP

È particolarmente interessante come **capability/tool boundary**, non come GAIA architecture.

Questo è coerente con la direzione già emersa:

```text
GAIA Agent
    │
    ├── identity / governance
    │
    └── capabilities
            │
            └── external tools / services
```

GAIA dovrebbe preferire standard/tool boundaries esistenti prima di costruire propri protocolli.

---

# E. BUILD vs ADOPT

| GAIA Requirement              | Existing OSS                 | Evidence                          |         Adopt |     Adapt |                   Build | Confidence |
| ----------------------------- | ---------------------------- | --------------------------------- | ------------: | --------: | ----------------------: | ---------: |
| Agent runtime                 | PydanticAI / ADK / LangGraph | forte                             |         **✓** | possibile |                      no |       HIGH |
| Coding-agent execution        | OpenHands                    | forte                             |         **✓** | possibile |                      no |       HIGH |
| Stateful workflows            | LangGraph                    | forte                             | **eventuale** | possibile |                      no |       HIGH |
| Multi-agent orchestration     | CrewAI/LangGraph/ADK         | disponibile                       |     eventuale | eventuale |                      no |     MEDIUM |
| Tool integration              | MCP ecosystem                | disponibile                       |         **✓** | eventuale |                      no |       HIGH |
| Model abstraction             | PydanticAI / existing SDKs   | disponibile                       |         **✓** |        no |                      no |       HIGH |
| Local model runtime           | Ollama                       | già usato                         |         **✓** |        no |                      no |       HIGH |
| Agent identity                | OSS partially                | non equivalente a GAIA            |             — |         — |          **GAIA-owned** |       HIGH |
| GAIA authority model          | OSS partial                  | nessun match completo             |             — |         — |          **GAIA-owned** |       HIGH |
| Human Owner authority         | frameworks partial           | nessun equivalente GAIA-specifico |             — |         — |          **GAIA-owned** |       HIGH |
| Evidence semantics            | tools/frameworks partial     | GAIA experience                   |             — |         — |          **GAIA-owned** |       HIGH |
| P1→P10 engineering governance | nessun match diretto         | GAIA-specific evolution           |             — |         — |          **GAIA-owned** |       HIGH |
| Target/Domain separation      | partial                      | GAIA model emerging               |             — |         — | **GAIA semantic layer** |     MEDIUM |
| Network capability            | standard tools/frameworks    | future GAIA need                  |             ✓ |  possible |                      no |     MEDIUM |
| Agent↔agent transport         | HTTP/SSH/MCP/RPC             | standard technologies             |             ✓ |         — |                      no |       HIGH |
| Persistent substrate          | Git/QNAP/etc.                | infrastructure concern            |             ✓ |         — |                      no |       HIGH |

### Sintesi

La colonna **Build** dovrebbe essere molto più piccola di quanto sarebbe stata qualche sprint fa.

GAIA dovrebbe costruire soprattutto **semantics + governance + evidence contracts**.

Dovrebbe adottare infrastructure/runtime/tooling quando già mature.

---

# F. GAIA DIFFERENTIATION

Dopo aver rimosso ciò che l'ecosistema OSS può ragionevolmente fornire, rimane una parte interessante.

### GAIA potrebbe essere soprattutto:

```text
                 GAIA
        SEMANTIC / GOVERNANCE LAYER
                  │
      ┌───────────┼───────────┐
      │           │           │
   Identity    Authority    Evidence
      │           │           │
      └───────────┼───────────┘
                  │
        Agent / Target / Domain
             semantics
                  │
        ┌─────────┴─────────┐
        │                   │
   External runtime    External tools
   PydanticAI/etc.      MCP/SSH/HTTP
        │                   │
      Ollama              HA/QNAP
        │
   1070 / 3090
```

Questa è una posizione architetturalmente molto più interessante di:

> “GAIA deve costruire un nuovo agent framework.”

---

# G. KNOWLEDGE GAPS

Ci sono ancora domande che non sono state dimostrate.

### 1. Serve davvero un GAIA runtime?

Non ancora dimostrato.

Abbiamo dimostrato che GAIA necessita di agent behavior e governance, non che necessiti di un runtime proprietario.

### 2. Serve davvero multi-agent orchestration?

Non ancora.

L'idea:

```text
Architect ↔ 3090 ↔ 1070
```

è interessante, ma non costituisce ancora un requisito operativo.

### 3. Quanto della governance deve essere software-enforced?

E2 dimostra che alcune boundary devono essere tecnicamente enforceable.

Ma non abbiamo ancora dimostrato che l'intero GAIA governance model debba diventare codice.

### 4. Quale runtime OSS sarebbe migliore?

Non è ancora il momento di scegliere.

PydanticAI, OpenHands, LangGraph e ADK risolvono problemi differenti.

### 5. Network Skill

La necessità appare concreta, ma il **minimal scope** deve essere definito prima di scegliere tecnologia.

---

# H. CONTRADICTIONS

Non vedo, sulla base del materiale disponibile, una contraddizione architetturale fondamentale.

Vedo invece una tensione ricorrente:

```text
GAIA vuole evitare framework prematuri
             ↕
GAIA continua a incontrare pattern
             ↕
nasce la tentazione di astrarli
```

La risposta più coerente con l'evoluzione osservata è:

> **non astrarre il pattern finché non è stato dimostrato almeno da più casi reali.**

Questo vale soprattutto per:

* Agent framework;
* Agent registry;
* Agent-to-agent protocol;
* Network abstraction;
* Model registry;
* orchestration;
* memory.

---

# I. RACCOMANDAZIONE TO TRIANGULATION

Architect + Senior Engineer dovrebbero rispondere soprattutto a queste domande:

### Q1 — Qual è il minimo GAIA-owned layer?

Probabilmente:

```text
Identity
Authority
Governance
Evidence
Human ownership
```

ma va confermato.

### Q2 — Quali capability devono essere genericamente portabili?

Esempi:

```text
Network
Filesystem
Git
Docker
Ollama
MCP
Home Assistant
```

Qui il modello **Skill/Capability** sembra più promettente del modello “nuovo framework”.

### Q3 — Quale runtime OSS può essere lasciato sotto GAIA?

Da valutare solo quando GAIA avrà un requisito runtime concreto.

### Q4 — Quale parte di E2 è vera architettura e quale è engineering implementation?

Questa è una distinzione importante prima di trasformare l'esperienza E2 in framework.

### Q5 — Quando scatta il trigger per adottare un runtime OSS?

Un buon trigger sarebbe:

> almeno due agenti GAIA reali richiedono lo stesso runtime capability e la duplicazione diventa concreta.

---

# CONCLUSIONE ARCHITECT

Il risultato della review **non suggerisce di fermare GAIA**, ma cambia significativamente il rapporto fra “costruire” e “adottare”.

### La direzione che emerge è:

```text
          GAIA SEMANTICS
      identity / authority
       governance / evidence
                │
                ▼
        MINIMAL CAPABILITIES
       network / git / tools
                │
                ▼
       EXISTING OSS RUNTIME
   ┌────────────┼────────────┐
   │            │            │
OpenHands   PydanticAI   LangGraph/ADK
   │            │            │
   └────────────┼────────────┘
                ▼
       LOCAL RUNTIME LAYER
          Ollama / etc.
                │
       ┌────────┴────────┐
       ▼                 ▼
     3090              1070
   Engineer           Target
       │                 │
       └───────┬─────────┘
               ▼
          Domain Skills
        HA / Docker / ...
```

**La parte più difficilmente sostituibile di GAIA non sembra essere il motore dell'agente. È il modello semantico/governance/evidence che decide come un agente può operare, con quale autorità e come dimostrare ciò che ha fatto.**

Per questo, allo stato attuale, la raccomandazione è:

**CONTINUE BUILDING — BUT ADOPT AGGRESSIVELY WHERE THE REQUIREMENT IS INFRASTRUCTURAL.**

Non vedo evidenza sufficiente per scegliere ora OpenHands, PydanticAI, LangGraph, ADK o CrewAI come runtime GAIA. Quella scelta dovrebbe essere una conseguenza di un requisito operativo reale, non il prossimo sprint architetturale. ([OpenHands][1])

[1]: https://www.openhands.dev/?utm_source=chatgpt.com "OpenHands | The Open Platform for Cloud Coding Agents"
[2]: https://www.langchain.com/langgraph?utm_source=chatgpt.com "LangGraph: Agent Orchestration Framework for Reliable AI Agents"
[3]: https://github.com/pydantic/pydantic-ai/blob/main/README.md?utm_source=chatgpt.com "pydantic-ai/README.md at main · pydantic/pydantic-ai · GitHub"
[4]: https://pydantic.dev/docs/ai/models/overview/?utm_source=chatgpt.com "Model Providers | Pydantic Docs"
[5]: https://en.wikipedia.org/wiki/CrewAI?utm_source=chatgpt.com "CrewAI"
[6]: https://www.youtube.com/watch?v=44C8u0CDtSo&utm_source=chatgpt.com "Getting started with Agent Development Kit - YouTube"

