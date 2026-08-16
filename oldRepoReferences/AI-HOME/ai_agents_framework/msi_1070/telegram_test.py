import sys
import os
import requests

# 📁 Percorso assoluto statico della radice del Framework per gli import
sys.path.insert(0, "/home/sbatta/local-ai/Scripts")
from core_lib.secrets import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_test():
    # Puliamo il token da eventuali spazi bianchi residui
    token = str(TELEGRAM_BOT_TOKEN).strip()
    
    # Costruzione stringente dell'URL ufficiale delle API di Telegram
    url = f"https://telegram.org{token}/sendMessage"
    
    payload = {
        "chat_id": str(TELEGRAM_CHAT_ID).strip(),
        "text": "🚀 *Framework Local-AI*\n\nConnessione MSI 1070 -> Telegram completata con successo! Le notifiche future sono pronte.",
        "parse_mode": "Markdown"
    }
    
    print("🛰️ Invio del messaggio di prova a Telegram in corso...")
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        if response.status_code == 200 and result.get("ok"):
            print("✅ Messaggio inviato! Controlla il tuo telefono.")
        else:
            print(f"❌ Errore nell'invio del messaggio: {result}")
    except Exception as e:
        print(f"❌ Errore critico di rete: {str(e)}")

if __name__ == "__main__":
    send_telegram_test()

