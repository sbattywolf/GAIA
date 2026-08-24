import os
import sys
import json
import urllib.request
import logging

# 📁 Percorso assoluto statico per le librerie core
sys.path.insert(0, "/home/sbatta/local-ai/Scripts")
import core_lib.secrets as prod_secrets
from core_lib.scrum_analyzer import evaluate_task_scrum  # 🧠 INIEZIONE DELLO SCRUM ANALYZER

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

LINEAR_URL = "https://linear.app"
LINEAR_TOKEN = str(prod_secrets.LINEAR_API_KEY).strip()
TEAM_ID = "IL_TUO_TEAM_ID_REALE_DI_LINEAR" # Assicurati che sia coerente

def parse_markdown_file(filepath):
    """Legge il file .md e separa il titolo dalla descrizione"""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    title = "Nuovo Task IA"
    description_lines = []
    
    for line in lines:
        if line.startswith("### TITOLO TICKET:"):
            title = line.replace("### TITOLO TICKET:", "").strip()
        else:
            description_lines.append(line)
            
    return title, "".join(description_lines).strip()

def create_linear_issue(title, description, estimate_points=None):
    """Invia la mutazione GraphQL a Linear includendo gli Story Points nativi"""
    # Se estimate_points è valido, lo forziamo nella query, altrimenti lasciamo vuoto
    estimate_field = f", estimate: {estimate_points}" if estimate_points and estimate_points != "N/A" else ""
    
    query = f"""
    mutation {{
      issueCreate(input: {{
        title: "{title}",
        description: "{description}",
        teamId: "{TEAM_ID}"
        {estimate_field}
      }}) {{
        success
        issue {{
          id
          identifier
          title
        }}
      }}
    }}
    """
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": LINEAR_TOKEN
    }
    
    req = urllib.request.Request(LINEAR_URL, data=json.dumps({"query": query}).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res = json.loads(response.read().decode("utf-8"))
            if "errors" in res:
                logger.error(f"❌ Errore GraphQL Linear: {res['errors']}")
                return None
            return res["data"]["issueCreate"]["issue"]
    except Exception as e:
        logger.error(f"❌ Errore di rete Linear: {e}")
        return None

def process_queue():
    """Scansiona la coda, invoca l'AI Scrum per la stima e carica su Linear"""
    queue_dir = "/home/sbatta/local-ai/generated_files/.backlog_queue/code_agent"
    if not os.path.exists(queue_dir):
        logger.info("Coda vuota. Nessun file da elaborare.")
        return

    files = [os.path.join(queue_dir, f) for f in os.listdir(queue_dir) if f.endswith(".md")]
    if not files:
        logger.info("Nessun ticket in coda.")
        return

    for filepath in files:
        logger.info(f"📄 Elaborazione file: {os.path.basename(filepath)}")
        title, description = parse_markdown_file(filepath)
        
        # 🧠 COGNITIVE STEP: L'AI analizza e calcola i punti in Fibonacci prima del push!
        scrum_data = evaluate_task_scrum(title, description)
        points = None
        if scrum_data and "story_points" in scrum_data:
            points = scrum_data["story_points"]
            logger.info(f"📊 AI Scrum Master ha assegnato: {points} Story Points. Motivazione: {scrum_data.get('justification')}")
        
        # Carica il ticket completo su Linear
        issue = create_linear_issue(title, description, estimate_points=points)
        
        if issue:
            logger.info(f"✅ Ticket creato con successo: {issue['identifier']} - {issue['title']}")
            # Sposta il file nell'archivio per evitare duplicati (Idempotenza)
            archive_dir = "/home/sbatta/local-ai/generated_files/.archive/code_agent"
            os.makedirs(archive_dir, exist_ok=True)
            os.rename(filepath, os.path.join(archive_dir, os.path.basename(filepath)))

if __name__ == "__main__":
    process_queue()

