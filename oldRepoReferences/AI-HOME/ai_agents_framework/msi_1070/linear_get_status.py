import sys
import os

sys.path.insert(0, "/home/sbatta/local-ai/Scripts")
from core_lib.linear_api import query_linear

def get_issue_status(issue_key):
    # Query globale sui ticket per estrarre lo stato senza usare filtri numerici problematici
    query = """
    {
      issues {
        nodes {
          identifier
          title
          state { name }
        }
      }
    }
    """
    
    result = query_linear(query)
    nodes = result.get('data', {}).get('issues', {}).get('nodes', []) if result else []
    
    # Cerchiamo il ticket corrispondente a livello Python
    target_issue = next((i for i in nodes if i['identifier'].upper() == issue_key.upper()), None)
    
    if target_issue:
        print(f"📊 Ticket {target_issue['identifier']}: {target_issue['title']}")
        print(f"📍 Stato Attuale: [{target_issue['state']['name'].upper()}]")
    else:
        print(f"❌ Impossibile trovare il ticket {issue_key.upper()} su Linear.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("📝 Uso: python3 linear_get_status.py [CHIAVE_TICKET]")
    get_issue_status(sys.argv[1])

