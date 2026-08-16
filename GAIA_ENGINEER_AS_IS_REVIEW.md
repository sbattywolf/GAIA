# GAIA Engineer — As-Is Review

## 1. Executive Summary

GAIA è un Personal AI Operating System local-first per un Human Owner, basato su Collaborator specializzati, confini espliciti e controllo umano. Il repository separa riferimenti correnti, ricerca, ADR, validation, POC e legacy. [README.md](README.md), [reference/IDENTITY.md](reference/IDENTITY.md), [reference/REPOSITORY_STRUCTURE.md](reference/REPOSITORY_STRUCTURE.md)

L'implementazione corrente è il bootstrap POC in gaia-bootstrap-poc; src resta un placeholder. La POC esercita un solo flusso Home read-only con Adapter falso sostituibile, non il sistema GAIA completo. [src/README.md](src/README.md), [gaia-bootstrap-poc/README.md](gaia-bootstrap-poc/README.md)

## 2. Repository and Documentation Landscape

| Area | Stato e scopo |
|---|---|
| README e reference | Working truth per identità, principi, modello, semantica e roadmap; varie versioni v0.2 sono Proposed. [README.md](README.md), [reference/ARCHITECTURE_CONVERGENCE_v0.2.md](reference/ARCHITECTURE_CONVERGENCE_v0.2.md) |
| adr | ADR-0001 è Accepted; esiste una copia Accepted di ADR-0003; gli altri sono Proposed. [adr/ADR-0001-Core-Boundary.md](adr/ADR-0001-Core-Boundary.md), [adr/ADR-0003-Capability-Model_Accepted.md](adr/ADR-0003-Capability-Model_Accepted.md) |
| sprint-01 e sprint-02 | Ricerca, critica e sintesi storiche ricostruite; non architettura corrente. [sprint-01/README.md](sprint-01/README.md), [sprint-02/README.md](sprint-02/README.md) |
| sprint-03 | Validation, scenario Home e artefatti POC. [sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md](sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md), [sprint-03/engineer-agent/PROJECT_HISTORY.md](sprint-03/engineer-agent/PROJECT_HISTORY.md) |
| reports e prompts | Provenienza/recupero e prompt manuali di ripresa, non decisioni architetturali. [reports/RECONSTRUCTION_REPORT.md](reports/RECONSTRUCTION_REPORT.md), [prompts/NEXT_RESEARCH_SESSION.md](prompts/NEXT_RESEARCH_SESSION.md) |
| oldRepoReferences | Legacy Zeus, reference-only. [AGENTS.md](AGENTS.md), [sprint-03/engineer-agent/POC_REUSE_ASSESSMENT.md](sprint-03/engineer-agent/POC_REUSE_ASSESSMENT.md) |

AGENTS.md è l'istruzione operativa primaria. Le sole istruzioni IDE sono Copilot/Mermaid; .agents e .codex sono vuote. [AGENTS.md](AGENTS.md), [.github/copilot-instructions.md](.github/copilot-instructions.md), [.github/instructions/mermaid.instructions.md](.github/instructions/mermaid.instructions.md)

## 3. GAIA Evolution: Sprint 1 → Sprint 2 → Sprint 3

Sprint 1 ha definito identità, criterio di riuso e decisioni aperte: riusare framework ai boundary senza consegnare loro stato o identità GAIA. [sprint-01/01_Framework_Research.md](sprint-01/01_Framework_Research.md), [sprint-01/03_Reuse_Analysis.md](sprint-01/03_Reuse_Analysis.md), [sprint-01/ARCHITECTURE_DISCUSSION_GUIDE.md](sprint-01/ARCHITECTURE_DISCUSSION_GUIDE.md)

Sprint 2 ha stressato il modello su World Model, failure, pattern e sostenibilità, confermando evidenza prima della generalizzazione; Memory, orchestrazione, Registry ed eventi restano aperti. [sprint-02/SPRINT_02_SYNTHESIS.md](sprint-02/SPRINT_02_SYNTHESIS.md), [sprint-02/04_Hidden_Bottlenecks.md](sprint-02/04_Hidden_Bottlenecks.md)

Sprint 3 ha prodotto convergenza v0.2, validation e bootstrap POC. Il primo scenario è leggere aperture Home mostrando esplicitamente ambiguità, staleness e indisponibilità. [reference/GAIA_MODEL_v0.2.md](reference/GAIA_MODEL_v0.2.md), [sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md](sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md), [sprint-03/engineer-agent/PROJECT_HISTORY.md](sprint-03/engineer-agent/PROJECT_HISTORY.md)

## 4. Current GAIA Model

I sette concetti first-class sono Identity, Core, Collaborator, Domain, Capability, Resource e Shared Context. World Model, Memory, Policy, Approval, Audit, Adapter, Tool, Event e Run sono vocabolario di supporto/provvisorio. [reference/GAIA_MODEL_v0.2.md](reference/GAIA_MODEL_v0.2.md)

World Model definisce significato, Context rilevanza corrente, Memory retention, Knowledge comprensione e Audit evidenza: non implicano servizi o database. [reference/ARCHITECTURE_CONVERGENCE_v0.2.md](reference/ARCHITECTURE_CONVERGENCE_v0.2.md), [reference/WORLD_MODEL_v0.2.md](reference/WORLD_MODEL_v0.2.md), [reference/CONTEXT_MODEL_v0.2.md](reference/CONTEXT_MODEL_v0.2.md)

## 5. Current Architecture

Il flusso target minimo separa Channel Adapter, Core, Collaborator, Capability/Resource scope, Policy/Approval, Execution Adapter, Structured Outcome e Channel Adapter. È una ripartizione di responsabilità, non una prescrizione di servizi o classi. [adr/ADR-0001-Core-Boundary.md](adr/ADR-0001-Core-Boundary.md), [reference/ARCHITECTURE_TO_CODE_v0.1.md](reference/ARCHITECTURE_TO_CODE_v0.1.md)

Core coordina ed enforcement, non logica Home; il Domain interpreta label/semantica; l'Adapter traduce I/O; la Capability definisce il cosa e non il come. Home Assistant è fonte autorevole solo per lo stato selezionato nello scenario e il suo ruolo definitivo è aperto. Telegram, Planner, Registry, Plugin, Event Bus e orchestrazione sono fuori POC. [adr/ADR-0001-Core-Boundary.md](adr/ADR-0001-Core-Boundary.md), [adr/ADR-0003-Capability-Model_Accepted.md](adr/ADR-0003-Capability-Model_Accepted.md), [adr/ADR-0004-HomeAssistant-Boundary.md](adr/ADR-0004-HomeAssistant-Boundary.md), [gaia-bootstrap-poc/docs/IMPLEMENTATION_NOTES.md](gaia-bootstrap-poc/docs/IMPLEMENTATION_NOTES.md)

## 6. ADR Landscape

| ADR | Stato | Decisione / vincolo |
|---|---|---|
| 0001 Core Boundary | Accepted | Core in-process minimo per Request, routing, Context limitato, scope, enforcement, delega ed evidenza; esclude logica Domain, Memory, Planner, Registry, Event Bus e Plugin. [adr/ADR-0001-Core-Boundary.md](adr/ADR-0001-Core-Boundary.md) |
| 0003 Capability Model | Proposed + copia Accepted | Capability separa definition, Resource scope, Policy Result, Approval, binding ed evidence; Read/Propose/Act, tre livelli di rischio e Indeterminate non eseguibile. Dipende da 0001. [adr/ADR-0003-Capability-Model.md](adr/ADR-0003-Capability-Model.md), [adr/ADR-0003-Capability-Model_Accepted.md](adr/ADR-0003-Capability-Model_Accepted.md) |
| 0002 Memory | Proposed | Retention, provenienza, correzione/forgetting e separazione da Context/Audit prima della tecnologia. [adr/ADR-0002-Memory-Semantics.md](adr/ADR-0002-Memory-Semantics.md) |
| 0004 Home Assistant | Proposed | Ruolo HA, ownership di state/registry, failure, migrazione e rollback. [adr/ADR-0004-HomeAssistant-Boundary.md](adr/ADR-0004-HomeAssistant-Boundary.md) |
| 0005 Communication State | Proposed | Ordering, duplicati, identità, sessione e continuità tra canale e GAIA. [adr/ADR-0005-Communication-State.md](adr/ADR-0005-Communication-State.md) |
| 0006 Tool Trust | Proposed | Read/write, impatto, credenziali, retry/idempotenza e verifica senza usare prompt come security boundary. [adr/ADR-0006-Tool-Trust.md](adr/ADR-0006-Tool-Trust.md) |
| 0007 Event/Run | Proposed | Correlazione, causalità, lifecycle, errori, retention e replay. [adr/ADR-0007-Event-Semantics.md](adr/ADR-0007-Event-Semantics.md) |

Contraddizione AS-IS: adr/README e ADR_CANDIDATES dichiarano tutti gli ADR proposti; ADR-0001 e la copia suffissata di ADR-0003 sono Accepted. Anche le reference v0.2 restano Proposed e descrivono gli ADR come futuri. Non determinabile quale indice sia l'ultimo autorevole. [adr/README.md](adr/README.md), [adr/ADR_CANDIDATES.md](adr/ADR_CANDIDATES.md), [reference/NEXT_STEPS_v0.2.md](reference/NEXT_STEPS_v0.2.md)

## 7. Current Bootstrap POC

La POC compone esplicitamente RequestRouter, HomeResourceResolver, ReadOpeningStateCapability e FakeHomeAssistantAdapter. Separa ResourceId canonico da HomeResourceReference, risolve label prima dell'I/O e restituisce outcome strutturati. [gaia-bootstrap-poc/src/gaia/bootstrap.py](gaia-bootstrap-poc/src/gaia/bootstrap.py), [gaia-bootstrap-poc/src/gaia/home/resource_resolver.py](gaia-bootstrap-poc/src/gaia/home/resource_resolver.py), [gaia-bootstrap-poc/src/gaia/home/read_opening_state_capability.py](gaia-bootstrap-poc/src/gaia/home/read_opening_state_capability.py)

Il Fake Adapter è in-memory e deterministico, con timestamp fisso timezone-aware, nessuna rete/autenticazione/polling/fallback. La replaceability è verificata con AlternativeProvider che soddisfa OpeningStateProvider senza modificare router o Domain flow. [gaia-bootstrap-poc/src/gaia/adapters/fake_home_assistant_adapter.py](gaia-bootstrap-poc/src/gaia/adapters/fake_home_assistant_adapter.py), [gaia-bootstrap-poc/tests/test_replaceability.py](gaia-bootstrap-poc/tests/test_replaceability.py)

I test coprono success, sconosciuto/ambiguo senza chiamata provider, unavailable/stale, risposta malformata, eccezione, unsupported e autorità della source rispetto a inferenza/cache. Il risultato registrato è 15 test passati; non sono stati rieseguiti per non generare artefatti nel workspace. [gaia-bootstrap-poc/tests](gaia-bootstrap-poc/tests), [gaia-bootstrap-poc/TEST_RESULTS.txt](gaia-bootstrap-poc/TEST_RESULTS.txt)

Non dimostra integrazione HA/Telegram reale, policy/approval, persistenza, freshness reale, multi-Resource, Memory, Audit operativo, Tool Trust, Event/Run o production readiness. Denied e Indeterminate esistono solo come vocabolario. [gaia-bootstrap-poc/docs/IMPLEMENTATION_NOTES.md](gaia-bootstrap-poc/docs/IMPLEMENTATION_NOTES.md), [gaia-bootstrap-poc/src/gaia/home/outcomes.py](gaia-bootstrap-poc/src/gaia/home/outcomes.py)

## 8. Legacy Project Relationship

Il legacy Zeus include client HA, resolver/intent, formatter, agente Telegram, test, configurazioni esempio, systemd, Docker/Open WebUI e runbook. È utile solo come evidence su protocolli, stati, failure mode, mapping e disciplina operativa. [oldRepoReferences/AI-HOME/1070/app](oldRepoReferences/AI-HOME/1070/app), [oldRepoReferences/AI-HOME/1070/tests](oldRepoReferences/AI-HOME/1070/tests), [oldRepoReferences/AI-HOME/docs/03_IMPLEMENTATION_PLAN_1070.md](oldRepoReferences/AI-HOME/docs/03_IMPLEMENTATION_PLAN_1070.md)

Non è baseline GAIA né materiale riusabile automaticamente: il riuso richiede ispezione, sanitizzazione, compatibilità di boundary e test; segreti, dati domestici e coupling canale/Home/Core sono esclusi. [AGENTS.md](AGENTS.md), [sprint-03/engineer-agent/POC_REUSE_ASSESSMENT.md](sprint-03/engineer-agent/POC_REUSE_ASSESSMENT.md)

## 9. GAIA Engineer — Current Role

1. Ruolo: tradurre evidenza e decisioni documentate in incrementi piccoli e verificabili, preservando boundary, replaceability e controllo umano. [AGENTS.md](AGENTS.md), [reference/DESIGN_PRINCIPLES.md](reference/DESIGN_PRINCIPLES.md)
2. Può assumere: analisi repository, implementazione focalizzata entro decisioni accettate, contratti/Adapter, test deterministici e verifiche diff. [AGENTS.md](AGENTS.md)
3. Non deve assumere: inventare concetti, promuovere ricerca a decisione, introdurre infrastruttura senza evidenza, importare legacy/segreti o mettere semantica Home nel Core. [AGENTS.md](AGENTS.md), [reference/ARCHITECTURE_CONVERGENCE_v0.2.md](reference/ARCHITECTURE_CONVERGENCE_v0.2.md)
4. Richiedono Human Owner/Architect: acceptance/supersession ADR, Memory, HA boundary, communication state, tool trust, eventi, azioni sensibili e conflitti di autorità. [adr](adr), [reference/ARCHITECTURE_CONVERGENCE_v0.2.md](reference/ARCHITECTURE_CONVERGENCE_v0.2.md)

## 10. Engineer Boundaries and Constraints

Prima di modificare: leggere README, reference, ADR accettati, sprint/validation pertinenti e codice coinvolto. Dopo: eseguire test rilevanti, controllare diff e coerenza ADR. Legacy e segreti non vanno modificati né esposti. [AGENTS.md](AGENTS.md)

## 11. Current Development Workflow

1. Classificare il task rispetto a fonti, ADR e scenario.
2. Ispezionare codice e test del boundary.
3. Applicare il cambiamento minimo, senza generalizzare.
4. Eseguire test e controlli di diff.
5. Registrare evidenza e limiti senza renderli architettura implicita.

Il toolset minimo deducibile è Git, Python compatibile con POC, pytest e strumenti di lettura/diff. Non è documentata una necessità attuale di framework agentico, Docker, HA o Telegram per iniziare sul bootstrap. [AGENTS.md](AGENTS.md), [gaia-bootstrap-poc/pyproject.toml](gaia-bootstrap-poc/pyproject.toml), [reference/NEXT_STEPS_v0.2.md](reference/NEXT_STEPS_v0.2.md)

## 12. Open Questions and Ambiguities

- Il ruolo definitivo di Home Assistant resta aperto in ADR-0004. [adr/ADR-0004-HomeAssistant-Boundary.md](adr/ADR-0004-HomeAssistant-Boundary.md)
- Memory non ha semantica accettata; nessuna Memory necessaria è un esito valido. [sprint-03/MEMORY_ROLE_VALIDATION.md](sprint-03/MEMORY_ROLE_VALIDATION.md)
- Communication State, Tool Trust ed Event/Run non hanno decisione runtime. [adr/ADR-0005-Communication-State.md](adr/ADR-0005-Communication-State.md), [adr/ADR-0006-Tool-Trust.md](adr/ADR-0006-Tool-Trust.md), [adr/ADR-0007-Event-Semantics.md](adr/ADR-0007-Event-Semantics.md)
- L'autorità effettiva di ADR/reference è contraddittoria; non determinabile senza decisione umana.

## 13. Gaps and Risks

| Priorità | Classe | Evidenza |
|---|---|---|
| IMPORTANT | documentazione ambigua | Stato ADR incoerente tra indice/candidate, ADR-0001, due copie ADR-0003 e roadmap. Va chiarito prima di modifiche architetturali. [adr/README.md](adr/README.md), [adr/ADR-0003-Capability-Model_Accepted.md](adr/ADR-0003-Capability-Model_Accepted.md), [reference/NEXT_STEPS_v0.2.md](reference/NEXT_STEPS_v0.2.md) |
| IMPORTANT | implementazione mancante | Manca la production slice: Adapter HA/Telegram reali, Policy/Approval, evidence e recovery. Sono esclusioni deliberate del POC, non bug POC. [gaia-bootstrap-poc/docs/IMPLEMENTATION_NOTES.md](gaia-bootstrap-poc/docs/IMPLEMENTATION_NOTES.md), [reference/NEXT_STEPS_v0.2.md](reference/NEXT_STEPS_v0.2.md) |
| IMPORTANT | decisione aperta | Servono evidenze su stati HA, freshness, timeout/failure ed entità mancanti prima del reale Adapter. [sprint-03/engineer-agent/PROJECT_HISTORY.md](sprint-03/engineer-agent/PROJECT_HISTORY.md) |
| MINOR | provenienza | Parte di Sprint 1/2 è ricostruita: history/evidence, non fonte primaria definitiva. [sprint-01/README.md](sprint-01/README.md), [reports/RECONSTRUCTION_REPORT.md](reports/RECONSTRUCTION_REPORT.md) |
| MINOR | implementazione POC | Policy/Approval e Denied/Indeterminate non sono esercitati nel POC read-only. [gaia-bootstrap-poc/docs/IMPLEMENTATION_NOTES.md](gaia-bootstrap-poc/docs/IMPLEMENTATION_NOTES.md) |
| INFORMATIONAL | futuro | Planner, Registry, Event Bus, Plugin e multi-Domain sono differiti. [reference/NEXT_STEPS_v0.2.md](reference/NEXT_STEPS_v0.2.md) |

Non emerge un BLOCKER per progettare e revisionare il prossimo Adapter; la contraddizione di autorità è invece blocker per cambiamenti che modifichino boundary.

## 14. Recommended Immediate Engineering Step

Preparare e sottoporre a review REAL_HOME_ASSISTANT_ADAPTER_DESIGN.md, senza implementarlo: deve conservare il seam OpeningStateProvider salvo evidenza contraria e definire raccolta evidence sanitizzata su stati, staleness, timeout, mapping tra reference esterne e ResourceId, e test. Se emergesse un cambio di boundary, va confrontato prima con ADR-0001/0003 e ADR-0004 proposto. [sprint-03/engineer-agent/PROJECT_HISTORY.md](sprint-03/engineer-agent/PROJECT_HISTORY.md), [sprint-03/engineer-agent/POC_REUSE_ASSESSMENT.md](sprint-03/engineer-agent/POC_REUSE_ASSESSMENT.md)

## 15. Engineer Understanding Check

- La POC prova che il Domain risolve label prima dell'Adapter e che source/caching/inferenza non generano falsa certezza. [gaia-bootstrap-poc/tests/test_domain_resolution.py](gaia-bootstrap-poc/tests/test_domain_resolution.py), [gaia-bootstrap-poc/tests/test_authority_rules.py](gaia-bootstrap-poc/tests/test_authority_rules.py)
- Core non deve assimilare Home, Telegram, Memory o orchestrazione; una Capability non è client o Tool. [adr/ADR-0001-Core-Boundary.md](adr/ADR-0001-Core-Boundary.md), [adr/ADR-0003-Capability-Model_Accepted.md](adr/ADR-0003-Capability-Model_Accepted.md)
- Per ogni task l'Engineer verifica autorità delle fonti, applica il minimo cambiamento, testa boundary e dichiara ciò che resta indeterminato. [AGENTS.md](AGENTS.md)
