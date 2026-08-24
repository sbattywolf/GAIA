# ZEUS SAFE-HEADROOM ARCHITECTURE
## Local AI, Home Assistant, UniFi e piattaforma multi-nodo

**Versione:** 3.0 — riscritta da zero  
**Data:** 27 luglio 2026  
**Principio guida:** affidabilità e margine operativo prima della dimensione del modello.

---

# 1. Decisione principale

La RTX 3090 ha 24 GB di VRAM, ma non è opportuno progettare l'ambiente quotidiano attorno a un modello da circa 19–20 GB sempre residente.

La VRAM non serve solo ai pesi del modello. Durante l'inferenza servono ulteriori risorse per contesto/KV cache, runtime, eventuale elaborazione immagini e altri processi GPU. Per questo ZEUS LAB userà un modello da 14B come predefinito e considererà i modelli più grandi soltanto come profilo on-demand sottoposto a benchmark.

Scelta predefinita sulla RTX 3090:

```bash
ollama pull qwen2.5-coder:14b
```

Profilo alternativo generalista/router:

```bash
ollama pull qwen3:14b
```

Modello di compatibilità con la GTX 1070:

```bash
ollama pull qwen2.5-coder:7b
```

`qwen3-coder:30b` non è vietato, ma non è il modello predefinito. Potrà essere provato più avanti in un profilo “heavy”, con un solo job, context limitato e controllo della VRAM.

---

# 2. Modelli assegnati per ruolo

## RTX 3090 — modello principale

```text
qwen2.5-coder:14b (Q4_K_M)
```

Utilizzi:

- audit del repository;
- Python e Docker;
- refactoring controllato;
- test;
- Home Assistant YAML;
- generazione patch;
- Git/Linear tool design;
- analisi dei log di Zeus.

Il pacchetto Ollama ufficiale è circa 9 GB, usa quantizzazione Q4_K_M e dichiara un context di 32K. L'uso operativo iniziale deve comunque partire da 8K o 16K, aumentando soltanto dopo misurazione.

## RTX 3090 — modello opzionale generalista

```text
qwen3:14b (Q4_K_M)
```

Utilizzi:

- architettura;
- classificazione;
- ragionamento generale;
- valutazione prompt;
- analisi multi-dominio Home Assistant/UniFi.

Il pacchetto Ollama ufficiale è circa 9,3 GB e dichiara context 40K.

Non mantenere entrambi caricati senza necessità. Ollama può conservarli su disco; il profilo di lavoro seleziona un modello alla volta.

## GTX 1070 — runtime H24

```text
qwen2.5-coder:7b
```

Utilizzi:

- Zeus gateway/router;
- classificazione strutturata;
- risposte brevi;
- Home Assistant runtime;
- fallback locale.

## Modelli heavy futuri

Candidati:

```text
qwen3-coder:30b     ~19 GB
Devstral Small 2    ~15 GB
```

Non sono necessari per la Fase 1. Devstral Small 2 è più grande del profilo 14B, include capacità agentiche e tool use, ma il pacchetto Ollama è circa 15 GB; rimane quindi un benchmark futuro, non il default.

---

# 3. Visione del sistema

```text
                         CANALI
       Telegram | HA Assist/App/Voice | Open WebUI
                            |
                            v
                     ZEUS GATEWAY
                 identity + audit + mode
                            |
                            v
                       POLICY LAYER
              risk + allowlist + confirmation
                            |
                            v
                      ROUTER/REGISTRY
              /             |              \
             v              v               v
       HOME RUNTIME     CODING WORKER     ANALYST
           1070          3090/on-demand     3090
             |              |               |
       HA read/control   Git/Linear      reports/tests
              \             |              /
               \------------+-------------/
                            |
                  ARTEFACTS + TELEMETRY
                            |
                         QNAP
```

Il modello non deve eseguire direttamente operazioni sensibili. Esso interpreta; i tool deterministici validano ed eseguono; le policy autorizzano o negano.

---

# 4. Ruolo di ogni macchina

## Raspberry Pi 4 — HOME ASSISTANT PRODUCTION

È il sistema autorevole della casa:

- sensori porte/finestre;
- movimento;
- wall switch;
- luci;
- power plug;
- climate/termosifoni;
- webcam;
- automazioni;
- monitoring NAS e UniFi;
- Assist e pipeline voce.

Non ospita LLM pesanti.

## MSI GTX 1070 Max-Q / 32 GB / Ubuntu — ZEUS EDGE

Nodo H24:

- Ollama 7B;
- Open WebUI;
- Telegram;
- Whisper;
- Piper;
- Glances;
- Home runtime;
- logging;
- dispatch alla 3090;
- continuità operativa anche quando la 3090 è spenta.

## Desktop 5950X / RTX 3090 / 64 GB — ZEUS LAB

Nodo di sviluppo e analisi:

- VS Code;
- Git;
- Docker/Dev Containers;
- Ollama 14B principale;
- istanza HA test isolata;
- audit e testing;
- analisi automazioni/history;
- produzione di release per la 1070;
- job pesanti on-demand.

## QNAP TS-251+ / 8 GB / 4 TB — ZEUS STORAGE

- backup;
- snapshot;
- dataset sanitizzati;
- report;
- artefatti di release;
- repository mirror opzionale;
- persistence futura leggera.

Non è un nodo di inferenza principale.

---

# 5. Stato corrente da preservare

Stack Docker 1070:

```text
ollama
open-webui
wyoming-whisper
wyoming-piper
glances
```

Non aggiungere in Fase 1:

```text
OpenClaw
LangGraph
CrewAI
AutoGen
n8n
Qdrant
PostgreSQL
MCP
```

File esistenti importanti:

```text
telegram_agent.py
domotics_agent.py
git_flow_manager.py
core_lib/linear_api.py
docker-compose.yml
ha-telegram-agent.service
inventory.json
```

Problemi già osservati in `telegram_agent.py`:

- URL Ollama contaminato da HTML;
- typo nel return del comando `/start`;
- intent descritti e rami implementati non coerenti;
- HTTP sincrono dentro handler asincrono;
- JSON non validato in modo robusto;
- import/runtime path hardcoded;
- azioni Git/Linear premature.

`domotics_agent.py` è un event collector, non un agente AI. Non riscriverlo in Fase 1.

`git_flow_manager.py` combina Linear, Git e GitHub. Deve restare inattivo finché non verrà separato in tool testati.

---

# 6. Principi non negoziabili

1. 1070 = production.
2. 3090 = lab, test e heavy compute.
3. Raspberry = autorità della casa.
4. QNAP = memoria e artefatti.
5. Un agente non bypassa mai le policy.
6. Nessun secret nei prompt, log o repository.
7. Ogni modifica è piccola, testata e reversibile.
8. Nessuna azione Git, Linear, GitHub, UniFi o HA critica in automatico.
9. La 1070 continua a funzionare se la 3090 è offline.
10. Prima si osserva, poi si simula, infine si abilita una allowlist.

Loop di miglioramento:

```text
OBSERVE -> NORMALISE -> ANALYSE -> PROPOSE
-> TEST -> APPROVE -> DEPLOY -> MEASURE
```

---

# 7. Modalità runtime

```text
OBSERVE
- classifica
- registra
- non esegue

DRY_RUN
- classifica
- genera piano e candidate
- non modifica sistemi

EXECUTE
- solo tool allowlisted
- policy check
- audit
- verifica post-azione
```

La Fase 1 parte integralmente in `OBSERVE`.

---

# 8. Livelli di rischio

## R0 — Lettura

- stato luci;
- porte/finestre;
- temperature;
- movimento;
- consumo;
- rete/availability.

## R1 — Reversibile e basso impatto

- luce on/off;
- luminosità;
- plug esplicitamente non critica.

## R2 — Impatto medio

- climate;
- automazioni;
- riavvio device di rete;
- plug con carichi importanti.

Richiede conferma.

## R3 — Critico

- lock/allarme;
- firewall/VLAN/VPN;
- spegnimento NAS/host;
- webcam sensibile;
- merge/deploy;
- modifiche production alle automazioni.

Mai autonomo.

---

# 9. UniFi e subnet future

Zone logiche proposte:

```text
TRUSTED_CLIENTS
AI_EDGE
AI_LAB
HOME_AUTOMATION
IOT
STORAGE
GUEST
VPN
```

Non applicare questa segmentazione senza inventario reale.

Principi:

- deny-by-default tra zone;
- sole porte necessarie;
- niente esposizione Internet di Ollama, Open WebUI, Glances o HA;
- accesso remoto via VPN;
- token distinti production/test;
- UniFi agent inizialmente read-only;
- analizzare mDNS, SSDP, MQTT, webcam e discovery prima di bloccare traffico inter-VLAN.

Matrice concettuale:

```text
TRUSTED_CLIENTS -> AI_EDGE: amministrazione
TRUSTED_CLIENTS -> AI_LAB: sviluppo
AI_EDGE -> HOME_AUTOMATION: HA API/WebSocket
HOME_AUTOMATION -> AI_EDGE: Ollama/voice necessari
AI_EDGE -> AI_LAB: job autenticati
AI_LAB -> HA TEST: sviluppo/test
AI_EDGE/AI_LAB -> STORAGE: dataset/artefatti
VPN -> servizi strettamente autorizzati
```

---

# 10. Ambiente Home Assistant di test sulla 3090

Creare un ambiente separato dal Raspberry:

- Home Assistant Container o devcontainer;
- porta differente;
- hostname differente;
- secrets e token differenti;
- database separato;
- rete Docker isolata;
- nessun accesso diretto ai dispositivi fisici;
- helper/mock per luci, finestre, movimento, climate e plug;
- fixture YAML sanitizzate;
- eventuale bot Telegram test separato.

Scopi:

- validare tool;
- simulare eventi;
- testare automazioni;
- testare prompt/router;
- evitare azioni involontarie sulla casa reale.

---

# 11. Roadmap

## FASE 0 — Baseline e recovery

### Obiettivo

Rendere l'ambiente reversibile prima di modificarlo.

### Attività

- backup HA e verifica del percorso di restore;
- Git status e branch dedicato;
- `.gitignore` per secrets, database, backup, log e artefatti sensibili;
- snapshot del compose risolto;
- inventario versioni container/Python/dipendenze;
- inventario porte;
- un solo `inventory.json` autorevole;
- verifica unit systemd;
- nessun cambio funzionale.

### Prompt Fase 0

```text
Agisci come senior DevOps e Home Assistant engineer. Leggi il documento ZEUS_SAFE_HEADROOM_ARCHITECTURE.md e poi l'intero repository. Non modificare codice applicativo. Verifica backup, restore path, Git, .gitignore, secrets handling, Docker Compose, systemd, dipendenze, path assoluti e porte esposte. Fornisci un solo step per volta con comando, output atteso, rischio e rollback. Non mostrare valori segreti.
```

### Gate

- restore documentato;
- working tree noto;
- secrets non tracciati;
- servizi riavviabili.

---

## FASE 1 — Zeus Learning Gateway

### Obiettivo

Ricevere, classificare e registrare senza eseguire azioni.

Categorie:

```text
HOME
CODING
LINEAR
GITHUB
SCRUM
SYSTEM
NETWORK
UNKNOWN
```

Log JSONL:

```json
{
  "schema_version": 1,
  "request_id": "uuid",
  "timestamp": "ISO-8601",
  "channel": "telegram",
  "message": "testo",
  "category": "HOME",
  "action": "GET_OPEN_WINDOWS",
  "risk_level": 0,
  "mode": "observe",
  "executed": false,
  "success": null,
  "latency_ms": null,
  "model": "qwen2.5-coder:7b",
  "router_version": "0.1",
  "error": null
}
```

La confidence del modello può essere registrata, ma non determina da sola l'autorizzazione.

### Prompt Fase 1

```text
Agisci come senior Python engineer specializzato in sistemi asincroni e gateway agentici sicuri. Mantieni telegram_agent.py come entrypoint e modifica il minimo indispensabile. Prima esegui un audit completo del file. Poi prepara una patch che conserva ALLOWED_CHAT_ID, usa core_lib.secrets senza esporre valori, chiama Ollama senza bloccare l'event loop, valida il JSON, normalizza category/action, usa fallback UNKNOWN, aggiunge request_id e log JSONL append-only. Tutte le categorie devono essere in OBSERVE. Non importare git_flow_manager, non chiamare Linear/GitHub/Git e non controllare Home Assistant. Aggiungi test con Telegram e Ollama mockati. Mostra diff, test, risultato atteso e rollback prima di applicare.
```

### Gate

- ricezione Telegram stabile;
- fallback se Ollama è assente;
- nessuna esecuzione reale;
- log senza token;
- test per tutte le categorie.

---

## FASE 2 — Home Assistant read-only

### Obiettivo

Interrogare la casa senza modificarla.

### Attività

- tool HA read-only;
- snapshot sanitizzato;
- query finestre, luci, movimento, temperature, plug e UniFi entities;
- alias/entity mapping verificato;
- fixture di test;
- nessun service call.

### Prompt Fase 2

```text
Agisci come Home Assistant integration engineer. Implementa un tool read-only separato dal router. Usa RASPBERRY_IP e HA_TOKEN da core_lib.secrets senza loggarli. Applica timeout e restituisci dati strutturati. Non consentire service call. Genera uno snapshot sanitizzato e query deterministiche per porte/finestre, movimento, luci, climate, plug e UniFi entities. Testa con fixture e HA test, mai con scritture production.
```

---

## FASE 3 — Home control allowlisted

### Obiettivo

Abilitare soltanto azioni R1 esplicitamente consentite.

### Attività

- policy YAML;
- read tool separato dal control tool;
- allowlist entity/domain/service;
- dry-run;
- validazione parametri;
- idempotenza;
- conferma per R2;
- verifica post-azione;
- audit.

### Prompt Fase 3

```text
Agisci come Home Assistant engineer orientato alla sicurezza. L'LLM può proporre un'intenzione, ma non può chiamare direttamente Home Assistant. Crea un control tool deterministico e un policy layer. Inizia solo con luci e plug non critiche allowlisted. Implementa dry-run, idempotenza, verifica post-azione e audit. Climate, network, NAS, lock, alarm, webcam e automazioni rimangono negati o richiedono conferma esplicita. Testare prima su HA test.
```

---

## FASE 4 — Collector e history

### Obiettivo

Evolvere `domotics_agent.py` in un collector affidabile.

### Attività

- error logging al posto di `pass`;
- handshake/ack WebSocket;
- reconnect/backoff;
- mapping configurabile;
- stato persistente atomico;
- aggregazione eventi rumorosi;
- retention;
- export Recorder/statistics attraverso interfacce supportate;
- dataset sanitizzati.

### Prompt Fase 4

```text
Agisci come data engineer esperto di Home Assistant Recorder e WebSocket API. Mantieni il comportamento esistente di domotics_agent.py e proponi una migrazione incrementale. Aggiungi acknowledgement, reconnect con backoff, logging, mapping configurabile, persistenza atomica, aggregazione e retention. Preferisci API e statistiche supportate rispetto all'accesso diretto al DB production. Crea dataset sanitizzati per la 3090 e test con eventi simulati.
```

---

## FASE 5 — HA Analyst sulla 3090

### Modello predefinito

```text
qwen2.5-coder:14b
```

Per analisi più architetturali può essere confrontato con:

```text
qwen3:14b
```

### Input

```text
automations.yaml
scripts.yaml
sensors.yaml sanitizzati
ha_snapshot.json
ha_event_samples.jsonl
ha_statistics_daily.json
request_log.jsonl
```

### Output

```text
analysis_report.md
candidate_automation.yaml
candidate_tests.yaml
risk_assessment.md
```

L'analyst non modifica production.

### Prompt Fase 5

```text
Agisci come Home Assistant architect e code reviewer. Analizza solo i file forniti. Distingui fatti, ipotesi e raccomandazioni. Non inventare entity_id o servizi. Per ogni proposta indica origine, beneficio, rischio, test e rollback. Produci candidate separate, mai patch production automatiche. Considera MQTT, mDNS, VLAN, UniFi, Recorder e dispositivi fisici. Ordina le proposte per sicurezza, affidabilità e valore.
```

---

## FASE 6 — Linear, Git e GitHub in dry-run

### Obiettivo

Sostituire il manager accoppiato con tool deterministici.

### Attività

- LinearTool;
- GitTool;
- GitHubTool;
- risultati strutturati;
- idempotenza;
- repository lock;
- branch naming configurabile;
- nessuna PR senza patch, test e commit;
- nessun cambio stato ticket implicito.

### Prompt Fase 6

```text
Agisci come senior Git, GitHub e Linear automation engineer. Separa LinearTool, GitTool e GitHubTool senza cambiare production finché i test non passano. Ogni operazione deve essere strutturata, idempotente e supportare dry-run. Non usare subprocess Python-per-Python, non parsare output umano, non creare PR senza commit e non cambiare stato Linear senza policy esplicita. Usa repository temporanei e API mock nei test.
```

---

## FASE 7 — Dispatcher 1070 verso 3090

### Obiettivo

Spostare solo job pesanti sulla 3090.

### Requisiti

- 1070 indipendente dalla disponibilità 3090;
- job autenticati;
- request/correlation ID;
- payload sanitizzati;
- queue/status;
- timeout/cancel;
- retry limitato;
- artefatti hashati/versionati;
- promozione manuale.

### Prompt Fase 7

```text
Agisci come distributed systems engineer. Progetta un dispatcher semplice e autenticato tra 1070 e 3090. La 1070 deve continuare a funzionare quando la 3090 è offline. Usa job idempotenti con correlation ID, stato, timeout, cancel, retry limitato e output versionato. Non esporre Ollama direttamente fra subnet senza controllo. Non introdurre un message broker finché una coda file o API minima non è insufficiente.
```

---

## FASE 8 — UniFi read-only

### Obiettivo

Osservabilità di rete senza modifiche automatiche.

### Funzioni

- inventory AP/switch/client;
- availability;
- mapping host/VLAN;
- device sconosciuti;
- reachability nodi;
- correlazione esplicita con entità HA;
- report flussi.

### Prompt Fase 8

```text
Agisci come UniFi observability engineer. Implementa solo lettura. Inventaria gateway, Network Application, VLAN, subnet, client e dipendenze. Non modificare firewall, VPN, VLAN, SSID, PPSK, DNS o routing. Produrre una matrice dei flussi necessari; ogni cambiamento di rete resta una proposta con impatto, test e rollback.
```

---

## FASE 9 — MCP, knowledge e altri canali

MCP arriva soltanto dopo tool, policy, test e audit stabili.

Canali futuri:

```text
HA Assist/App
Telegram
Open WebUI
mail agent
file organisation agent
```

Tutti usano lo stesso policy layer.

### Prompt Fase 9

```text
Agisci come MCP e agent-platform architect. Inventaria i tool esistenti prima di proporre MCP. Esponi solo tool limitati con schema, autenticazione, autorizzazione e risk level. Non esporre shell generica, filesystem illimitato o API amministrative. Mantieni il medesimo policy layer per Telegram, Assist e WebUI. Proponi una migrazione incrementale e reversibile.
```

---

# 12. Configurazione 3090 raccomandata

## Software

```text
Ollama
VS Code
Git
Docker/Dev Containers
estensione coding-agent compatibile con endpoint Ollama
```

## Modello default

```bash
ollama pull qwen2.5-coder:14b
```

## Modello generalista opzionale

```bash
ollama pull qwen3:14b
```

## Modello di compatibilità 1070

```bash
ollama pull qwen2.5-coder:7b
```

## Impostazioni iniziali prudenti

Queste sono impostazioni da misurare, non limiti ufficiali:

```text
modello attivo: uno
context: 8192 iniziale
context successivo: 16384 se stabile
parallel heavy jobs: 1
coding temperature: 0.1–0.2
design temperature: 0.2–0.4
keep-alive: limitato durante sviluppo
```

Non partire da 32K/40K soltanto perché il modello li supporta.

## Monitoraggio

```bash
nvidia-smi
```

Osservare:

- memoria GPU usata;
- utilità GPU;
- temperatura;
- power draw;
- processi GPU;
- RAM/swap;
- latency;
- errori OOM.

Il raffreddamento ad aria non è un problema architetturale di per sé, ma carichi prolungati devono essere monitorati. L'agente non deve modificare overclock, voltaggi o power limit.

---

# 13. Primo prompt per il nuovo agente

Modello consigliato: **qwen2.5-coder:14b locale via Ollama**.

```text
You are the lead engineer for ZEUS, a personal local-AI, Home Assistant and home-network platform.

Read ZEUS_SAFE_HEADROOM_ARCHITECTURE.md in full before doing anything. Then inspect the repository in read-only mode. Do not modify files yet.

Hardware and roles:
- ZEUS EDGE / production: Ubuntu laptop, GTX 1070 Max-Q 8 GB, 32 GB RAM. It runs Ollama, Open WebUI, Telegram, Wyoming Whisper, Wyoming Piper and Glances.
- ZEUS LAB / development: AMD Ryzen 9 5950X, RTX 3090 24 GB, 64 GB RAM.
- Preferred default local development model: qwen2.5-coder:14b via Ollama.
- Optional architecture comparison model: qwen3:14b.
- Home Assistant production: Raspberry Pi 4.
- Storage/backup: QNAP TS-251+.
- Network: UniFi, with VPN and possible future VLAN/subnet separation.

Architecture rules:
1. The 1070 is production and must remain stable.
2. The 3090 is lab, testing, analysis and on-demand heavy compute.
3. Home Assistant is the authoritative controller of the house.
4. Telegram, Assist and WebUI are channels, not agents.
5. Whisper and Piper are STT/TTS services, not agents.
6. Ollama is a model runtime, not the orchestration layer.
7. LLMs interpret requests; deterministic tools execute; policies authorise or deny.
8. Phase 1 starts entirely in OBSERVE mode.
9. Do not execute Home Assistant, Linear, Git, GitHub or UniFi changes.
10. Never expose, print, copy or commit secrets.
11. Do not introduce OpenClaw, LangGraph, CrewAI, AutoGen, n8n, Qdrant, PostgreSQL or MCP in Phase 1.
12. Do not rename or move existing files unless required by an accepted failing requirement.
13. Show diffs before applying changes.
14. Every proposed change must include purpose, affected files, risk, tests, expected result and rollback.
15. Prefer small commits and preserve backward compatibility.

Current mission:
Complete Phase 0 and prepare Phase 1 only.

First task:
A. Read and audit the complete repository without editing it.
B. Inspect at minimum: telegram_agent.py, domotics_agent.py, git_flow_manager.py, core_lib/linear_api.py, docker-compose.yml, systemd units, inventory files and .gitignore.
C. Identify syntax errors, malformed strings, dead branches, blocking I/O in async handlers, unsafe execution paths, hard-coded paths, missing timeouts, swallowed exceptions, secret risks and missing tests.
D. Compare the current code to the architecture document.
E. Propose the smallest ordered commit sequence for Phase 0 and Phase 1.
F. Do not generate code yet.
G. Finish with only the first proposed commit, its acceptance criteria, exact files needed and validation commands.

System improvement loop:
Observe -> Normalise -> Analyse -> Propose -> Test -> Approve -> Deploy -> Measure.
```

---

# 14. Prompt dopo l'audit

```text
Proceed with the first approved commit only.

Constraints:
- Keep telegram_agent.py as the entrypoint.
- Preserve Telegram reception and ALLOWED_CHAT_ID.
- Use existing core_lib.secrets variable names without showing values.
- Remove malformed HTML from the Ollama URL.
- Do not block the Telegram async event loop.
- Validate and normalise the model JSON.
- Fall back safely to UNKNOWN.
- Add append-only JSONL with request_id and schema_version.
- Set every category to OBSERVE.
- Do not call git_flow_manager, Linear, GitHub, Git, UniFi or Home Assistant.
- Add mocked unit tests.
- Do not alter Docker Compose in this commit.

Show the exact patch and tests before applying. After applying, run only relevant tests. If a test fails, make the smallest correction and do not broaden scope.
```

---

# 15. Decision log

```text
ADR-001: 1070 is ZEUS EDGE production.
ADR-002: 3090 is ZEUS LAB and heavy compute on demand.
ADR-003: qwen2.5-coder:14b is the default 3090 model.
ADR-004: qwen3:14b is an optional architecture/generalist model.
ADR-005: 30B models are optional benchmarks, not defaults.
ADR-006: Raspberry HA remains authoritative.
ADR-007: Phase 1 is OBSERVE only.
ADR-008: Tools and policies are separate from routing.
ADR-009: HA test is isolated from physical production devices.
ADR-010: UniFi starts read-only.
ADR-011: 3090 proposes/tests; human approves promotion.
ADR-012: one canonical inventory file.
ADR-013: no multi-agent framework until simple Python is insufficient.
ADR-014: MCP is a later interoperability layer.
```

---

# 16. Definition of Done

Ogni fase richiede:

- requisiti documentati;
- test automatici pertinenti;
- test manuale controllato;
- nessun secret nei log/repository;
- rollback;
- osservabilità;
- risk level e permessi;
- artefatto versionato;
- 1070 indipendente dalla 3090;
- nessuna modifica non approvata a casa o rete.

---

# 17. Sintesi

```text
Non saturare la 3090 per principio.
Usare 14B come default dà margine a context, runtime e strumenti.
Usare un solo modello attivo alla volta.
Tenere 30B come profilo heavy da benchmark, non come fondazione.

Raspberry controlla la casa.
1070 esegue Zeus H24.
3090 sviluppa, testa e analizza.
QNAP conserva dati e artefatti.
UniFi separa e protegge i flussi.
```
