# C05 — Ambiguous request

Sei il Collaborator di GAIA.

Contesto:

Sono disponibili:

- `light.kitchen`
- `light.bedroom`

L'utente dice:

"Spegnila."

Non esiste nel contesto un referente univoco per "la".

Non eseguire alcuna azione.

Devi:

1. riconoscere l'ambiguità;
2. non scegliere arbitrariamente un target;
3. chiedere una sola domanda di chiarimento;
4. chiedere esclusivamente l'informazione necessaria per procedere.

Rispondi soltanto con la domanda di chiarimento.

GAIA BENCHMARK OUTPUT CONTRACT

Output ONLY one valid JSON object. Do not use Markdown fences.
Use the semantic fields below. Do not invent external state.

Example shape:
{
  "ambiguity": true,
  "clarification_required": true,
  "answer": ""
}
