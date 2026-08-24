# Architettura futura 3090, MCP e Open WebUI

## Zeus Brain

La 3090 viene avviata on-demand e riceve task pesanti dal backlog. Non deve essere necessaria per comandi domestici realtime.

## Use case

- coding generale
- generazione patch con test
- analisi automazioni e trace HA
- generazione dashboard Lovelace
- proposta di script/scene/helper
- revisione naming/label
- documentazione

## Guardrail Home Assistant

1. Accesso read-only di default.
2. Export/backup prima di ogni proposta.
3. Modifiche su file/branch separati.
4. Diff umanamente leggibile.
5. Dry-run o ambiente di test quando disponibile.
6. Nessun riavvio/reload automatico senza approvazione.
7. Rollback esplicito.

## MCP

Percorso raccomandato:

- fase A: valutare il MCP Server ufficiale HA per Assist e snapshot delle entità esposte
- fase B: valutare community ha-mcp separatamente per capability amministrative, con permessi e rischio maggiori
- fase C: aggiungere MCP a Open WebUI o a un client dedicato

Non confondere il server MCP ufficiale, limitato all'Assist API e alle entità esposte, con strumenti community che dichiarano funzioni amministrative più ampie.

## Open WebUI

- nodo 3090
- `WEBUI_SECRET_KEY` persistente
- accesso LAN protetto
- tool admin-only
- preferire Streamable HTTP per MCP nativo nelle versioni che lo supportano
- usare MCPO solo quando occorre convertire server stdio/OpenAPI

## GitHub Copilot in IntelliJ

Il repository include:

- `.github/copilot-instructions.md`
- `.github/agents/zeus-architect.agent.md`
- `.github/prompts/implement-1070-feature.prompt.md`
- `.github/prompts/review-home-assistant-change.prompt.md`

Il modello scelto non cambia le regole: piccoli diff, test, niente segreti, niente modifiche live non approvate.
