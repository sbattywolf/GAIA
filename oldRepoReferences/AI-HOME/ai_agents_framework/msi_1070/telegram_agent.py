import os
import sys
import logging
import subprocess
import urllib.request
import json
import time

sys.path.insert(0, "/home/sbatta/local-ai/Scripts")
import core_lib.secrets as prod_secrets

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = str(prod_secrets.TELEGRAM_BOT_TOKEN).strip()
ALLOWED_CHAT_ID = int(str(prod_secrets.TELEGRAM_CHAT_ID).strip())
OLLAMA_URL = "http://localhost:11434/api/generate"

def http_post(url, json_data):
    data = json.dumps(json_data).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        logger.error(f"❌ Errore HTTP: {e}")
        return None

def analyze_message_with_llm(user_text):
    """Usa Qwen2.5-Coder per una precisione millimetrica su JSON ed esecuzione comandi"""
    system_prompt = """
    Sei Zeus, l'Agente Esecutivo del cluster Local-AI di Sbatta. Il tuo compito è analizzare il testo ed emettere ESCLUSIVAMENTE un JSON valido. Non salutare e non aggiungere testo fuori dal JSON.

    REGOLE TASSO DI ATTIVAZIONE INTENT:
    1. Se l'utente ti ordina di accendere, spegnere, regolare o verificare dispositivi, luci, interruttori o entità della casa (es. "Accendi luci camera", "Spegni soffitto") ➡️ l'intent DEVE essere 'DOMOTICA'. Nel campo 'action_data' inserisci 'entity': 'luce_camera_letto' (o l'entità rilevata) e 'state': 'on' o 'off'.
    2. Se l'utente prende in carico o modifica un task (es. "Prendo in carico SBA-7") ➡️ l'intent è 'MODIFICA_TICKET'.
    3. Se l'utente fa solo saluti o chiacchiere generiche ➡️ l'intent è 'CHIACCHIERA'.

    Rispondi ESCLUSIVAMENTE con questa struttura JSON:
    {
      "intent": "DOMOTICA" | "CHIACCHIERA" | "MODIFICA_TICKET",
      "action_data": { "entity": "nome_entita", "state": "on|off", "ticket_id": "SBA-X" },
      "human_reply": "La tua risposta umana, cortese ed ESTREMAMENTE BREVE in italiano."
    }
    """
    
    # 🚨 RIPRISTINIAMO QWEN: È un cecchino sui JSON e non soffre le allucinazioni di Llama
    payload = {
        "model": "qwen2.5-coder:7b", 
        "prompt": f"{system_prompt}\n\nTesto Utente: \"{user_text}\"", 
        "stream": False, 
        "format": "json"
    }
    res = http_post(OLLAMA_URL, payload)
    return json.loads(res["response"]) if res and "response" in res else None

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ALLOWED_CHAT_ID: returnanalyze_message_with_llm
    await update.message.reply_text("🤖 Assistente DevOps Online!")

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ALLOWED_CHAT_ID: return
    
    user_text = update.message.text
    analysis = analyze_message_with_llm(user_text)
    
    if not analysis or "intent" not in analysis:
        await update.message.reply_text("🤷‍♂️ Micro-blocco neurale. Ripeti?")
        return

    intent = analysis.get("intent")
    action_data = analysis.get("action_data", {})
    reply_text = analysis.get("human_reply", "Ricevuto.")

    if intent == "CHIACCHIERA":
        await update.message.reply_text(reply_text, parse_mode="Markdown")
        
    elif intent == "CREA_TICKET":
        await update.message.reply_text(reply_text, parse_mode="Markdown")
        # Logica di accodamento file .md per ticket lineari qui...
        
    elif intent == "MODIFICA_TICKET" or intent == "MODICIA_TICKET":
        ticket_id = action_data.get("ticket_id")
        status = action_data.get("status_change")
        
        if ticket_id and status == "IN_PROGRESS":
            sys.path.insert(0, "/home/sbatta/local-ai/Scripts/core_lib")
            import git_flow_manager
            
            # Invocazione pulita delegata alla libreria esterna!
            res = git_flow_manager.validate_and_start_pr(ticket_id)
            
            if res["success"]:
                await update.message.reply_text(
                    f"✅ *Presa in Carico Convalidata!*\n\n"
                    f"📊 *Task*: {res['title']}\n"
                    f"🔀 *Git Flow*: Aperta branch `{res['branch']}`.\n"
                    f"🚀 *GitHub*: Pull Request creata con successo! Linear ha aggiornato lo stato."
                )
            else:
                await update.message.reply_text(f"⚠️ *Blocco di Sicurezza*: {res['error']}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

