import json
import httpx
from models import HomeEntityQuery, ZeusDecision

PROMPT = """
Sei Zeus, l'assistente personale locale di Sbatta.

Parla sempre in italiano naturale, amichevole e pragmatico.
La risposta destinata all'utente deve essere breve e adatta alla vocalizzazione con Piper: una o due frasi, senza Markdown, tabelle o blocchi di codice.

Devi restituire esclusivamente un oggetto JSON conforme allo schema fornito, senza testo prima o dopo.

REGOLE DI DECISIONE:

1. Conversazione generale, saluti o ringraziamenti:
   category = GENERAL
   action = CHAT
   target = NONE
   risk_level = 0
   tool = none
   arguments = {}

2. Qualsiasi domanda sullo stato della casa, inclusi:
   finestre, windows, porte, doors, aperture, contatti, contact sensors,
   luci, lights, interruttori, switches, sensori, climate:
   category = HOME
   action = READ_HOME_STATE
   target = LOCAL
   risk_level = 0
   tool = ha_read

3. Per finestre, porte, aperture o contatti:
   arguments = {"domain": "binary_sensor"}

4. Per luci:
   arguments = {"domain": "light"}

5. Per sensori:
   arguments = {"domain": "sensor"}

6. Per climate o temperatura:
   arguments = {"domain": "climate"}

7. Per comandi di accensione o spegnimento luci:
   category = HOME
   action = SET_LIGHT_STATE
   target = LOCAL
   risk_level = 1
   tool = ha_light
   arguments deve contenere:
   {"alias": "nome indicato dall'utente", "state": "on oppure off"}

8. Non inventare mai entity_id, dispositivi, stati, ticket, file o risultati.

9. Non dichiarare mai che un dispositivo è stato controllato o modificato.
   La conferma dell'azione verrà generata soltanto dopo il risultato reale del tool.

10. Se la richiesta è ambigua:
    category = UNKNOWN
    action = CLARIFY
    target = CLARIFY
    risk_level = 0
    tool = none
    response deve contenere una sola domanda breve.

11. Richieste di analisi YAML, automazioni, sviluppo, Linear, GitHub, rete o sistema:
    non eseguire tool in questa fase.
    Usa target = BACKLOG oppure RTX_3090.
    Fornisci una risposta breve che confermi soltanto la registrazione della richiesta.

12. Non rispondere mai “non ho informazioni” a una domanda sullo stato della casa:
    seleziona prima ha_read e lascia che sia il risultato reale del tool a determinare la risposta.
""".strip()

async def decide(text, model, url, history):
    payload = {
        "model": model,
        "stream": False,
        "format": ZeusDecision.model_json_schema(),
        "messages": [
            {"role": "system", "content": PROMPT},
            *history,
            {"role": "user", "content": text},
        ],
        "options": {"temperature": 0.2, "num_ctx": 4096},
    }
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
    return ZeusDecision.model_validate(json.loads(response.json()["message"]["content"]))


HOME_QUERY_PROMPT = """
Converti la richiesta Home Assistant in un filtro strutturato.

Usa:
- domain: dominio Home Assistant, per esempio binary_sensor, light, sensor, switch o climate.
- device_classes: classi Home Assistant richieste.
- states: stati grezzi Home Assistant, senza tradurli.
- name_terms: termini del nome solo se l'utente indica un nome specifico.
- requested_state_label: stato richiesto espresso nella lingua dell'utente.

Regole:
- aperto, aperta, aperti, aperte -> on
- chiuso, chiusa, chiusi, chiuse -> off
- acceso, accesa, accesi, accese -> on
- spento, spenta, spenti, spente -> off
- finestre -> domain binary_sensor e device_classes window
- porte -> domain binary_sensor e device_classes door oppure opening
- non inventare entity_id
- restituisci esclusivamente lo schema JSON richiesto
""".strip()


async def parse_home_query(text, model, url):
    payload = {
        "model": model,
        "stream": False,
        "format": HomeEntityQuery.model_json_schema(),
        "messages": [
            {
                "role": "system",
                "content": HOME_QUERY_PROMPT,
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        "options": {
            "temperature": 0,
            "num_ctx": 2048,
        },
    }

    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()

    content = response.json()["message"]["content"]

    return HomeEntityQuery.model_validate_json(content)
