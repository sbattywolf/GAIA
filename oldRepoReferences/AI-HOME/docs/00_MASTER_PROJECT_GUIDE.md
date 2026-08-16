# Guida completa del progetto Zeus

## 1. Obiettivo

Zeus è un agente AI locale incrementale. Il nodo 1070 gestisce richieste rapide e affidabili; il nodo 3090 svolgerà attività pesanti e modifiche assistite al software e a Home Assistant. Home Assistant resta sul Raspberry dedicato.

## 2. Stato della baseline

La baseline 1070 dispone di Telegram, Ollama, client Home Assistant, logging/backlog, routing generale e un fast path deterministico introdotto tramite `home_intents.py` e `home_resolver.py`.

Il fast path ha trasformato query come "quali finestre sono aperte?" da lente a quasi istantanee, perché evita Ollama e interroga direttamente Home Assistant.

## 3. Risultati reali da preservare

- Finestre aperte/chiuse: corrette e veloci.
- Porte aperte: nessun risultato quando tutte le quattro porte rilevate sono `off`; comportamento corretto.
- Porte chiuse: quattro entità corrette.
- "Quali luci sono accese adesso?": ha correttamente filtrato `state=on`, ma ha incluso un LED indicatore non desiderato.
- "Stato delle luci?": ha elencato tutte le 48 entità `light`, incluse luci tecniche, segmenti RGB, entità duplicate e `unavailable`; risposta tecnicamente corretta ma inutilizzabile.
- Report casa e richieste multi-intento: il parser corrente prende un solo sottoinsieme e produce risposte fuorvianti.
- Conteggio automazioni: il pre-router non riconosce sempre la richiesta come query dati; alcune richieste finiscono nel backlog.

## 4. Diagnosi

### 4.1 Il fast path funziona

La latenza non era principalmente un limite della GTX 1070. Era generata dall'uso del modello per trasformazioni semplici e deterministiche.

### 4.2 Il modello dati è ancora domain-first

`device_kind=light -> domain=light` non descrive la casa reale. I wall switch controllano molte luci tradizionali. Le eccezioni con bulbi smart includono corridoio, ingresso e due spot.

### 4.3 `/api/states` non basta per Area e Label

Gli stati runtime danno `entity_id`, stato e attributi. Per area, device, entity metadata e label serve un inventory provider che unisca runtime state e registri persistenti, usando la WebSocket API o un'astrazione ufficiale futura.

## 5. Architettura target

```text
Telegram / Open WebUI / voce
  -> Input adapter
  -> Fast pre-router deterministico
  -> Intent normalizzato
  -> Context resolver minimo
  -> Capability resolver
  -> Inventory provider HA
  -> Policy e confirmation gate
  -> Tool executor
  -> Formatter italiano
  -> Audit log

Fallback:
  richiesta ambigua -> Ollama intent extractor strutturato
  richiesta pesante -> backlog / 3090
```

## 6. Contratti principali

### Intent logico

Campi raccomandati:

- `intent_type`: state_query, count_query, action, report, inventory_query, unknown
- `capability`: lighting, openings, presence, climate, security, automation
- `area`: canonical area ID/name o null
- `requested_state`: on, off, open, closed, unavailable o null
- `action`: turn_on, turn_off, toggle o null
- `scope`: all, area, named_target, prior_context
- `requires_confirmation`
- `confidence`
- `missing_information`

### Inventory record

- entity_id
- domain
- device_id
- area_id e area_name
- labels applicate a entity/device/area, senza presupporre ereditarietà
- friendly_name
- aliases
- device_class
- state
- availability
- exposed_to_assist
- capability memberships
- control_policy

## 7. Regole di sicurezza

- Mai inventare entity ID.
- Mai confermare un'azione prima del risultato reale.
- "Spegni tutto" deve chiedere cosa si intende o usare una policy esplicita.
- Lock, alarm, siren, garage/cover e security richiedono policy dedicate.
- Le operazioni amministrative sulla configurazione HA sono escluse da Zeus Edge.
- Il nodo 3090 deve lavorare su branch, backup e diff, mai direttamente sulla configurazione live senza approvazione.

## 8. Ruolo dei nodi

### Zeus Edge 1070

- always-on
- Telegram
- routing deterministico
- controllo e lettura real-time
- cache breve dell'inventory
- piccolo modello locale per ambiguità
- log JSONL

### Zeus Brain 3090

- coding di programmi software
- analisi del repository
- generazione e revisione automazioni
- dashboard Lovelace
- analisi trace e YAML
- Open WebUI
- client MCP
- task on-demand

### QNAP

Raccomandazione: non inserirlo nel percorso sincrono. Possibili ruoli futuri:

- backup versionati del repository e configurazione HA
- retention log
- metriche Grafana/Prometheus se già gestibili sul NAS
- archivio artefatti generati dalla 3090

Redis/PostgreSQL sono opzioni, non prerequisiti. Introdurli solo quando esiste un requisito misurato.

## 9. Strategia di implementazione

1. Congelare baseline fast path.
2. Correggere formatter semantico per `window`, `door`, `light`.
3. Aggiungere query aggregate e multi-intento senza LLM.
4. Implementare inventory provider read-only.
5. Modellare `lighting` con area, label, alias e policy.
6. Introdurre test contract e regression test dai dialoghi reali.
7. Aggiungere cache e telemetria.
8. Solo dopo valutare MCP e 3090.
