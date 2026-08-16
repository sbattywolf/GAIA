import os
import sys
import json
import asyncio
import datetime
import websockets

# 📁 Percorso assoluto statico della radice del Framework
sys.path.insert(0, "/home/sbatta/local-ai/Scripts")
from core_lib.secrets import RASPBERRY_IP, MODEL_1070, OLLAMA_API_URL, HA_TOKEN

HA_WS_URL = f"ws://{RASPBERRY_IP}:8123/api/websocket"
DOMOTICS_QUEUE = "/home/sbatta/local-ai/generated_files/.backlog_queue/domotics_agent"

# Mappa dello stato reale monitorato in tempo reale
HOUSE_STATE = {
    "ufficio": {"luci": "off", "presenza": "off"},
    "bagno": {"luci": "off", "movimento": "off"},
    "camera_letto": {"finestra": "Chiusa", "luci": "off"}
}

async def authenticate(websocket):
    auth_request = await websocket.recv()
    auth_json = json.loads(auth_request)
    if auth_json.get("type") == "auth_required":
        await websocket.send(json.dumps({"type": "auth", "access_token": HA_TOKEN}))
        auth_response = await websocket.recv()
        if json.loads(auth_response).get("type") == "auth_ok":
            print("✅ Autenticato con successo su Home Assistant Live API!")
            return True
    return False

async def subscribe_events(websocket):
    subscribe_msg = {"id": 1, "type": "subscribe_events", "event_type": "state_changed"}
    await websocket.send(json.dumps(subscribe_msg))
    print("📡 Iscrizione agli eventi live completata. Ascolto attivo...")

async def process_event(event_data):
    try:
        event = event_data.get("event", {})
        entity_id = event.get("data", {}).get("entity_id", "")
        new_state = event.get("data", {}).get("new_state", {}).get("state", "")
        
        if "light.desk_light" in entity_id or "light.luce_tetto" in entity_id:
            HOUSE_STATE["ufficio"]["luci"] = new_state
        elif "binary_sensor.finestra_letto_dx_porta" in entity_id:
            HOUSE_STATE["camera_letto"]["finestra"] = "Aperta" if new_state == "on" else "Chiusa"
        elif "binary_sensor.sensore_movimento_bagno_occupancy" in entity_id:
            HOUSE_STATE["bagno"]["movimento"] = "Movimento" if new_state == "on" else "Nessun Movimento"
    except Exception as e:
        pass

def generate_markdown_report():
    """Genera il report formattato in caso di anomalie riscontrate"""
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"security_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = os.path.join(DOMOTICS_QUEUE, filename)
    
    anomalies = []
    if HOUSE_STATE["camera_letto"]["finestra"] == "Aperta":
        anomalies.append("- 🪟 **Camera da Letto**: La finestra risulta aperta a tarda notte!")
    if HOUSE_STATE["ufficio"]["luci"] == "on":
        anomalies.append("- 💡 **Ufficio**: Le luci sono rimaste accese!")
        
    if not anomalies:
        print("🔒 Controllo sicurezza: Tutto in regola, nessun report generato.")
        return

    report_content = f"""### TITOLO TICKET: Report Sicurezza Seriale Domotica
**Generato il:** {now_str}
**Epic:** Domotics Live Monitoring
**Priority:** Medium

#### Description
Il sistema di monitoraggio live ha rilevato delle potenziali vulnerabilità o dimenticanze nella gestione della casa.

#### Rilevamenti Critici
{chr(10).join(anomalies)}

#### Status Completo Stanze
- **Ufficio**: Luci [{HOUSE_STATE['ufficio']['luci'].upper()}]
- **Bagno**: Stato [{HOUSE_STATE['bagno'].get('movimento', 'UNKNOWN').upper()}]
- **Camera da Letto**: Finestra [{HOUSE_STATE['camera_letto']['finestra'].upper()}]
"""
    os.makedirs(DOMOTICS_QUEUE, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"📄 Report di sicurezza salvato in coda: {filename}")

async def timed_report_checker():
    """Controlla l'orario ogni minuto ed esegue il report alle 23:30"""
    while True:
        now = datetime.datetime.now()
        if now.hour == 23 and now.minute == 30:
            generate_markdown_report()
            await asyncio.sleep(60) # Evita doppie esecuzioni nello stesso minuto
        await asyncio.sleep(30)

async def main_loop():
    # Avvia il controllo orario in background
    asyncio.create_task(timed_report_checker())
    
    while True:
        try:
            async with websockets.connect(HA_WS_URL) as websocket:
                if await authenticate(websocket):
                    await subscribe_events(websocket)
                    while True:
                        message = await websocket.recv()
                        await process_event(json.loads(message))
        except Exception as e:
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("\n🛑 Agente Domotico arrestato.")

