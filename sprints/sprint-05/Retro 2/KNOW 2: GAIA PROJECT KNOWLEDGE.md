# A. PROJECT KNOWLEDGE DEFINITION

### OBSERVATION

GAIA already has a documented Project Knowledge model. It is not simply “all project files” and not a second architecture authority.

The strongest existing definition is:

> Project Knowledge is **relevant, classified, traceable, authority-aware, status-aware, retrievable project knowledge**. 

The Phase 2 knowledge architecture further separates:

* **Tier 0 — Identity**
* **Tier 1 — Core Knowledge**
* **Tier 2 — Current State**
* **Tier 3 — Domain Knowledge**
* **Tier 4 — Research**
* **Tier 5 — Historical Evidence**
* **Tier 6 — Working Context** 

### EVIDENCE

The existing model explicitly says Tier 2 current state **must not be mixed into Identity**, while Tier 5 historical evidence is loaded for reconstruction/lineage and Tier 6 ephemeral working context must not silently become Project Knowledge. 

The existing mandate also reconstructs the intended workflow as:

```text
SOURCE
  ↓
CLASSIFY / RECONCILE / SYNTHESIZE
  ↓
PROJECT KNOWLEDGE
  ↓
DOWNSTREAM USE
```

and explicitly says the output is not “everything the chats said.” 

### INFERENCE

Project Knowledge is therefore best understood as:

```text
PROJECT KNOWLEDGE
=
curated contextual knowledge
+
reconciliation
+
provenance
+
lifecycle/status
+
authority awareness
```

not:

```text
PROJECT KNOWLEDGE
=
SOURCE OF TRUTH
```

### RECOMMENDATION

Preserve this boundary.

**No new Project Knowledge architecture is proven necessary by this review.**

---

# B. IDENTITY vs PROJECT KNOWLEDGE BOUNDARY

The most useful test is the one requested:

> **Would this remain true if the repository, project, mission, machine, host, runtime or model changed?**

If yes, it is a candidate for durable identity.

If no, it is contextual.

## B.1 Durable identity

`reference/IDENTITY.md` is explicitly the durable identity authority. The existing Wave 2 verification confirms it as **durable/current identity authority**. 

Identity should therefore contain only properties such as:

* what GAIA is;
* what GAIA is not;
* durable human-control principles;
* durable behavioral orientation;
* durable identity constraints.

### Example

```text
GAIA remains human-controlled.
```

This survives a change from:

```text
Qwen → another model
Ollama → another runtime
VS Code → Open WebUI
3090 → another machine
```

Therefore:

**IDENTITY**

---

## B.2 Project state

Examples:

* current repository state;
* current branch;
* current milestone;
* current implementation status;
* current blockers;
* current validation state.

These change as GAIA evolves.

Therefore:

**PROJECT KNOWLEDGE / CURRENT STATE**

The existing Tier 2 model explicitly establishes this separation. 

---

## B.3 Architecture decisions

An accepted ADR is not merely contextual knowledge.

For its specific responsibility it is **architectural authority**.

Therefore:

```text
Accepted ADR
    = source of truth for that architectural decision

Project Knowledge
    = context that helps retrieve/understand it
```

The existing Wave 1 reconciliation explicitly establishes responsibility-specific authority rather than one universal canonical document. 

---

## B.4 Historical material

Historical truth can remain true historically without being current.

Existing knowledge architecture explicitly treats historical documents as evidence about why the current state exists, not as current-state authority. 

Therefore:

```text
historically true
    ≠
currently authoritative
```

**HISTORICAL KNOWLEDGE**

---

## B.5 Mission

Mission is task-specific.

Example:

```text
Implement E2
```

does not belong in durable identity.

It belongs in:

**MISSION / WORKING CONTEXT**

---

# C. AUTHORITY MODEL

The existing evidence supports a **responsibility-specific authority model**, not a single universal source.

## C.1 Current authority

| Information                             | Authority                                             |
| --------------------------------------- | ----------------------------------------------------- |
| GAIA identity                           | `reference/IDENTITY.md`                               |
| Explicit accepted architecture decision | individual accepted ADR                               |
| Current repository implementation       | repository/Git state                                  |
| Current validation                      | corresponding validation/evidence artifact            |
| Current project state                   | current-state evidence / appropriate current artifact |
| Project vocabulary                      | designated vocabulary artifact, subordinate to ADRs   |
| Historical lineage                      | historical artifact itself                            |
| Project Knowledge                       | contextual/reconciliation layer                       |

The documentation authority matrix explicitly defines `CANONICAL` only when an artifact is the primary authoritative source for its responsibility, and `DERIVED`/`HISTORICAL` separately. 

## C.2 Project Knowledge authority

### DECISION SUPPORTED BY EXISTING EVIDENCE

Project Knowledge has:

* **contextual authority as a reconciliation layer**;
* **no independent architectural authority**;
* **no authorization authority**;
* **no ability to override accepted ADRs**;
* **no ability to override current repository evidence**.

This is already strongly established.

The Phase 2 blueprint explicitly states that the knowledge layer must not become a new canonical architecture authority and that individual responsibilities retain their own authority. 

---

# D. LIFECYCLE / TEMPORALITY MODEL

This is critical because GAIA has repeatedly encountered old/current duplication.

The existing lifecycle model already distinguishes:

```text
CURRENT
PROVISIONAL
HISTORICAL
SUPERSEDED
UNKNOWN / UNVERIFIED
DERIVED / SECONDARY
```

The authority matrix explicitly recommends:

```text
CANONICAL
CURRENT WORKING BASELINE
DERIVED
HISTORICAL
```

as distinct classifications. 

## D.1 Historical correctness

A historical document can be factually correct and still be wrong for current context.

Example:

```text
old GAIA_MODEL.md
```

may accurately describe what GAIA once meant.

That does not make it current architecture.

The existing Wave 2 rule is:

```text
current working version
    → load

older predecessor
    → lineage/reconciliation only
```



## D.2 Required conceptual metadata

The existing model says a knowledge artifact should conceptually answer:

```text
What is it?
Who owns it?
What status does it have?
What is its authority?
When was it last validated?
What supersedes it?
What does it depend on?
```



This is sufficient conceptually to prevent most historical/current confusion.

### INFERENCE

The metadata is more important than the exact storage format.

**NOT PROVEN:** that GAIA needs a dedicated database/service to maintain this metadata.

---

# E. CURRENT vs HISTORICAL DISTINCTION

This boundary is already unusually well established because of the migration work.

## Current

Current evidence should be preferred for:

* repository state;
* runtime observations;
* implementation;
* validation;
* active project status.

## Historical

Historical evidence should answer:

> Why did GAIA get here?

rather than:

> What is GAIA now?

The existing repository rules explicitly prevent old `oldRepoReferences` and historical documents from being treated as normal current development material. 

## Superseded

A document should not become superseded merely because it is old.

The authority matrix's distinction is important:

```text
older
≠
superseded
```

A true supersession requires a later authority for the same responsibility.

### STATUS

**ALREADY EXPLICIT / STRONG**

---

# F. SOURCE OF TRUTH vs CONTEXTUAL KNOWLEDGE

This is perhaps the most important boundary.

## SOURCE OF TRUTH

Means:

> This artifact has authority for this specific responsibility.

Examples:

```text
IDENTITY.md
    → identity

Accepted ADR
    → architectural decision

Repository/Git
    → committed implementation state

Validation artifact
    → validation evidence
```

## CONTEXTUAL RETRIEVAL LAYER

Means:

> This material helps the Agent understand, locate, compare or interpret authoritative information.

Examples:

```text
Project Knowledge
Wave reconciliation
historical reconstruction
indexes
derived summaries
chat context
```

The existing authority model explicitly says:

```text
importance for context
    ≠
architectural authority
```



Therefore a document being present in Project Knowledge **must never be interpreted as automatically authoritative**.

---

# G. ENGINEER-SPECIFIC PROJECT CONTEXT

The Engineer should obtain from Project Knowledge what changes with the project.

## G.1 Current repository authority

**PROJECT KNOWLEDGE**

The Engineer needs to know:

* which repository is in scope;
* current baseline;
* protected areas;
* current relevant ADRs;
* current lifecycle state.

It should not hard-code these into durable Agent identity.

---

## G.2 Current milestone

**PROJECT KNOWLEDGE / MISSION CONTEXT**

Example:

```text
E2
PM-002
Toolkit V0.1
Local Engineer V0.1.1
```

These are project lifecycle facts, not identity.

---

## G.3 Protected paths

**PROJECT / GOVERNANCE CONTEXT**

Protected paths can change.

They therefore do not belong in durable identity.

---

## G.4 Implementation authority

The Engineer needs to know:

```text
who authorized implementation
what scope was authorized
what remains outside scope
```

This is **current governance/task context**.

The Engineer should not infer it from a commit or from Project Knowledge alone.

---

## G.5 Test authority

The Engineer needs to know:

* which tests are authoritative;
* which tests are historical;
* what a test actually proves.

The ING_3090 review specifically identified test-lineage confusion as a recurring failure mode. 

Therefore this is highly relevant Project Knowledge, but not identity.

---

## G.6 Current blockers

**CURRENT STATE**

For example:

```text
PM-002 = BLOCKED
E2 governance gates = OPEN
```

These must be retrieved as current context.

---

## G.7 Historical context

Useful when needed:

```text
Why is PM-002 protected?
Why does an ADR exist?
Why is a legacy path preserved?
```

But it should be loaded when relevant, not permanently encoded into Agent identity.

---

## G.8 Current execution environment

The Engineer needs:

* host;
* machine;
* runtime;
* model;
* available tools;
* relevant credentials/capabilities.

But these are **environmental facts**.

They should not become durable identity.

---

# H. HOST / MACHINE / RUNTIME / MODEL CONTEXT

The identity test produces a clean classification.

| Example                              | Classification                       | Reason                                 |
| ------------------------------------ | ------------------------------------ | -------------------------------------- |
| VS Code                              | **HOST CONTEXT**                     | interface through which Agent operates |
| Open WebUI                           | **HOST CONTEXT**                     | interface/integration layer            |
| Telegram                             | **HOST CONTEXT**                     | external interaction channel           |
| GitHub                               | **HOST / EXTERNAL SERVICE CONTEXT**  | external repository/service boundary   |
| RTX 3090                             | **MACHINE CONTEXT**                  | physical compute environment           |
| target machine                       | **MACHINE CONTEXT**                  | execution target                       |
| Docker                               | **RUNTIME CONTEXT**                  | execution mechanism                    |
| Python environment                   | **RUNTIME CONTEXT**                  | implementation environment             |
| Qwen model                           | **MODEL CONTEXT**                    | model selection                        |
| Ollama/container runtime             | **RUNTIME CONTEXT**                  | model/runtime infrastructure           |
| current Home Assistant instance      | **DOMAIN / EXTERNAL SYSTEM CONTEXT** | external authoritative system          |
| current E2 mission                   | **MISSION CONTEXT**                  | task-specific                          |
| GAIA Human Owner authority principle | **IDENTITY / GOVERNANCE**            | durable behavioral constraint          |

### Identity test

If we replace:

```text
3090 → 1070
Qwen → another model
VS Code → Telegram
Ollama → another runtime
```

GAIA does not cease to be GAIA.

Therefore those properties are **not durable Agent identity**.

This is also consistent with the identity principle that technology and framework should not define GAIA. 

---

# I. INFORMATION THAT SHOULD NOT BE DUPLICATED IN AGENT FILES

The current Agent proposal correctly identifies the problem: the current E2 Engineer file mixes durable behavior, role, mission, current state, machine/model assumptions and governance. However, that document remains explicitly **PROPOSAL / NOT YET AUTHORITATIVE**. 

The independent Project Knowledge evidence supports avoiding duplication of:

## 1. Current project state

Do not permanently embed:

```text
current branch
current milestone
current blockers
current completion
current implementation state
```

These change.

## 2. Current architecture status

Do not duplicate:

```text
which ADR is currently accepted
which proposal is pending
which semantic model is current
```

except perhaps as bounded contextual references.

The source authority remains the ADR/document itself.

## 3. Machine/model state

Do not make:

```text
RTX 3090
Qwen3-Coder 30B
Ollama
Docker
```

durable identity.

## 4. Mission

Do not make:

```text
E2
PM-002
HC-001
```

part of general Agent identity.

## 5. Historical lessons

Do not permanently embed every ING_3090 lesson into identity.

Only the **general invariant** may become durable.

For example:

```text
Do not infer authority from filenames.
```

can be a reusable behavioral rule.

But:

```text
This particular file was once mistaken for X during ING_3090.
```

is historical context.

## 6. Test counts / validation state

Do not embed:

```text
37/37
19/19
PASS
```

as identity.

These are current evidence.

---

# J. CURRENT GAIA MATERIAL CLASSIFICATION

| Material                      | Classification                                                   | Evidence / reasoning                                      |
| ----------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------- |
| `reference/IDENTITY.md`       | **DURABLE IDENTITY / CANONICAL**                                 | explicit identity authority                               |
| `GAIA_MODEL_v0.2.md`          | **CURRENT WORKING / PROPOSED**                                   | current conceptual baseline, explicitly Proposed          |
| ADR-0001                      | **ACCEPTED ARCHITECTURE**                                        | accepted ADR                                              |
| ADR-0003 accepted copy        | **ACCEPTED ARCHITECTURE**                                        | accepted ADR                                              |
| Proposed ADR-0003 predecessor | **PROPOSED / HISTORICAL LINEAGE**                                | accepted copy supersedes it for decision authority        |
| Context Model v0.2            | **PROPOSED SEMANTIC KNOWLEDGE**                                  | explicitly Proposed                                       |
| World Model v0.2              | **PROPOSED SEMANTIC KNOWLEDGE**                                  | explicitly Proposed                                       |
| Glossary v0.2                 | **PROPOSED SUPPORTING KNOWLEDGE**                                | vocabulary, subordinate to ADRs                           |
| Architecture Convergence v0.2 | **PROPOSED GOVERNANCE / COORDINATION**                           | does not override ADRs                                    |
| NEXT_STEPS v0.2               | **PROJECT / ROADMAP CONTEXT**                                    | mutable planning information                              |
| `AGENTS.md`                   | **ENGINEERING STEERING**                                         | operational, not architecture authority                   |
| `.agent.md`                   | **ROLE / STEERING CONTEXT**                                      | agent-specific operational instructions                   |
| W3 artifacts                  | **IMPLEMENTATION / VALIDATION EVIDENCE**                         | bounded evidence, not general architecture                |
| E2 state                      | **CURRENT PROJECT / LIFECYCLE CONTEXT**                          | implementation/validation/governance must remain separate |
| Toolkit V0.1                  | **ACCEPTED / FROZEN ARCHITECTURAL+IMPLEMENTATION BASELINE**      | current established state                                 |
| Local Engineer V0.1.1         | **CURRENT CAPABILITY / LIFECYCLE EVIDENCE**                      | lifecycle must remain explicitly classified               |
| PM-002                        | **CURRENT BLOCKED PROJECT STATE**                                | not identity                                              |
| 1070                          | **MACHINE / HISTORICAL + CURRENT EVIDENCE CONTEXT**              | target environment evidence                               |
| 3090                          | **MACHINE / ENGINEERING CONTEXT**                                | engineering environment                                   |
| Qwen3-Coder 30B               | **MODEL CONTEXT**                                                | provisional execution context                             |
| Ollama                        | **RUNTIME CONTEXT**                                              | technology                                                |
| Home Assistant inventory      | **EXTERNAL DOMAIN EVIDENCE**                                     | external authority for current HA state                   |
| Sprint 4/5 material           | **HISTORICAL** unless current evidence explicitly revalidates it | existing reconciliation rule                              |
| Project Knowledge             | **RECONCILIATION / CONTEXT**                                     | not independent authority                                 |

---

# K. OPEN QUESTIONS

These are questions, not decisions.

## K1 — Exact canonical identity boundary

**Status: PARTIALLY RESOLVED**

`IDENTITY.md` already establishes durable identity.

What remains open is the exact boundary between:

```text
GAIA Identity
```

and:

```text
GAIA Agent behavioral policy
```

The existing Engineer proposal suggests separating them, but that proposal is not authoritative. 

**AUTHORITY:** Architect + Human Owner if a formal architectural change is contemplated.

---

## K2 — Should current-state retrieval be explicit Agent behavior?

**Status: OPEN / NOT PROVEN**

The existing knowledge model strongly implies it.

But this review does not establish an accepted requirement that every Agent dynamically retrieve Tier 2 state.

That would be an implementation decision.

---

## K3 — Exact Project Knowledge authority metadata

The conceptual model already requires authority/status/provenance information.

**OPEN:** whether that requires a formal schema or can remain document-level metadata.

No evidence justifies creating a new state system.

---

## K4 — Project Knowledge synchronization

The existing reconciliation identifies Git ↔ Project Knowledge divergence as a real process gap. 

**Status: OPEN**

But:

```text
gap
≠
need for a database/service
```

The implementation mechanism is not proven.

---

## K5 — Agent snapshot freshness

The current `.agent.md` model can contain current-state snapshots.

The recent governance review identified the principle:

```text
VERSIONED ≠ AUTHORITATIVE
STEERING ≠ ARCHITECTURE AUTHORITY
SNAPSHOT ≠ CURRENT TRUTH
EVIDENCE > EMBEDDED ASSUMPTION
```

The broader authority model supports these distinctions, but the exact agent-snapshot rule is not yet fully explicit in the canonical material.

**Status: DOCUMENTATION GAP / NOT ARCHITECTURAL GAP**

---

## K6 — Seven first-class concepts

The v0.2 model explicitly identifies seven concepts, but remains **Proposed**. 

Therefore:

**AUTHORITY:** current working conceptual baseline, not formally Accepted architecture.

This distinction must remain visible.

---

## K7 — Context / World Model acceptance

Both remain Proposed in the evidence available.

**NOT PROVEN:** that they should now become Accepted.

---

# L. PROJECT KNOWLEDGE RECOMMENDATION

## Recommendation

**Preserve the existing conceptual Project Knowledge architecture. Do not replace it with a new architecture.**

The strongest evidence supports:

```text
                 GAIA
                  │
       ┌──────────┼───────────┐
       │          │           │
    IDENTITY   AUTHORITY   PROJECT KNOWLEDGE
       │          │           │
       │      Accepted ADRs   ├── Current State
       │      Governance      ├── Domain Context
       │                      ├── Research
       │                      ├── Historical Evidence
       │                      └── Derived Context
       │
       └── durable principles
```

with:

```text
SOURCE OF TRUTH
    ≠
PROJECT KNOWLEDGE
```

and:

```text
PROJECT KNOWLEDGE
    ≠
AGENT IDENTITY
```

and:

```text
HISTORICAL KNOWLEDGE
    ≠
CURRENT STATE
```

and:

```text
CURRENT STATE
    ≠
MISSION
```

and:

```text
MACHINE / MODEL / RUNTIME
    ≠
IDENTITY
```

---

## The key conclusion

### OBSERVATION

GAIA has **already independently established** a strong separation between Identity and mutable project knowledge.

### EVIDENCE

The Tier model explicitly separates Identity from Current State, Domain, Research, Historical Evidence and Working Context. 

The Project Knowledge mandate explicitly defines the layer as classified, traceable, authority-aware and status-aware rather than as a transcript of project conversations. 

The authority matrix distinguishes canonical, working, derived and historical artifacts. 

### INFERENCE

The current GAIA model does **not** need a fundamental redesign to achieve the requested Identity/Project Knowledge separation.

The main remaining issue is **precision**, especially around how embedded current-state snapshots inside durable Agent steering are interpreted.

### RECOMMENDATION

If anything is eventually changed, the first-order improvement should be a **small documentation/governance clarification**, not:

* a state database;
* Agent Registry;
* Memory framework;
* synchronization service;
* new Project Knowledge runtime;
* new Agent architecture.

### DECISION

**NOT MADE BY THIS REVIEW.**

This review does not authorize adoption of any proposed Agent layer model.

---

# FINAL INDEPENDENT ASSESSMENT

| Area                                                    | Result                       |
| ------------------------------------------------------- | ---------------------------- |
| Durable GAIA Identity                                   | **ESTABLISHED**              |
| Project Knowledge as contextual layer                   | **ESTABLISHED**              |
| Project Knowledge as independent architecture authority | **NOT SUPPORTED**            |
| Current vs historical distinction                       | **ESTABLISHED**              |
| Authority/lifecycle distinction                         | **ESTABLISHED**              |
| Current-state separation from Identity                  | **ESTABLISHED**              |
| Mission separation                                      | **ESTABLISHED CONCEPTUALLY** |
| Host/machine/model separation                           | **SUPPORTED**                |
| Agent snapshot ≠ current truth                          | **PARTIALLY EXPLICIT**       |
| Need for new knowledge framework                        | **NOT PROVEN**               |
| Need for new Agent architecture                         | **NOT PROVEN**               |
| Need for Project Knowledge database/service             | **NOT PROVEN**               |
| Need for documentation clarification                    | **SUPPORTED**                |

**Final status:** **INDEPENDENT PROJECT KNOWLEDGE REVIEW COMPLETE.**

No Architect or Senior Engineer response was used to reconcile this result; the analysis above is grounded in the Project Knowledge artifacts and evidence retrieved for this review.

