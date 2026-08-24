# Matrice test e accettazione

## Query aperture

- quali finestre sono aperte?
- ci sono finestre chiuse?
- quali porte sono aperte?
- quali sono le porte chiuse?
- e quelle chiuse?

Atteso: grammatica corretta, nessun sensore non pertinente, follow-up mantiene capability.

## Query illuminazione

- quali luci sono accese adesso?
- ci sono luci accese?
- ci sono luci accesse?  # refuso intenzionale
- stato luci ufficio
- stato luci camera da letto

Atteso: target canonici, niente LED/RGB tecnici, niente `unavailable` salvo richiesta esplicita.

## Conteggi

- quante automazioni ci sono?
- quante automazioni sono abilitate?
- quante sono disabilitate?
- quante finestre e quante porte ho?

Atteso: conteggi distinti, nessun backlog per query supportata.

## Report

- fammi un report dello stato della casa

Atteso minimo:

- aperture aperte
- luci utente accese
- entità principali unavailable
- automazioni disabilitate, se disponibile

## Azioni

- spegni luce ufficio
- accendi luce camera da letto soffitto
- spegni tutto

Atteso: resolver capability; domanda di chiarimento per "tutto"; verifica post-azione.
