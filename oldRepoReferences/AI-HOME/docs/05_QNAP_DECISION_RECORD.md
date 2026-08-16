# ADR: uso del QNAP TS-251+

## Decisione corrente

Il QNAP non viene inserito nel percorso sincrono di Zeus Edge.

## Motivazione

Il fast path ha mostrato che la latenza era soprattutto architetturale. Spostare Telegram, cache o database sul NAS aggiungerebbe dipendenze di rete e operazioni senza risolvere intent, inventory e capability mapping.

## Possibili usi futuri

- backup repository
- backup Home Assistant
- retention di log e artefatti
- destinazione metriche
- archivio modelli/documenti non in uso

## Trigger per rivalutare

- i log locali superano la retention desiderata
- serve alta disponibilità per session/context
- più nodi devono condividere stato
- esiste un requisito di audit/restore

## Non consigliato

- inferenza LLM
- routing realtime
- dipendenza obbligatoria per accendere/spegnere luci
