# GAIA Engineer Local v0.1 — E2 Implementation Handoff

**Status:** PROPOSED / PENDING HUMAN OWNER APPROVAL  
**Track:** GAIA Engineer Local Continuity  
**Phase:** E2 — Controlled Coding Agent  
**Predecessor:** E1 — RTX 3090 Environment Gate  
**Primary target:** Local RTX 3090 + Ollama + Qwen3-Coder 30B

---

## 1. Purpose

E2 defines the first controlled local coding-agent slice for GAIA.

The objective is to prove that a local Engineer runtime can work against the authoritative GAIA repository using bounded filesystem/repository tools, execute validation, produce an inspectable diff, and stop for Human Owner review before any authoritative Git operation.

E2 is a **coding-agent continuity milestone**, not a new GAIA architectural layer.

The local runtime is an implementation/deployment mechanism. It must not become a new GAIA production abstraction.

---

## 2. Current baseline

E1 was executed on the actual Human Owner RTX 3090 environment.

Verified:

- NVIDIA RTX 3090 detected
- 24 GB VRAM
- NVIDIA driver 580.173.02
- CUDA 13.0 reported by `nvidia-smi`
- Ubuntu 26.04 LTS
- Python 3.14.4
- Git 2.53.0
- Bash 5.3.9
- pytest 9.1.1
- Ollama 0.32.13
- Ollama service active
- GAIA repository available locally
- existing GAIA Engineer benchmark runner operational
- six-model benchmark executed with `--performance`

### E1 benchmark result

Current benchmark version: GAIA Engineer Benchmark v1.2.

| Model | Result |
|---|---:|
| qwen2.5-coder-14b | 0/5 |
| qwen3-coder-30b | 5/5 |
| devstral-24b | 4/5 |
| devstral-small-2-24b | 5/5 |
| gpt-oss-20b | 5/5 |
| gemma4-26b | 5/5 |

### E1 candidate selection

Primary E2 candidate:

`qwen3-coder:30b`

Secondary candidates:

`gpt-oss:20b`

`devstral-small-2:latest`

The selection is provisional for E2 and is based on the existing GAIA benchmark results. It is not a permanent architectural decision.

---

## 3. E2 scope

E2 SHALL demonstrate the following controlled loop:

```text
Human Owner task
      ↓
Local Engineer reads repository
      ↓
Engineer searches repository
      ↓
Engineer proposes / performs bounded edits
      ↓
Engineer runs prescribed tests
      ↓
Engineer inspects diff
      ↓
Engineer reports evidence
      ↓
Human Owner reviews
      ↓
Human Owner decides Git action
```

The initial implementation should be the smallest useful slice capable of demonstrating this loop.

---

## 4. Runtime boundary

The expected local runtime is:

```text
GAIA Engineer Local
        ↓
Ollama
        ↓
Qwen3-Coder 30B
        ↓
bounded local tools
        ↓
GAIA repository workspace
```

Ollama remains a local model-serving runtime.

It is NOT a new GAIA architectural component.

E2 must not introduce:

- a generic Provider framework;
- a generic Agent framework inside GAIA production;
- a Resource Registry;
- Planner;
- Memory;
- Event Bus;
- Plugin framework;
- distributed orchestration;
- new production Capability abstractions.

---

## 5. Initial tool contract

The E2 slice should reuse the existing benchmark/tool vocabulary where practical.

Required initial operations:

### `read_file`

Read a file within the authorized workspace.

Requirements:

- path must resolve inside the authorized workspace;
- no arbitrary filesystem access;
- no secrets directory access;
- no SSH/private-key access;
- no credential harvesting;
- failures must be explicit.

### `search`

Search text/patterns inside the authorized workspace.

Requirements:

- search scope is the authorized workspace;
- no unrestricted host filesystem search;
- no private-resource traversal;
- results must identify files/locations sufficiently for human inspection.

### `write_file` / bounded edit

The Engineer must be able to make controlled code/document changes needed for an authorized task.

Requirements:

- path must resolve inside the authorized workspace;
- protected paths must be enforced;
- edits must be inspectable through Git diff;
- no automatic commit/push/merge.

### `run_tests`

Execute an explicitly bounded validation command.

Requirements:

- command must execute inside the authorized workspace;
- no destructive shell operations;
- no arbitrary credential access;
- output must be captured as evidence;
- failures must stop or return control to the Human Owner rather than being silently bypassed.

---

## 6. Workspace boundary

The authoritative repository remains the Human Owner's local checkout.

E2 must not assume that the Engineer owns the repository.

The Engineer works against an explicitly supplied workspace.

The initial target is:

```text
/home/sbatta/github_repos/GAIA
```

but implementation should avoid hard-coding this path where a workspace root can be configured safely.

The workspace boundary must prevent traversal outside the authorized root.

---

## 7. Git safety boundary

E2 MUST NOT autonomously perform:

- `git commit`
- `git push`
- `git merge`
- pull-request creation
- branch deletion
- destructive reset
- force operations
- history rewriting

The Engineer may inspect Git state and diff.

Expected inspection operations include:

```text
git status
git diff
git diff --check
git log
```

The Human Owner remains authoritative for Git state transitions.

---

## 8. Protected architecture boundary

The following remain protected unless a future milestone explicitly authorizes changes:

- ADR-0001
- ADR-0003
- W3 production semantics
- approved Resource identity semantics
- existing Policy/Approval boundary
- production Core architecture
- production Capability semantics

The Engineer must stop and report a governance conflict instead of bypassing the boundary.

A task that requires architectural expansion is a STOP condition, not an invitation to generalize the implementation.

---

## 9. Coding task model

E2 should initially support small, bounded implementation tasks.

A valid task should contain:

- task identifier;
- objective;
- authorized files/area;
- explicit non-goals;
- validation command;
- expected evidence;
- stop conditions.

The Engineer should not infer broad project authority from a narrow task.

---

## 10. Human approval model

The Human Owner remains the final authority.

The Engineer may:

1. inspect;
2. reason;
3. edit within the authorized workspace;
4. execute bounded tests;
5. report the resulting diff/evidence.

The Engineer may NOT independently decide that an architectural or governance boundary should be changed.

The expected approval point is:

```text
Implementation complete
        ↓
Tests complete
        ↓
Diff inspected
        ↓
Evidence prepared
        ↓
HUMAN OWNER REVIEW
        ↓
Git decision
```

---

## 11. Evidence contract

Every E2 controlled coding task should be reconstructable from:

- task identifier;
- starting repository commit;
- files changed;
- commands executed;
- test results;
- `git diff --check`;
- relevant diff/stat;
- model/runtime identity;
- timestamp;
- explicit statement of Human Owner validation status.

No credentials, tokens, private endpoints, or raw secrets may appear in evidence.

---

## 12. E2 acceptance tests

The Engineer implementation should provide tests demonstrating at least:

### E2-T01 — Repository read

Engineer can read an authorized repository file.

### E2-T02 — Repository search

Engineer can locate a known symbol/text inside the workspace.

### E2-T03 — Bounded write

Engineer can modify an explicitly authorized file.

### E2-T04 — Workspace escape blocked

An attempt to access a path outside the workspace is rejected.

### E2-T05 — Protected path blocked

An attempt to modify a protected path without authorization is rejected.

### E2-T06 — Test execution

Engineer can execute a prescribed GAIA test command and capture its result.

### E2-T07 — Diff evidence

Engineer can produce an inspectable diff after a controlled change.

### E2-T08 — Git mutation blocked

Engineer cannot autonomously commit, push, merge, or rewrite history.

### E2-T09 — Secret hygiene

Engineer cannot read configured secret files or expose credentials through evidence.

### E2-T10 — Stop-condition behavior

An architectural/governance conflict produces a STOP result rather than an unauthorized change.

---

## 13. E2 trial task

The first real coding trial should be deliberately small.

It should:

- modify a non-protected test/documentation area;
- require reading existing GAIA code;
- require repository search;
- require a bounded edit;
- require a deterministic test;
- produce a human-reviewable diff.

The first trial should NOT modify:

- `src/gaia/**` production semantics;
- ADR-0001;
- ADR-0003;
- PM-002 Resource binding;
- W3 architecture.

---

## 14. Performance considerations

The RTX 3090 benchmark established that the local environment can run the candidate models.

E2 should record model/runtime identity and basic execution timing, but performance optimization is not the primary acceptance criterion.

Correctness, boundary enforcement, reproducibility and human control have priority over raw token throughput.

Do not introduce speculative inference infrastructure merely to improve benchmark numbers.

---

## 15. Secondary model policy

If Qwen3-Coder 30B is unavailable or unsuitable during E2 trials, the approved experimental alternatives are:

1. GPT-OSS 20B
2. Devstral Small 2 24B

Switching the candidate model for an E2 trial does not change GAIA architecture.

The selected runtime/model must be recorded in evidence.

---

## 16. Stop conditions

E2 MUST STOP if implementation requires:

- modification of ADR-0001 or ADR-0003;
- new production architecture;
- new generic Agent/Provider/Registry abstraction;
- Memory, Planner, Event Bus or Plugin infrastructure;
- unrestricted host filesystem access;
- automatic Git mutation;
- credential access;
- bypassing Policy/Approval boundaries;
- modifying PM-002 Resource identity/reference;
- weakening protected-file enforcement;
- distributed runtime/orchestration.

Any such requirement must return to Human Owner / Architect governance.

---

## 17. Deliverable expected from Engineer

After authorization, the Engineer should provide a complete implementation package containing:

- implementation files;
- tests;
- configuration examples;
- E2 evidence;
- implementation manifest;
- validation results;
- SHA-256 of the package.

The Engineer must not commit, push, merge or create a PR unless explicitly authorized by the Human Owner workflow.

---

## 18. Human Owner validation

After receiving the Engineer package, the Human Owner must:

1. verify package identity/hash;
2. apply it to the authoritative local checkout;
3. run E2 tests;
4. inspect Git diff;
5. verify protected files are unchanged;
6. perform the first controlled coding trial;
7. verify stop conditions;
8. record authoritative local evidence.

Engineer validation is not a substitute for Human Owner validation.

---

## 19. Architect review gate

After Human Owner validation, Architect review should verify:

- E2 remains a local coding continuity layer;
- no GAIA production architecture was broadened;
- Git authority remains with Human Owner;
- filesystem boundary is enforced;
- protected architecture remains protected;
- evidence is reconstructable;
- the selected model/runtime is recorded;
- no hidden autonomous behavior was introduced.

Only after this review should E2 be classified COMPLETE.

---

## 20. Relationship to PM-002

PM-002 remains an independent track.

Current PM-002 state:

```text
Operational validation: BLOCKED
Resource: home.light.living_room
Provider reference: light.living_room
Reason: provider reference currently returns 404
Engineer PM-002 changes: STOPPED
```

E2 does not authorize changing that binding and must not introduce a workaround.

The PM-002 block does not prevent the E2 continuity track from proceeding.

---

## 21. Non-goals

E2 does NOT attempt to:

- replace all existing ChatGPT project actors;
- migrate the entire GAIA governance model to local inference;
- reproduce every cloud-agent feature;
- build a multi-agent framework;
- build a persistent memory system;
- introduce a database;
- integrate the QNAP;
- build the Home Assistant collaborator;
- build the RTX 1070 domestic collaborator;
- build the RTX 3090 as a general-purpose multi-agent server;
- solve long-term knowledge migration;
- finalize E3 knowledge transfer.

Those are future roadmap concerns.

---

## 22. E2 completion criteria

E2 may be considered complete only when all are true:

- local Qwen3-Coder 30B Engineer runtime operates on the RTX 3090;
- authorized workspace access works;
- repository read/search works;
- bounded editing works;
- test execution works;
- workspace escape is blocked;
- protected paths are blocked;
- Git mutation is blocked;
- secret access is blocked;
- controlled coding trial succeeds;
- evidence is reconstructable;
- Human Owner authoritative validation is PASS;
- Architect review is APPROVE.

Until then:

**E2 = IN PROGRESS / NOT COMPLETE**

---

## 23. Governance status

**PROPOSED / PENDING HUMAN OWNER APPROVAL**

This document is an implementation handoff proposal.

It does not authorize implementation by itself.

The Engineer must remain STOPPED until the Human Owner explicitly authorizes E2 implementation.

