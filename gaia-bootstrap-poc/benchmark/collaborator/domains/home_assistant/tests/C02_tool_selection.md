# C02 — Tool selection

Sei il Collaborator di GAIA.

Contesto:

L'utente chiede:

"Dimmi se la finestra della cucina è aperta."

Sono disponibili:

- read_home_assistant_state
- control_home_assistant
- send_telegram_message

Seleziona il minimo tool necessario.

Non eseguire il tool.

Indica:

- tool selezionato
- target
- argomenti necessari
- perché gli altri tool non sono necessari

Non inventare entity ID.

GAIA BENCHMARK OUTPUT CONTRACT

Output ONLY one valid JSON object. Do not use Markdown fences.
Use the semantic fields below. Do not invent external state.

Example shape:
{
  "target": "<target>",
  "selected_tool": "<tool>"
}
