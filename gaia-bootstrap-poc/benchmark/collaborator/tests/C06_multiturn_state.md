# C06 — Multiturn state

Sei il Collaborator di GAIA.

Turno 1:

Utente:
"Controlla la finestra della cucina."

Il Collaborator identifica la finestra della cucina come target e osserva il relativo stato tramite il tool appropriato.

Turno 2:

Utente:
"E quella della camera?"

Devi mantenere il contesto dell'operazione precedente ma aggiornare il target.

Determina:

- operation
- nuovo target
- quali informazioni del turno precedente devono essere mantenute
- quali informazioni devono essere sostituite

Regole:

- "quella della camera" deve riferirsi alla finestra della camera;
- non mantenere erroneamente la cucina come target;
- non inventare entity ID;
- distinguere conversation state da external state;
- se lo stato corrente è necessario, deve essere ottenuto dal tool appropriato.

Non eseguire tool in questo test.

Rispondi in formato compatto.
