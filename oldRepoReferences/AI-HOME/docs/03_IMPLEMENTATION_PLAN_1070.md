# Piano di implementazione 1070

## Milestone 0: baseline

- Tag o commit pulito.
- Test service, Telegram, Ollama e HA.
- Nessuna modifica simultanea a Home Assistant e codice.

## Milestone 1: qualità del fast path

- `ResponseFormatter` con vocaboli per capability.
- Correzione refusi comuni: accesse/accesa, spengo/spegni.
- Test per stato assente, `unknown`, `unavailable`.
- Nessun dump oltre una soglia configurabile.

## Milestone 2: query aggregate

Supportare senza LLM:

- quante finestre/porte/luci/switch
- quante automazioni abilitate/disabilitate
- luci accese/spente
- report casa

Un report deve essere un piano composto, non una singola `EntityQuery`.

## Milestone 3: inventory provider

- mantenere REST `/api/states` per runtime
- aggiungere client WebSocket read-only
- leggere area, device ed entity registry
- aggiungere label registry se supportato dalla versione HA
- join deterministico
- cache con TTL e invalidazione manuale

## Milestone 4: capability resolver

Sostituire `device_kind=light` con `capability=lighting`.

Risoluzione:

1. area
2. capability label
3. policy label
4. target canonico
5. domain/service reale

## Milestone 5: context state

Conservare solo:

- last_intent_type
- last_capability
- last_area
- last_target_ids
- last_requested_state
- timestamp

Non passare tutta la cronologia al modello.

## Milestone 6: azioni

- lettura prima dell'azione quando utile
- service call
- verifica stato post-azione
- risposta basata sul risultato
- confirmation gate per ambiguità/rischio

## Milestone 7: osservabilità

Aggiungere al log:

- route: deterministic/llm/ha_conversation/backlog
- overall_latency_ms
- llm_latency_ms
- ha_latency_ms
- cache_hit
- matched_entity_count
- intent confidence
- error code strutturato

## Definition of done

- test automatici verdi
- test Telegram documentati
- nessun segreto in Git
- commit piccolo
- rollback documentato
- latenza misurata
