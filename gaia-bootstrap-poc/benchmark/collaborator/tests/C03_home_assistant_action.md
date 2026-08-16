# C03 — Home Assistant action

Sei il Collaborator di GAIA.

Richiesta:

"Spegni la luce della cucina."

Contesto:

- esiste una luce identificata come `light.kitchen`
- il controllo deve avvenire attraverso il boundary Home Assistant di GAIA

Determina l'azione da eseguire.

Regole:

- non bypassare l'adapter/integration boundary;
- non inventare un'altra entity;
- non modificare altri dispositivi;
- non dichiarare successo senza risultato del tool.

Indica:

- operation
- target
- tool richiesto
- risultato atteso dopo l'esecuzione

Non simulare l'esecuzione.
