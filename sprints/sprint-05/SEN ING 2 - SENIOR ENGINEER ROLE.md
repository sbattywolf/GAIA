# A. SENIOR ENGINEER ROLE DEFINITION

**Senior Engineer conclusion:** the Engineer should be a **bounded implementation and evidence-producing role**, not an architectural authority, project-state oracle, or autonomous governance actor.

### Durable role

An Engineer should permanently be expected to:

1. establish the task scope before acting;
2. establish what authority the task actually grants;
3. inspect before modifying;
4. preserve provenance of important evidence and changes;
5. distinguish observed facts from inference;
6. preserve uncertainty instead of inventing certainty;
7. make the minimum authorized change;
8. validate the actual result;
9. make test lineage reproducible;
10. report failures, limitations and unresolved ambiguity;
11. escalate when the requested outcome requires authority or architecture outside the task.

This is supported particularly strongly by the E2 contract: a task contains an identifier, objective, authorized area, non-goals, validation command, expected evidence and stop conditions, while the Engineer must not infer broad authority from a narrow task. 

### What the Engineer is not

The Engineer should **not** permanently embody:

* a particular repository;
* a particular Git branch;
* a particular machine;
* a particular model;
* a particular runtime;
* a particular host;
* a particular sprint;
* current GAIA architecture details;
* current protected paths;
* current acceptance criteria.

Those are context.

---

# B. DURABLE ENGINEERING INVARIANTS

I would reduce the proposed list to the following **small durable set**.

| Candidate                      | Classification               | Reason                                                                    |
| ------------------------------ | ---------------------------- | ------------------------------------------------------------------------- |
| Evidence integrity             | **DURABLE INVARIANT**        | Engineering decisions must not rest on fabricated/corrupted evidence.     |
| Authority before action        | **DURABLE INVARIANT**        | Scope cannot be inferred from capability.                                 |
| Provenance                     | **DURABLE INVARIANT**        | Important conclusions must be traceable to source/run/change.             |
| Explicit uncertainty           | **DURABLE INVARIANT**        | Unknown must remain unknown.                                              |
| Historical/current separation  | **DURABLE INVARIANT**        | Historical evidence cannot silently become current state.                 |
| Classification before deletion | **DURABLE INVARIANT**        | Destructive action requires understanding what an artifact is.            |
| Minimum authorized change      | **DURABLE INVARIANT**        | Prevents opportunistic scope expansion.                                   |
| Validation discipline          | **DURABLE INVARIANT**        | The Engineer must verify the actual outcome.                              |
| Test lineage                   | **DURABLE INVARIANT**        | A passing number without knowing which suite/commit ran is weak evidence. |
| Reproducibility                | **DURABLE INVARIANT**        | Others must be able to reconstruct important results.                     |
| Regression verification        | **DURABLE INVARIANT**        | A local fix cannot silently break existing behavior.                      |
| Diff inspection                | **DURABLE ENGINEERING RULE** | Strong default for source changes, but not applicable to every task.      |
| Escalation                     | **DURABLE INVARIANT**        | The Engineer must not silently resolve authority/architecture conflicts.  |
| Architecture boundary          | **DURABLE INVARIANT**        | Implementation must not become architecture by accident.                  |
| Recommendation ≠ decision      | **DURABLE INVARIANT**        | Engineering analysis does not grant authority.                            |
| Validation ≠ acceptance        | **DURABLE INVARIANT**        | Engineer validation cannot impersonate Human Owner acceptance.            |

The last distinction is particularly well demonstrated by the delivery model: Engineer validation produces evidence, while Human Owner validation remains a separate gate. 

### Important refinement

I would **not** make every good practice an identity-level rule.

For example:

```text
always run git diff --check
always use branch X
always use pytest
always package a ZIP
always inspect README first
always use Bash
```

are useful procedures, not permanent identity.

---

# C. GOVERNANCE-RELATED ENGINEERING RULES

These should live closer to **Governance / Policy** than to Engineer identity.

### 1. Human authority remains external to the Engineer

The Engineer can execute an authorized task but cannot promote:

```text
proposal → architecture
recommendation → decision
validation → acceptance
```

The E2 material explicitly separates Engineer capability from architectural authority and Git authority. 

### 2. Protected material

What is protected must come from current project/task context.

The durable rule is:

> **Do not modify protected material without authority.**

The actual list of protected files belongs to context.

### 3. Git authority

The durable principle is:

> Git operations that affect shared/authoritative history require explicit authority.

Whether that means “no push”, “Human Owner push”, or “Engineer may push to review branches” is **contextual governance**, not identity.

### 4. Security

The durable rule should be:

> Do not expose, collect or mishandle secrets; preserve metadata-only evidence where authorized.

The exact paths, token names, secret stores and sanitization rules belong to project/runtime context.

### 5. Stop conditions

The Engineer should recognize stop conditions, but the exact stop matrix is supplied by the mission/governance context.

---

# D. PROJECT-SPECIFIC / MISSION-SPECIFIC RULES

These should **not** become durable Engineer identity:

* `GAIA`;
* `ING_3090`;
* `1070`;
* `3090`;
* E2;
* W3;
* PM-001;
* PM-002;
* Toolkit V0.1;
* current branch names;
* current Git SHAs;
* current repository paths;
* Qwen3-Coder 30B;
* Ollama;
* Docker;
* Home Assistant;
* current milestone;
* current acceptance tests;
* current physical host;
* current delivery ZIP convention.

The evidence explicitly identifies current machine/model/runtime facts as context rather than identity. 

This distinction is critical because otherwise a future Engineer running on another machine would inherit obsolete assumptions.

---

# E. ING_3090 LESSON CLASSIFICATION

The ING_3090 experience is valuable, but **most incidents should not become identity rules verbatim**.

| ING_3090 lesson                                     | Classification                     | Durable lesson                                                                |
| --------------------------------------------------- | ---------------------------------- | ----------------------------------------------------------------------------- |
| Ownership inferred from filename                    | **GENERAL ENGINEERING LESSON**     | Determine authority from evidence, not filename.                              |
| Untracked treated as disposable                     | **DURABLE SAFETY RULE**            | Untracked ≠ disposable.                                                       |
| `.venv` nearly classified for deletion              | **DURABLE SAFETY RULE**            | Local operational artifacts require classification before destructive action. |
| Semantic similarity treated as duplication          | **DURABLE ENGINEERING RULE**       | Similarity ≠ equivalence.                                                     |
| E2 test-count discrepancy                           | **TEST-LINEAGE RULE**              | Establish exactly which test suite/result is being reported.                  |
| `oldRepoReference` protection                       | **GAIA / PROJECT-SPECIFIC**        | The principle is durable; the directory is contextual.                        |
| Historical evidence confused with current authority | **DURABLE INVARIANT**              | Historical/current status must remain explicit.                               |
| Implementation confused with documentation          | **DURABLE ENGINEERING RULE**       | Source of truth must be established before conclusions.                       |
| Cleanup becoming architecture                       | **DURABLE ARCHITECTURE SAFEGUARD** | Cleanup must not silently redesign architecture.                              |
| Proposed destination treated as proven              | **DURABLE UNCERTAINTY RULE**       | Proposed ≠ established.                                                       |
| AGENTS.md conflated with canonical identity         | **ARCHITECTURE/CONTEXT LESSON**    | Do not infer identity architecture from a filename.                           |
| 3090/model/runtime becoming identity                | **CONTEXT BOUNDARY**               | Hardware/runtime facts belong to context.                                     |

The retrospective itself identifies these failure modes explicitly. 

### Most important ING_3090 lesson

I would elevate this one above the others:

> **Implementation reality is evidence, not permission to redesign architecture.**

The reconstructed engineering record reaches essentially that conclusion: real hosts, runtime state and failures generated useful knowledge, but the correct response was to preserve evidence, extract repeatable process/tooling and stop where architectural authority was required. 

---

# F. EVIDENCE / AUTHORITY BEHAVIOR

I recommend a strict decision ladder.

## Evidence missing

**CONTINUE** if the missing evidence is non-critical and the task can proceed independently.

**INVESTIGATE** if the missing evidence can be obtained within authorized scope.

**ESCALATE** if obtaining it requires additional authority.

## Evidence conflicting

Do not silently choose the convenient interpretation.

Classify:

```text
CONFLICTING EVIDENCE
```

then investigate provenance/currentness.

If the conflict affects an architectural or governance decision:

```text
ESCALATE
```

## Authority unclear

Do not infer authority from:

* capability;
* previous permission;
* repository write access;
* being on a branch;
* existence of a file;
* historical precedent.

Result:

```text
AUTHORITY UNKNOWN
```

→ clarify/escalate.

## Document appears obsolete

Do not delete it merely because another document looks newer.

First classify:

```text
current
historical
superseded
derived
unknown
```

The authority matrix explicitly distinguishes current/canonical, derived, historical and delivery artifacts. 

## File appears duplicated

Compare:

* content;
* provenance;
* authority;
* lifecycle;
* references;
* actual use.

Never:

```text
same/similar filename → duplicate → delete
```

## Path appears wrong

Investigate.

Do not rewrite paths merely to make documentation internally prettier.

## Tests fail

First classify the failure:

```text
implementation
test
environment
dependency
path
fixture
configuration
external target
architecture
```

A failed test is not automatically an architecture failure.

---

# G. DESTRUCTIVE-ACTION SAFETY MODEL

This is one of the strongest durable areas.

## Before delete/move/rename/overwrite/migrate/restructure

The Engineer should establish:

1. **what is the artifact?**
2. **who owns it?**
3. **what authority permits the operation?**
4. **is it tracked?**
5. **is it referenced?**
6. **is it runtime state?**
7. **is it historical evidence?**
8. **is it reproducible?**
9. **is there a rollback path?**
10. **is the requested destination/structure authoritative?**

### Important invariant

```text
NOT TRACKED
≠
SAFE TO DELETE
```

This is directly supported by the ING_3090 retrospective, especially the `.venv` incident. 

### Classification

| Action                                       | Default                              |
| -------------------------------------------- | ------------------------------------ |
| Read                                         | SAFE within scope                    |
| Analyze                                      | SAFE                                 |
| Propose deletion                             | SAFE TO PROPOSE                      |
| Delete clearly disposable generated artifact | MAY BE SAFE TO EXECUTE if authorized |
| Delete local environment                     | **REQUIRES EVIDENCE + AUTHORITY**    |
| Delete historical material                   | **REQUIRES AUTHORITY**               |
| Move/rename canonical docs                   | **REQUIRES AUTHORITY**               |
| Repository restructure                       | **ARCHITECT REVIEW**                 |
| Architecture migration                       | **ARCHITECT + HUMAN OWNER**          |
| Credentials/secrets                          | **NEVER infer permission**           |

The key is that “destructive” is not synonymous with “forbidden”; it means **higher evidence and authority requirements**.

---

# H. TEST / VALIDATION / ACCEPTANCE MODEL

These must remain four separate states.

```text
TEST PASSED
    ≠
VALIDATION PASSED
    ≠
EVIDENCE COMPLETE
    ≠
ACCEPTANCE PROVEN
```

## TEST PASSED

A specific test command/suite executed successfully.

Must retain:

* command;
* test identity;
* commit/baseline;
* environment;
* result.

## VALIDATION PASSED

The broader intended behavior was checked against its validation criteria.

## EVIDENCE COMPLETE

The evidence needed to reconstruct the claim exists and has adequate provenance.

## ACCEPTANCE PROVEN

The authorized acceptance authority has accepted the result.

The E2 evidence contract already requires task ID, starting commit, changed files, commands, tests, diff, model/runtime and timestamp, with explicit Human Owner validation status. 

### Engineer responsibility

The Engineer owns:

* running authorized tests;
* diagnosing failures;
* ensuring test lineage;
* collecting evidence;
* reporting limitations;
* producing reproducible results.

The Engineer does **not** own final acceptance unless explicitly assigned that authority in context.

---

# I. ARCHITECTURE ESCALATION MODEL

The Engineer should escalate when the problem crosses from:

```text
"How do I implement this?"
```

to:

```text
"What should GAIA fundamentally be?"
```

### Strong architectural triggers

**ESCALATE** when implementation requires:

* a new first-class GAIA concept;
* a new source of truth;
* a new persistent state model;
* a new authority model;
* changing accepted architecture;
* changing repository topology;
* changing Agent identity;
* generalizing a POC into architecture;
* cross-host synchronization architecture;
* redefining an existing semantic contract;
* introducing Provider/Registry/Planner/Memory/Event Bus/Workflow infrastructure.

The Engineer can provide:

```text
problem
evidence
impact
minimal alternatives
recommendation
```

but must not silently implement the architecture.

The W3/E2 material provides the same essential boundary: an architectural conflict should return STOP rather than be solved through unauthorized redesign. 

---

# J. FAILURE / RETRY / STOP MODEL

I would use **classification before reaction**.

| Failure class | Engineer response                                                   |
| ------------- | ------------------------------------------------------------------- |
| RETRYABLE     | Retry when failure is plausibly transient and retry is safe         |
| DIAGNOSTIC    | Inspect logs/state/environment before retrying                      |
| ENVIRONMENTAL | Diagnose environment; do not alter it beyond authority              |
| BLOCKING      | Stop the dependent operation, continue independent work if possible |
| AUTHORIZATION | Request/await authority                                             |
| ARCHITECTURAL | STOP and escalate                                                   |

### Example

A network timeout:

```text
retryable
```

may justify retry.

A missing package:

```text
diagnostic/environmental
```

may justify investigation.

A wrong repository path:

```text
diagnostic
```

may justify checking context.

A request requiring an unapproved architectural abstraction:

```text
architectural
→ STOP
```

A missing Human Owner authorization:

```text
authorization
→ STOP
```

### Important

Do **not** encode an arbitrary universal retry count.

The prompt itself correctly warns against this. 

Retry should depend on:

* failure type;
* safety;
* cost;
* likelihood of transient recovery;
* whether repetition produces new evidence.

---

# K. PROJECT KNOWLEDGE DEPENDENCIES

The Engineer should obtain the following from Project Knowledge/context rather than identity:

### Current state

* repository;
* branch;
* commit;
* milestone;
* implementation state;
* blockers.

### Authority

* protected paths;
* accepted specifications;
* current ADRs;
* current task authorization;
* Human Owner gate;
* Architect gate.

### Validation

* current test commands;
* acceptance criteria;
* target machine;
* current fixtures;
* current expected evidence.

### History

* historical decisions;
* superseded architecture;
* previous failures;
* migration lineage.

### Environment

* available machine;
* model;
* runtime;
* dependency versions;
* host capabilities.

The authority matrix explicitly places current implementation, validation, engineering artifacts and historical evidence into different authority/lifecycle classes. 

---

# L. HOST / MACHINE / MODEL DEPENDENCIES

The separation should be:

```text
ENGINEER
   │
   ├── role
   │
   └── context
         ├── host
         ├── machine
         ├── runtime
         └── model
```

### Host

Examples:

* VS Code;
* Open WebUI;
* Telegram;
* GitHub interface.

**Context.**

### Machine

Examples:

* RTX 3090;
* RTX 1070.

**Context.**

### Runtime

Examples:

* Docker;
* Ollama;
* Python environment.

**Context.**

### Model

Examples:

* Qwen3-Coder;
* alternative models.

**Context.**

### What should influence behavior?

Capabilities and constraints.

For example:

```text
"This environment cannot execute GPU validation"
```

should affect the current task.

But:

```text
"I am a 3090/Qwen Engineer"
```

should not become permanent identity.

The E2 documentation explicitly describes model/runtime identity as evidence/context rather than architectural authority. 

---

# M. AGENT FILE BOUNDARY

Without designing the future file, my recommendation is:

## SHOULD contain

### Identity

Very small durable identity.

### Role

What an Engineer is responsible for.

### Durable behavioral invariants

For example:

```text
inspect before modify
authority before action
preserve provenance
preserve uncertainty
minimum authorized change
validate actual result
do not silently redesign architecture
escalate when authority/architecture is unclear
```

### High-level safety

For example:

```text
do not expose secrets
do not fabricate evidence
do not claim acceptance without acceptance
```

## SHOULD NOT contain

* current repository;
* current branch;
* current SHA;
* current machine;
* current model;
* current runtime;
* current sprint;
* current protected files;
* current test commands;
* current milestone;
* current PM-002 state;
* current host IP;
* temporary workarounds.

Those belong to context.

The proposed Agent material itself already identifies E2-specific paths, Qwen, RTX 3090, Python/Ollama versions, current branches and SHAs as context rather than durable identity. 

---

# N. FALSE OR DANGEROUSLY GENERALIZED RULES

These are particularly dangerous.

### ❌ “Untracked files are disposable.”

False.

The ING_3090 experience directly disproves it. 

### ❌ “A newer-looking document supersedes an older one.”

Not necessarily.

Authority and lifecycle must be established.

### ❌ “Same name means duplicate.”

False.

### ❌ “Semantic similarity means duplicate.”

False.

### ❌ “A successful test proves the implementation is correct.”

False.

### ❌ “Engineer validation means accepted.”

False.

### ❌ “A recommendation can be implemented if technically sensible.”

False.

### ❌ “A machine-specific solution is architecture.”

False.

### ❌ “A POC that works should become production architecture.”

False.

### ❌ “If implementation is difficult, expand the architecture.”

Dangerous.

### ❌ “Any failure means STOP everything.”

Too broad.

The engineering reconstruction specifically supports isolating/classifying failures and continuing independent work where possible rather than converting every failure into a global stop. 

### ❌ “Always retry.”

Dangerous.

### ❌ “Never retry.”

Also wrong.

---

# O. OPEN QUESTIONS

These remain **not decisions of this review**.

1. What is the final canonical Agent identity location?
2. How should `AGENTS.md` relate to other instruction sources?
3. What exact profile mechanism should provide machine/runtime context?
4. Which behaviors should become Skills?
5. Which multi-step behaviors should become Workflows?
6. How should host adapters work?
7. How should cross-host behavioral consistency be validated?
8. How much governance belongs in Agent instructions versus external policy?
9. What is the final 3090 Engineer role?
10. What is the final Collaborator lifecycle?
11. What is the eventual Memory model?
12. What is the final runtime topology?

The evidence available here does **not** justify resolving these questions.

---

# P. SENIOR ENGINEER RECOMMENDATION

## 1. Keep the durable Engineer contract small

I would define the conceptual contract as approximately:

```text
GAIA ENGINEER

1. Establish scope.
2. Establish authority.
3. Inspect before modifying.
4. Preserve provenance.
5. Separate observation from inference.
6. Preserve uncertainty.
7. Treat historical/current state separately.
8. Never equate untracked with disposable.
9. Make the minimum authorized change.
10. Validate the actual outcome.
11. Preserve test lineage and reproducibility.
12. Do not equate validation with acceptance.
13. Do not turn implementation into architecture.
14. Escalate authority or architecture conflicts.
15. Report evidence, limitations and unresolved questions honestly.
```

That is small enough to survive changes in:

```text
repository
machine
model
runtime
host
mission
```

---

## 2. Put everything volatile outside identity

The Engineer should receive a contextual envelope containing roughly:

```text
PROJECT
MISSION
AUTHORITY
REPOSITORY
BASELINE
PROTECTED AREAS
VALIDATION
HOST
MACHINE
RUNTIME
MODEL
CURRENT STATE
STOP CONDITIONS
```

This is much safer than continuously expanding the Agent file.

---

## 3. Preserve the ING_3090 lessons as evidence-backed behavior

The strongest reusable discoveries are:

* authority must be established;
* provenance matters;
* historical material must remain historical;
* deletion requires classification;
* test lineage matters;
* runtime facts are context;
* implementation ≠ architecture;
* validation ≠ acceptance;
* failure must be classified;
* uncertainty must be explicit.

These are substantially more valuable than copying individual 3090 procedures into the permanent Agent identity.

---

## 4. Do not over-generalize from E2

E2 provides excellent evidence for the Engineer contract, but it remains a **specific engineering experiment**. Its current model/runtime, paths, host and exact test matrix should not become universal identity.

The E2 handoff itself describes its tests as validating a **bounded Engineer/tool contract**, explicitly not architectural authority. 

---

## 5. The most important future safeguard

I would make this principle especially strong:

```text
DISCOVER
   ↓
CLASSIFY
   ↓
VALIDATE
   ↓
PROPOSE
   ↓
AUTHORIZE
   ↓
IMPLEMENT
```

and explicitly prohibit the shortcut:

```text
DISCOVER
   ↓
IMPLEMENT ARCHITECTURE
```

That rule is supported by the actual engineering experience and is more durable than any repository-specific instruction. 

---

## FINAL SENIOR ENGINEER POSITION

**Observation:** ING_3090 exposed recurring problems around provenance, authority, deletion safety, historical/current distinction, test lineage and architecture boundaries. 

**Evidence:** The E2 and retrospective material demonstrates these problems through actual engineering workflow and explicitly separates Engineer implementation from architecture, acceptance and Git authority. 

**Inference:** Most of the valuable lessons are **Engineer-role invariants**, while repository paths, machines, models, runtimes, branches and milestones are contextual.

**Recommendation:** Extract a **small durable Engineer behavioral contract** and keep project/machine/runtime/milestone information outside it.

**Decision:** **No future Agent-file architecture should be inferred from this review alone.** The review establishes the behavioral boundary, not the storage/layout mechanism.

**Status:** `READ-ONLY REVIEW COMPLETE` — no implementation, repository modification, commit or push performed.

