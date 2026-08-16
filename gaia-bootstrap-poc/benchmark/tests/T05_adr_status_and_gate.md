Analizza esclusivamente il repository GAIA.

Questo test verifica lo stato delle decisioni architetturali ADR.

PRIMA:
leggi con `read_file`:
`gaia-bootstrap-poc/architecture/ADR_VALIDATION_MATRIX.yaml`

DOPO:
usa `search` per verificare nel repository le fonti ADR relative a:
ADR-0001
ADR-0002
ADR-0003
ADR-0004
ADR-0005
ADR-0006
ADR-0007

Non limitarti a ripetere la matrice.
Confronta la matrice con le evidenze presenti nei file ADR.

Per ciascun ADR indica:

1. STATUS:
   ACCEPTED
   PROPOSED
   DEFERRED
   CONFLICTED
   oppure
   NON DIMOSTRATO DALLE EVIDENZE DISPONIBILI.

2. FILE AUTOREVOLE, se dimostrabile.

3. GATE:
   YES oppure NO.

4. Eventuale conflitto tra file.

Regole:

- ACCEPTED non significa IMPLEMENTATO.
- PROPOSED non significa ACCEPTED.
- PROPOSED non significa DEPRECATED.
- DEFERRED non significa REJECTED.
- DEFERRED può descrivere uno scope di implementazione/attivazione rinviato;
  non va trattato come STATUS dell'ADR se il file autorevole indica PROPOSED.
- L'implementazione non dimostra da sola l'accettazione di un ADR.
- La documentazione non dimostra da sola l'implementazione.
- Se più file presentano stati o autorità differenti, segnala il conflitto.
- Non inventare uno stato o un file autorevole.
- Non proporre modifiche.
- Non proporre task.
- Non usare conoscenza esterna.

Rispondi in formato compatto.
