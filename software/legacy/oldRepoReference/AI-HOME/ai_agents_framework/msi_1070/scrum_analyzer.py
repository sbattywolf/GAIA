import sys
import json
import urllib.request
import logging

# 📁 Percorso assoluto per core_lib e segreti di produzione
sys.path.insert(0, "/home/sbatta/local-ai/Scripts")
import core_lib.secrets as prod_secrets

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

OLLAMA_URL = str(prod_secrets.OLLAMA_API_URL).strip()
LINEAR_URL = str(prod_secrets.URL_LINEAR_GRAPHQL).strip()
LINEAR_TOKEN = str(prod_secrets.LINEAR_API_KEY).strip()

def http_post(url, json_data, headers=None):
    if headers is None: headers = {"Content-Type": "application/json"}
    data = json.dumps(json_data).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        logger.error(f"❌ Errore HTTP POST su {url}: {e}")
        return None

def evaluate_task_scrum(ticket_title, ticket_description):
    """Interroga l'LLM locale (Llama 3.1 8B) per estrarre Fibonacci Points e Skill Matrix"""
    system_prompt = """
    Sei il Master Scrum AI del cluster Local-AI. Analizza il task e restituisci ESCLUSIVAMENTE un oggetto JSON valido.
    
    REGOLE:
    1. Stima la complessità in Fibonacci (1, 2, 3, 5, 8, 13).
    2. Valuta l'idoneità hardware delle macchine (1-5 o N/A):
       - msi_1070: Domotica, automazioni, script leggeri.
       - rtx_3090: Calcolo pesante, LLM giganti (32B+), fine-tuning.
       - qnap_nas: Database SQL, backup, manutenzione file system.

    Rispondi solo in JSON:
    {
      "story_points": 1 | 2 | 3 | 5 | 8 | 13,
      "justification": "Spiegazione tecnica breve.",
      "machine_matrix": {"msi_1070": "1-5|N/A", "rtx_3090": "1-5|N/A", "qnap_nas": "1-5|N/A"}
    }
    """
    payload = {
        "model": "llama3.1:8b",  # 🧠 Sfrutta il nuovo e potente cervello di Zeus pullato oggi!
        "prompt": f"{system_prompt}\n\nTitolo: {ticket_title}\nDescrizione: {ticket_description}",
        "stream": False,
        "format": "json"
    }
    
    logger.info("🧠 Generazione stima Scrum via Llama 3.1...")
    res = http_post(OLLAMA_URL, payload)
    if res and "response" in res:
        try: return json.loads(res["response"])
        except Exception: logger.error("JSON fallato dall'LLM.")
    return None

def update_linear_estimate(ticket_id, points):
    """Invia la mutazione GraphQL per scrivere i punti direttamente nel campo Estimate di Linear"""
    if not points or points == "N/A":
        logger.info("Nessun punteggio numerico valido da aggiornare.")
        return False

    # Per aggiornare l'Estimate serve prima recuperare l'UUID interno dell'Issue tramite l'identificatore visibile (es. SBA-7)
    query_get_id = f"""
    query {{
      issue(id: "{ticket_id}") {{
        id
      }}
    }}
    """
    
    headers = {"Content-Type": "application/json", "Authorization": LINEAR_TOKEN}
    res_id = http_post(LINEAR_URL, {"query": query_get_id}, headers=headers)
    
    if not res_id or "data" not in res_id or not res_id["data"]["issue"]:
        logger.error(f"❌ Impossibile trovare il ticket {ticket_id} su Linear.")
        return False
        
    uuid_internal = res_id["data"]["issue"]["id"]

    # 🚀 MUTAZIONE GRAPHQL DI SCRITTURA PUNTI
    mutation_update = f"""
    mutation {{
      issueUpdate(id: "{uuid_internal}", input: {{ estimate: {int(points)} }}) {{
        success
      }}
    }}
    """
    
    res_update = http_post(LINEAR_URL, {"query": mutation_update}, headers=headers)
    if res_update and "data" in res_update and res_update["data"]["issueUpdate"]["success"]:
        logger.info(f"🎯 Linear Aggiornato! {ticket_id} impostato a {points} Story Points.")
        return True
    return False

if __name__ == "__main__":
    # Test esecutivo se lanciato direttamente da terminale passando l'ID (Es. python3 scrum_analyzer.py SBA-7)
    if len(sys.argv) > 1:
        target_ticket = sys.argv[1]
        logger.info(f"🚀 Avvio stima forzata diretta per il ticket: {target_ticket}")
        
        # Recupera i dettagli attuali del ticket per darli in pasto all'LLM
        query_details = f'query {{ issue(id: "{target_ticket}") {{ title description }} }}'
        headers = {"Content-Type": "application/json", "Authorization": LINEAR_TOKEN}
        ticket_data = http_post(LINEAR_URL, {"query": query_details}, headers=headers)
        
        if ticket_data and ticket_data.get("data", {}).get("issue"):
            issue_info = ticket_data["data"]["issue"]
            t_title = issue_info.get("title", "Task")
            t_desc = issue_info.get("description", "")
            
            scrum = evaluate_task_scrum(t_title, t_desc)
            if scrum and "story_points" in scrum:
                print(f"📊 Risultato AI: {scrum['story_points']} Punti. Motivazione: {scrum['justification']}")
                update_linear_estimate(target_ticket, scrum["story_points"])
        else:
            print("Ticket non trovato.")

