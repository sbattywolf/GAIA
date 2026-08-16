# Stato corrente e risultati dei test

## Inventario runtime osservato

- automation: 35
- binary_sensor: 45
- camera: 5
- climate: 9
- light: 48
- scene: 24
- sensor: 792
- switch: 110
- vacuum: 1

Questi conteggi sono uno snapshot condiviso dall'utente e possono cambiare.

## Aperture osservate

### Porte

- `binary_sensor.sensore_porta_wc_opening`, class `door`
- `binary_sensor.sensore_porta_ingresso_opening`, class `door`
- `binary_sensor.sensore_porta_sgabuzzino_contact`, class `door`
- `binary_sensor.sensore_porta_ripostiglio_contact`, class `door`

Nello snapshot erano tutte `off`, quindi nessuna porta aperta.

### Finestre

Sei entità classificate `window`; nello snapshot tre `on` e tre `off`.

## Illuminazione

### Controlli wall switch rilevanti

- `switch.wall_switch_ufficio_switch`
- `switch.wall_switch_corridoio_switch`
- `switch.wall_switch_ingresso_switch`
- `switch.wall_switch_camera_letto_switch`
- `switch.wall_switch_spot_1_switch`
- `switch.wall_switch_spot_2_switch`
- `switch.switch_cucina_light_switch`

### Entità `light` rilevanti

- gruppi lights spots/open/tetto corridoio/ufficio
- `light.spot_1`, `light.spot_2`
- `light.luce_tetto_corridoio_light`
- `light.luce_tetto_ingresso`
- `light.luce_tetto_ufficio_light`
- `light.desk_light_ufficio_light`

### Rumore da escludere dalle query generiche

- LED indicator/status
- segmenti RGBIC TV Backlight
- RGB GPU e motherboard
- entità `unavailable`
- switch Adaptive Lighting di configurazione
- power outage memory, indicator light, child lock

Non eliminare queste entità. Classificarle come non appartenenti alla capability generica `lighting_control`.

## Aree esistenti

Bagno, Camera da letto, Corridoio, Cucina, Ingresso, Office, Ripostiglio, Sgabuzzino, Soggiorno, Ufficio, WC.

Nota: `Office` e `Ufficio` possono essere intenzionalmente distinti oppure una duplicazione semantica. Non unificarli automaticamente. Verificare contenuto e uso.

## Bug e gap confermati

1. Formatter "aperte/accesi" e "chiuse/spenti" non è semanticamente corretto.
2. Query senza stato restituisce dump completo.
3. "Ci sono luci accese?" con refuso può non estrarre lo stato.
4. Query multi-intento viene ridotta a un solo tipo di entità.
5. Report casa non ha un piano di aggregazione.
6. Automazioni contate nel runtime non sono ancora supportate come capability.
7. Indicatore LED viene trattato come luce utente.
8. Area non è estratta dal parser deterministico.
9. Follow-up dipende ancora da stringhe e merge di query tecniche.
