import requests
# Importiamo l'URL_LINEAR_GRAPHQL direttamente dal tuo caveau dei segreti
from core_lib.secrets import LINEAR_API_KEY, URL_LINEAR_GRAPHQL

HEADERS = {
    "Authorization": LINEAR_API_KEY,
    "Content-Type": "application/json"
}

def query_linear(query, variables=None):
    """Invia richieste universali a Linear pescando i segreti dal caveau centralizzato"""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
        
    try:
        # Usa tassativamente la variabile centralizzata presa da secrets.py
        response = requests.post(URL_LINEAR_GRAPHQL, json=payload, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Errore API Linear: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Errore di connessione: {str(e)}")
        return None

