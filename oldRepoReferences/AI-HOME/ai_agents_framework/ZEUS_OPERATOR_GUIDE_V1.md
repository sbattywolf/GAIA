# ZEUS — Guida Operativa Personale
## Cosa fare, quale modello usare, cosa attivare e su quale macchina

**Versione:** 1.0  
**Data:** 27 luglio 2026  
**Destinatario:** Carlo  
**Documento collegato:** `ZEUS_SAFE_HEADROOM_ARCHITECTURE_V3.md`

---

# 1. Scopo di questa guida

Questo documento non descrive principalmente l'architettura: descrive **cosa devi fare tu**, in quale ordine, quale modello scegliere, quale prompt usare, dove eseguire ogni attività e quando fermarti.

Regola fondamentale:

```text
Non passare alla fase successiva solamente perché il modello propone di farlo.
Passa alla fase successiva solo quando il gate di uscita della fase corrente è soddisfatto.
```

---

# 2. Mappa rapida delle macchine

## Raspberry Pi 4

```text
Ruolo: Home Assistant production
Da usare per: casa reale, integrazioni, automazioni, sensori e attuatori
Da non usare per: sviluppo LLM pesante o test rischiosi
```

## MSI GTX 1070 / Ubuntu

```text
Nome logico: ZEUS EDGE
Ruolo: production H24
Modello: qwen2.5-coder:7b
Da usare per:
- Telegram production
- Zeus router/runtime
- richieste Home Assistant rapide
- Whisper e Piper
- logging
- dispatch futuro verso 3090
```

## Desktop RTX 3090 / Ryzen 5950X / 64 GB

```text
Nome logico: ZEUS LAB
Ruolo: sviluppo, test e analisi
Modello principale: qwen2.5-coder:14b
Modello opzionale: qwen3:14b
Da usare per:
- audit repository
- sviluppo Python
- test
- Home Assistant test
- analisi automazioni/history
- preparazione release per 1070
```

## QNAP

```text
Nome logico: ZEUS STORAGE
Ruolo: storage e backup
Da usare per:
- backup
- snapshot
- dataset sanitizzati
- report
- artefatti di release
```

---

# 3. Modelli: quale usare e quando

## Modello quotidiano sulla 3090

```text
qwen2.5-coder:14b
```

Usalo quando devi:

- leggere e modificare il repository;
- correggere Python;
- creare test;
- lavorare su Docker Compose;
- analizzare Home Assistant YAML;
- creare patch;
- progettare LinearTool, GitTool e GitHubTool;
- preparare una release per la 1070.

Comando di installazione:

```bash
ollama pull qwen2.5-coder:14b
```

## Modello generalista opzionale sulla 3090

```text
qwen3:14b
```

Usalo come secondo parere quando devi:

- rivalutare l'architettura;
- analizzare categorie e routing;
- ragionare su Home Assistant + UniFi;
- rivedere prompt e policy;
- verificare se il coder ha trascurato aspetti non strettamente software.

Comando:

```bash
ollama pull qwen3:14b
```

Non è necessario usarlo durante la prima esecuzione. Non tenere due modelli caricati contemporaneamente se non serve.

## Modello production sulla 1070

```text
qwen2.5-coder:7b
```

Usalo per:

- classificazione dei messaggi Telegram;
- output JSON strutturato;
- Zeus runtime;
- risposte brevi;
- operazioni Home Assistant future e controllate.

## Modelli heavy

```text
qwen3-coder:30b
Devstral Small 2
```

Per ora non usarli. Valutali soltanto quando:

- il 14B fallisce su casi misurabili;
- hai un benchmark ripetibile;
- esegui un solo job;
- monitori VRAM e temperatura;
- non hai altri workload GPU importanti.

---

# 4. Impostazioni iniziali della 3090

Usa un solo modello attivo.

Impostazioni iniziali consigliate da provare:

```text
Modello: qwen2.5-coder:14b
Context: 8192
Temperature coding: 0.1–0.2
Job pesanti paralleli: 1
Keep-alive: limitato durante sviluppo
```

Se tutto è stabile e il repository richiede più contesto:

```text
Context successivo: 16384
```

Non iniziare subito da 32K.

Monitoraggio:

```bash
watch -n 2 nvidia-smi
```

Controlla:

- VRAM;
- temperatura GPU;
- utilizzo GPU;
- power draw;
- processi caricati;
- eventuali errori out-of-memory;
- RAM e swap del sistema.

---

# 5. Strumenti da usare sulla 3090

Installa o prepara:

```text
Ollama
VS Code
Git
Docker Desktop oppure Docker su Ubuntu
Dev Containers
un'estensione coding-agent compatibile con Ollama
```

Regole iniziali dell'agente:

```text
- niente approve-all;
- niente shell illimitata;
- mostrare sempre il diff;
- lavorare su branch dedicato;
- non leggere secrets.py se contiene valori reali;
- non includere database, backup o token nel contesto;
- eseguire test prima del commit;
- non fare deploy autonomo sulla 1070.
```

---

# 6. Preparazione iniziale

## Sulla 3090

1. Crea una directory di lavoro.
2. Clona o copia il repository.
3. Metti nella root:

```text
ZEUS_SAFE_HEADROOM_ARCHITECTURE_V3.md
ZEUS_OPERATOR_GUIDE_V1.md
```

4. Verifica che i segreti reali non siano presenti.
5. Crea un branch dedicato:

```bash
git checkout -b feature/zeus-phase-0-1
```

6. Avvia Ollama.
7. Seleziona `qwen2.5-coder:14b` nel coding agent.
8. Incolla il prompt iniziale presente nel documento architetturale V3.

## Cosa devi aspettarti

Il primo output deve essere soltanto:

```text
- comprensione repository;
- problemi confermati;
- assunzioni da verificare;
- confronto con architettura V3;
- sequenza minima di commit;
- proposta del primo commit.
```

Non deve scrivere codice.

---

# 7. Workflow standard con l'agente AI

Per ogni commit usa questo ciclo:

```text
1. AUDIT
2. PROPOSTA
3. DIFF
4. TUA APPROVAZIONE
5. APPLICAZIONE
6. TEST
7. REVIEW
8. COMMIT
9. EVENTUALE RELEASE
10. DEPLOY MANUALE
```

## Cosa dire dopo l'audit

Se il primo commit proposto è corretto, usa:

```text
Proceed with the first approved commit only.
Do not apply any patch yet.
Show the exact diff, tests, expected results, risks and rollback.
Do not broaden the scope.
```

## Cosa dire dopo aver letto il diff

Se il diff è corretto:

```text
Apply only the displayed patch.
Then run only the listed tests.
Do not change any additional file.
If a test fails, diagnose it and propose the smallest correction before applying it.
```

## Cosa dire dopo test verdi

```text
Summarise the implemented behaviour, test results and remaining risks.
Suggest one commit message.
Do not start the next commit.
```

---

# 8. Fase 0 — Cosa fai tu

## Dove

```text
RTX 3090 / ZEUS LAB
```

## Modello

```text
qwen2.5-coder:14b
```

## Cosa triggerare

Triggera:

```text
- audit read-only;
- controllo .gitignore;
- controllo secrets;
- validazione Docker Compose;
- validazione systemd;
- inventario path e porte;
- strategia backup e rollback;
- analisi dei due inventory.json.
```

Non triggerare:

```text
- refactoring;
- deploy;
- Home Assistant reale;
- Linear;
- GitHub PR;
- UniFi;
- migrazione directory.
```

## Cosa controlli personalmente

- Il repository non contiene valori segreti.
- Il branch è corretto.
- Esiste un backup Home Assistant.
- Sai ripristinare il bot precedente.
- L'agente distingue fatti e ipotesi.
- Nessun file production è stato modificato.

## Quando puoi uscire dalla Fase 0

```text
- backup e rollback documentati;
- working tree noto;
- secrets esclusi;
- compose e systemd verificati;
- primo commit Phase 1 definito.
```

---

# 9. Fase 1 — Zeus OBSERVE

## Dove sviluppi

```text
RTX 3090
```

## Dove esegui production dopo i test

```text
GTX 1070
```

## Modelli

```text
Sviluppo: qwen2.5-coder:14b
Runtime: qwen2.5-coder:7b
```

## Cosa triggerare sulla 3090

```text
- audit completo di telegram_agent.py;
- correzione degli errori sintattici;
- chiamata Ollama non bloccante;
- validazione JSON;
- fallback UNKNOWN;
- request_id;
- log JSONL append-only;
- categorie HOME/CODING/LINEAR/GITHUB/SCRUM/SYSTEM/NETWORK/UNKNOWN;
- test mockati Telegram/Ollama;
- modalità OBSERVE per tutto.
```

## Cosa non triggerare

```text
- accensione luci;
- lettura Home Assistant reale;
- creazione ticket;
- branch Git;
- PR GitHub;
- comandi UniFi;
- modifica Docker Compose, salvo bug indispensabile e separato.
```

## Test da eseguire in lab

```text
/start
ciao
accendi la luce ufficio
quali finestre sono aperte?
prendi in carico SBA-123
apri branch per SBA-123
analizza automations.yaml
stato Ollama
stato rete
messaggio ambiguo
Ollama offline
JSON Ollama invalido
chat ID non autorizzato
```

## Risultato corretto

Tutto viene classificato e registrato. Nulla viene eseguito.

## Deploy manuale sulla 1070

Prima:

```bash
sudo systemctl status ha-telegram-agent
```

Dopo aver salvato la versione precedente:

```bash
sudo systemctl restart ha-telegram-agent
sudo systemctl status ha-telegram-agent
journalctl -u ha-telegram-agent -n 100 --no-pager
```

## Quando puoi uscire dalla Fase 1

```text
- Telegram risponde stabilmente;
- Ollama offline non blocca il bot;
- JSON invalido usa UNKNOWN;
- log completi senza secrets;
- nessuna azione reale;
- rollback provato o chiaramente eseguibile.
```

---

# 10. Periodo operativo OBSERVE

Usa Zeus normalmente da Telegram.

Cosa triggerare:

```text
- vere richieste quotidiane;
- domande domotiche;
- richieste Linear;
- richieste Git;
- richieste coding;
- richieste di rete;
- richieste ambigue.
```

Scopo:

- raccogliere distribuzione reale delle categorie;
- capire gli action type ricorrenti;
- identificare misclassificazioni;
- capire quali tool servono per primi;
- verificare se il 7B è sufficiente.

Non correggere manualmente i log. Aggiungi in futuro un feedback log separato.

Esempio feedback:

```json
{
  "request_id": "...",
  "predicted_category": "HOME",
  "correct_category": "LINEAR",
  "reviewed_by": "human",
  "notes": "ticket related request"
}
```

---

# 11. Fase 2 — Home Assistant read-only

## Dove sviluppi

```text
RTX 3090 + Home Assistant test
```

## Dove esegui production

```text
GTX 1070 che interroga Raspberry HA
```

## Modello

```text
qwen2.5-coder:14b per sviluppo
qwen2.5-coder:7b per runtime
```

## Cosa triggerare

```text
- HomeAssistantReadTool;
- snapshot sanitizzato;
- entity mapping;
- query read-only;
- test con fixture;
- HA test container;
- gestione timeout e token.
```

Prime richieste abilitate:

```text
Quali finestre sono aperte?
Quali luci sono accese?
C'è movimento in bagno?
Che temperatura c'è in camera?
Quali plug sono attive?
Quali entità UniFi sono unavailable?
```

## Cosa non triggerare

```text
- service call;
- turn_on/turn_off;
- climate setpoint;
- restart;
- automazioni;
- rete.
```

## Gate

Le risposte provengono da dati reali del tool e non vengono inventate dal modello.

---

# 12. Fase 3 — Azioni HOME allowlisted

## Dove sviluppi

```text
RTX 3090 + HA test
```

## Dove esegui production

```text
GTX 1070 -> Raspberry HA
```

## Cosa triggerare per primo

Solo azioni R1:

```text
- accendi luce allowlisted;
- spegni luce allowlisted;
- luminosità;
- plug non critica allowlisted.
```

## Cosa richiede conferma

```text
- climate;
- automazioni;
- riavvio device;
- plug importanti.
```

## Cosa resta vietato

```text
- lock;
- allarme;
- firewall/VLAN/VPN;
- spegnimento NAS/host;
- webcam sensibile;
- merge/deploy;
- modifica automatica automazioni production.
```

## Gate

```text
- policy allowlist;
- dry-run;
- idempotenza;
- verifica stato finale;
- audit;
- test HA test superati.
```

---

# 13. Fase 4 — Collector/history

## Dove

```text
Sviluppo 3090
Runtime 1070/Raspberry APIs
Storage QNAP
```

## Modello

```text
qwen2.5-coder:14b
```

## Cosa triggerare

```text
- miglioramento incrementale domotics_agent.py;
- reconnect WebSocket;
- logging errori;
- mapping configurabile;
- persistenza atomica;
- aggregazione eventi;
- retention;
- export statistics;
- dataset sanitizzati.
```

## Non triggerare

```text
- accesso diretto al DB production senza necessità;
- invio di history grezza enorme al modello;
- modifica automatica automazioni.
```

---

# 14. Fase 5 — HA Analyst

## Dove

```text
RTX 3090
```

## Modello predefinito

```text
qwen2.5-coder:14b
```

## Quando usare qwen3:14b

Usalo come review opzionale per:

```text
- architettura;
- interpretazione pattern;
- policy;
- priorità delle proposte;
- impatti Home Assistant + UniFi.
```

## Cosa triggerare

```text
- analisi automations.yaml;
- analisi scripts/sensors sanitizzati;
- analisi snapshot;
- analisi eventi aggregati;
- analisi statistiche;
- analisi request_log e feedback_log;
- candidate automation;
- test candidate;
- risk assessment.
```

## Output attesi

```text
analysis_report.md
candidate_automation.yaml
candidate_tests.yaml
risk_assessment.md
```

## Non triggerare

```text
- modifica diretta production;
- deploy automatico;
- entity_id inventati;
- automazioni senza test e rollback.
```

---

# 15. Fase 6 — Linear/Git/GitHub

## Dove sviluppi

```text
RTX 3090
```

## Modello

```text
qwen2.5-coder:14b
```

## Ordine dei trigger

```text
1. read-only Linear
2. Linear dry-run
3. Git su repository temporaneo
4. GitHub mock/dry-run
5. workflow integrato dry-run
6. azioni reali solo con conferma
```

Non permettere:

```text
- PR senza commit;
- cambio ticket implicito;
- merge automatico;
- parsing di output umano;
- Python chiamato via subprocess da Python;
- azioni non idempotenti.
```

---

# 16. Fase 7 — Dispatcher 1070 -> 3090

## Trigger locali sulla 1070

Restano sulla 1070:

```text
- domotica live;
- query read-only;
- routing;
- logging;
- risposte brevi.
```

## Trigger da assegnare alla 3090

```text
- analisi repository;
- refactoring multi-file;
- generazione test;
- history estesa;
- analisi errori Zeus;
- prompt evaluation;
- candidate automations;
- report complessi.
```

## Regola

Se la 3090 è spenta:

```text
- Zeus continua a funzionare;
- il job viene rifiutato, accodato in modo esplicito o marcato unavailable;
- nessuna richiesta Home critica dipende dalla 3090.
```

---

# 17. Fase 8 — UniFi

## Dove

```text
Analisi 3090
Runtime read-only 1070 o integrazione HA
```

## Trigger consentiti

```text
- inventory;
- status AP/switch/client;
- device sconosciuti;
- mapping host/VLAN;
- availability;
- reachability;
- report dei flussi.
```

## Trigger vietati senza progetto separato

```text
- cambia VLAN;
- modifica firewall;
- crea VPN;
- cambia SSID/PPSK;
- modifica DNS;
- modifica routing;
- riavvia gateway.
```

---

# 18. Quando valutare un modello più grande

Valuta un modello heavy soltanto se hai un caso ripetibile nel quale il 14B fallisce.

Procedura:

```text
1. salva prompt, input e risultato 14B;
2. definisci risultato atteso;
3. esegui lo stesso caso con modello heavy;
4. misura qualità, VRAM, latenza e stabilità;
5. decidi se il miglioramento giustifica il costo;
6. non cambiare il modello production 1070 per questo motivo.
```

Non scegliere un modello più grande soltanto perché entra in VRAM.

---

# 19. Checklist quotidiana

Prima di lavorare:

```text
[ ] Sono sulla 3090, non sulla production 1070?
[ ] Sono nel branch corretto?
[ ] Il working tree è noto?
[ ] I secrets sono esclusi?
[ ] Ho caricato il modello corretto?
[ ] Ho chiesto una sola modifica?
[ ] Ho vietato scope aggiuntivo?
```

Prima di approvare una patch:

```text
[ ] Ho letto il diff?
[ ] Tocca solo i file concordati?
[ ] Mantiene la compatibilità?
[ ] Non introduce secret o path personali inutili?
[ ] Ha test?
[ ] Ha rollback?
[ ] Non abilita azioni reali premature?
```

Prima del deploy 1070:

```text
[ ] Tutti i test passano sulla 3090?
[ ] Ho salvato la versione precedente?
[ ] So come riavviare il servizio?
[ ] So come leggere i log?
[ ] Il deploy non richiede la 3090 online?
[ ] Posso fare rollback immediato?
```

---

# 20. Tabella mentale: cosa triggerare dove

```text
Telegram production            -> 1070 / qwen2.5-coder:7b
Home Assistant live            -> 1070 -> Raspberry
Voce STT/TTS                    -> 1070 Whisper/Piper
Sviluppo Python                 -> 3090 / qwen2.5-coder:14b
Test Home Assistant             -> 3090 / HA test
Analisi automazioni             -> 3090 / qwen2.5-coder:14b
Review architetturale opzionale -> 3090 / qwen3:14b
Analisi history                 -> 3090, dati sanitizzati
Backup e artefatti              -> QNAP
Domotica reale                  -> Raspberry, mediata da policy
UniFi read-only                 -> 1070/3090, secondo il tool
UniFi changes                   -> mai automatiche
Linear/Git/GitHub               -> prima dry-run su 3090
Task pesante futuro             -> dispatcher 1070 -> 3090
```

---

# 21. Se non sai cosa fare

Non chiedere all'agente:

```text
Sistema tutto.
```

Usa invece:

```text
Read the current phase requirements from ZEUS_SAFE_HEADROOM_ARCHITECTURE_V3.md and ZEUS_OPERATOR_GUIDE_V1.md.
Inspect the current repository and Git status.
Tell me which single smallest action is next according to the current phase gate.
Do not modify files.
Include the reason, affected files, validation and rollback.
```

---

# 22. Regola finale

```text
La 1070 serve te ogni giorno.
La 3090 costruisce e testa ciò che andrà sulla 1070.
Il Raspberry controlla davvero la casa.
Il QNAP conserva ciò che non vuoi perdere.
UniFi protegge i flussi.
Tu resti il punto di approvazione.
```
