# C01 — Intent recognition

Sei il Collaborator di GAIA.

Richiesta utente:

"Vorrei sapere se la finestra della cucina è aperta."

Identifica l'intento senza eseguire alcuna azione.

Devi determinare:

- operation
- target
- parameters
- se la richiesta è read-only o state-changing
- eventuale ambiguità

Non usare conoscenza esterna.
Non inventare entity ID.
Non eseguire tool.

Rispondi in formato compatto.

GAIA BENCHMARK OUTPUT CONTRACT

Output ONLY one valid JSON object. Do not use Markdown fences.
Use the semantic fields below. Do not invent external state.

Example shape:
{
  "operation": "<operation>",
  "target": "<target>",
  "read_only": true,
  "ambiguity": true
}
