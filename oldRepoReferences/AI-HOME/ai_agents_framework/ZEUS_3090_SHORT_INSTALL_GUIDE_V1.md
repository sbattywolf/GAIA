# ZEUS 3090 — Short Installation Guide

## Decisione

Installare ora soltanto la toolchain necessaria per Fase 0 e Fase 1:

- aggiornamenti Ubuntu;
- strumenti terminale e sviluppo;
- driver NVIDIA, solo se mancanti;
- Git;
- Python, virtual environment e test tool;
- VS Code;
- Ollama nativo;
- `qwen2.5-coder:14b`;
- workspace ZEUS.

Rimandare alla Fase 2:

- Docker Engine;
- Docker Compose;
- Dev Containers;
- Home Assistant test.

Rimandare alle fasi successive:

- `qwen3:14b`;
- modelli 30B;
- Continue;
- GitHub Copilot;
- OpenCode;
- Open WebUI sulla 3090;
- NVIDIA Container Toolkit;
- PostgreSQL;
- Qdrant;
- MCP;
- n8n;
- OpenClaw;
- LangGraph/CrewAI/AutoGen.

## Come usare il documento comandi

1. Eseguire le sezioni `00`–`18` in ordine.
2. Alla sezione `03`, se `nvidia-smi` funziona, saltare la sezione `04`.
3. Dopo la sezione `04`, completare il riavvio prima di eseguire `05`.
4. Nella sezione `13`, sostituire `REPLACE_WITH_REPOSITORY_URL`.
5. Nella sezione `16`, sostituire `REPLACE_WITH_EMAIL`.
6. Non eseguire ancora le sezioni marcate `DEFERRED`.
7. Non installare contemporaneamente Ollama nativo e Ollama Docker.
8. Non copiare `core_lib/secrets.py` con credenziali reali nel workspace controllato dall'agente.
9. Non aggiungere al repository `.env`, database, log, backup o token.
10. Installare in VS Code una sola integrazione AI per volta.

## VS Code e Ollama

Dopo la sezione `10`:

1. Aprire VS Code.
2. Disabilitare Continue, GitHub Copilot, Cline, Roo Code e altre estensioni AI.
3. Installare l'estensione Ollama indicata dalla documentazione Ollama per VS Code.
4. Aprire Chat.
5. Selezionare `qwen2.5-coder:14b` nella sezione Ollama.
6. Eseguire il test:

```text
Reply only with: ZEUS VSCODE LOCAL OK
```

7. Verificare contemporaneamente la GPU:

```bash
watch -n 2 nvidia-smi
```

## Python

Il documento installa globalmente soltanto tool CLI isolati tramite `pipx`.

Le dipendenze del progetto vengono installate dentro:

```text
.venv
```

Prima di lavorare nel progetto:

```bash
cd ~/github_repos/ai_agents_framework
source .venv/bin/activate
```

Dopo il lavoro:

```bash
deactivate
```

Non installare librerie applicative con `sudo pip` o nel Python globale.

## Git

Creare il branch:

```text
feature/zeus-phase-0-1
```

Prima di iniziare con l'agente:

```bash
git status
git branch --show-current
```

Il primo prompt deve produrre soltanto un audit read-only. Non deve modificare file.

## Docker

Non serve per il primo audit o per stabilizzare `telegram_agent.py` con test mockati.

Installarlo quando si avvia la Fase 2 perché servirà per:

- Home Assistant test isolato;
- fixture e servizi simulati;
- Dev Containers;
- integration test.

Ollama resterà nativo anche dopo l'installazione di Docker.

## Gate prima di usare il prompt ZEUS

Verificare:

```text
[ ] RTX 3090 visibile con nvidia-smi
[ ] Ollama attivo come servizio
[ ] Un solo listener su 127.0.0.1:11434
[ ] qwen2.5-coder:14b installato
[ ] Inferenza eseguita sulla GPU
[ ] VS Code avviato
[ ] Estensione Ollama collegata
[ ] Repository presente
[ ] Branch feature/zeus-phase-0-1 attivo
[ ] .venv creato
[ ] pytest disponibile
[ ] secrets reali esclusi
[ ] documenti ZEUS nella root
```

## Primo lavoro

Aprire il repository in VS Code:

```bash
cd ~/github_repos/ai_agents_framework
code .
```

Selezionare `qwen2.5-coder:14b` e inviare il prompt iniziale di audit contenuto in `ZEUS_SAFE_HEADROOM_ARCHITECTURE_V3.md`.

## Fonti ufficiali utilizzate

- Ubuntu NVIDIA drivers: https://ubuntu.com/server/docs/how-to/graphics/install-nvidia-drivers/
- VS Code Linux: https://code.visualstudio.com/docs/setup/linux
- Ollama Linux: https://docs.ollama.com/linux
- Ollama VS Code: https://docs.ollama.com/integrations/vscode
- Docker Engine Ubuntu: https://docs.docker.com/engine/install/ubuntu/
