import os
import sys
import requests

# 📁 Trucco Python per inserire la radice del Framework nel path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Ora l'importazione dei segreti centralizzati funzionerà senza errori
from core_lib.secrets import SOURCE_DIR, OUTPUT_DIR, OLLAMA_API_URL, MODEL_1070

# 🧠 PROMPT DI SISTEMA AGGIORNATO E CENTRALIZZATO
SYSTEM_PROMPT = """Tu sei lo Scrum Master e il Technical Lead dell infrastruttura Home Assistant dell utente. 
Il tuo compito e analizzare il file YAML estratto dai backup (As-Is).
Devi rispondere ESCLUSIVAMENTE generando una Issue in formato Markdown compatibile con Linear, strutturata cosi:

### TITOLO TICKET: [Nome File]
**Epic:** Config Validation and Bug Fixing
**Priority:** High, Medium o Low

#### Description
Spiega l errore riscontrato o la svecchiatura necessaria nel componente.

#### Acceptance Criteria
- Criterio 1: Cosa sistemare.
- Criterio 2: Come verificare la validita YAML.

#### Technical Solution
Fornisci qui dentro il blocco di codice corretto. Usa i tag di codice.

Non aggiungere altri commenti. Genera il ticket in Markdown e basta."""

os.makedirs(OUTPUT_DIR, exist_ok=True)

if not os.path.exists(SOURCE_DIR):
    print(f"❌ Errore: Il punto di mount Samba non è accessibile: {SOURCE_DIR}")
    sys.exit(1)

files = [f for f in os.listdir(SOURCE_DIR) if f.endswith(('.yaml', '.yml'))]

print(f"🚀 Trovati {len(files)} file YAML nella partizione condivisa del Raspberry.")
print(f"🖥️ Avvio elaborazione locale su GTX 1070 tramite modello {MODEL_1070}...")

for file_name in files:
    file_path = os.path.join(SOURCE_DIR, file_name)
    print(f"📦 Analisi AI in corso per: {file_name}...")
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        file_content = f.read()
    
    payload = {
        "model": MODEL_1070,
        "prompt": f"Analizza il contenuto di questo file {file_name}:\n\n```yaml\n{file_content}\n```",
        "system": SYSTEM_PROMPT,
        "stream": False,
        "options": {"temperature": 0.1, "num_ctx": 8192}
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=300)
        if response.status_code == 200:
            markdown_output = response.json().get("response", "")
            output_file_name = f"linear_issue_{file_name.replace('.', '_')}.md"
            output_path = os.path.join(OUTPUT_DIR, output_file_name)
            
            with open(output_path, 'w', encoding='utf-8') as out_f:
                out_f.write(markdown_output)
            print(f"✅ Report salvato in coda: {output_file_name}")
        else:
            print(f"❌ Errore Ollama API per {file_name}: Stato HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Errore critico durante l'elaborazione di {file_name}: {str(e)}")

print(f"🏁 Fine dello Sprint automatico di analisi!")

