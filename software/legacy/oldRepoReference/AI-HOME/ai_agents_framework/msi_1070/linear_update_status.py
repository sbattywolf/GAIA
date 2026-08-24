import sys
import os

sys.path.insert(0, "/home/sbatta/local-ai/Scripts")
from core_lib.linear_api import query_linear

STATUS_MAPPING = {
    "done": "Done",
    "review": "Review",
    "todo": "Todo",
    "progress": "In Progress"
}

def update_status(issue_key, target_status):
    state_name = STATUS_MAPPING.get(target_status.lower())
    if not state_name:
        print(f"❌ Stato '{target_status}' non valido. Usa: todo, progress, review, done.")
        return

    # 1. Recupera l'UUID della Issue e l'UUID dello stato in un colpo solo cercando nel Team
    search_query = """
    {
      issues {
        nodes {
          id
          identifier
          title
          team {
            id
            states { nodes { id name } }
          }
        }
      }
    }
    """
    
    print(f"📦 Ricerca del ticket {issue_key.upper()} nei database di Linear...")
    search_result = query_linear(search_query)
    nodes = search_result.get('data', {}).get('issues', {}).get('nodes', []) if search_result else []
    
    # Cerchiamo il nodo che corrisponde alla nostra chiave (es. SBA-7)
    target_issue = next((i for i in nodes if i['identifier'].upper() == issue_key.upper()), None)
    
    if not target_issue:
        print(f"❌ Impossibile trovare il ticket {issue_key.upper()} su Linear. Verifica la bacheca.")
        return
        
    issue_uuid = target_issue['id']
    issue_title = target_issue['title']
    
    # Estraiamo gli stati disponibili per il team di questo ticket
    workflow_states = target_issue['team']['states']['nodes']
    state_uuid = next((s['id'] for s in workflow_states if s['name'].lower() == state_name.lower()), None)
    
    if not state_uuid:
        print(f"❌ Impossibile trovare l'ID dello stato {state_name} nel workflow del tuo team.")
        return

    # 2. Eseguiamo la mutazione finale usando solo ID di tipo UUID garantiti
    mutation = """
    mutation UpdateIssueState($id: String!, $stateId: String!) {
      issueUpdate(id: $id, input: { stateId: $stateId }) {
        success
      }
    }
    """
    variables = {"id": issue_uuid, "stateId": state_uuid}
    
    print(f"🔄 Spostamento del ticket in {state_name.upper()}...")
    result = query_linear(mutation, variables)
    
    if result and result.get('data', {}).get('issueUpdate', {}).get('success'):
        print(f"✅ Successo! Il ticket {issue_key.upper()} ({issue_title}) è stato spostato in: {state_name.upper()}")
    else:
        print(f"❌ Errore durante la mutazione di aggiornamento: {result}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("📝 Uso corretto: python3 linear_update_status.py [CHIAVE_TICKET] [STATO]")
    update_status(sys.argv[1], sys.argv[2])

