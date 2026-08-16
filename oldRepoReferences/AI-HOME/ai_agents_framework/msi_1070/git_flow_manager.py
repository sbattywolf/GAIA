import subprocess
import os
import sys

REPO_PATH = "/home/sbatta/github_repos/home_assistant_framework/"

def run_cmd(cmd, cwd=None):
    try:
        return subprocess.check_output(cmd, cwd=cwd, stderr=subprocess.STDOUT, text=True).strip()
    except subprocess.CalledProcessError as e:
        return f"ERROR: {e.output}"

def validate_and_start_pr(ticket_id):
    """Verifica il ticket su Linear, crea la branch ed apre la PR su GitHub in modalità non interattiva"""
    
    # 📋 1. Ispezione su Linear
    linear_output = run_cmd(["python3", "/home/sbatta/local-ai/Scripts/msi_1070/linear_get_status.py", ticket_id])
    
    ticket_title = None
    for line in linear_output.split("\n"):
        if "Ticket" in line and ":" in line:
            # Estrae la stringa dopo i due punti in modo sicuro
            ticket_title = line.split(":", 1)[1].strip()
            break
            
    if not ticket_title or "ERROR" in linear_output or "non trovato" in linear_output.lower():
        return {"success": False, "error": f"Il ticket `{ticket_id}` non esiste o non è valido su Linear."}

    # 🔀 2. Sincronizzazione locale Git
    run_cmd(["git", "checkout", "main"], cwd=REPO_PATH)
    run_cmd(["git", "pull", "origin", "main"], cwd=REPO_PATH)
    
    # Pulizia del titolo per renderlo un nome branch valido
    clean_title = "".join(c for c in ticket_title.lower().replace(" ", "_") if c.isalnum() or c == "_")
    branch_name = f"feature/{ticket_id}_{clean_title[:30]}" # Accorciamo per sicurezza
    
    # Crea e passa sulla nuova branch
    run_cmd(["git", "checkout", "-b", branch_name], cwd=REPO_PATH)
    
    # Spinge la branch sul cloud di GitHub
    run_cmd(["git", "push", "-u", "origin", branch_name], cwd=REPO_PATH)
    
    # 🚀 3. Creazione PR atomica NON INTERATTIVA (Evita blocchi di sistema)
    pr_cmd = [
        "gh", "pr", "create",
        "-t", f"Merge {ticket_id}: {ticket_title}",
        "-b", f"PR automatica generata dall'Agente DevOps 1070 per il task {ticket_id}.",
        "--base", "main",
        "--head", branch_name
    ]
    pr_res = run_cmd(pr_cmd, cwd=REPO_PATH)
    
    if "ERROR" in pr_res:
        return {"success": False, "error": f"Ramo spinto, ma errore apertura PR: {pr_res}"}
        
    return {"success": True, "title": ticket_title, "branch": branch_name}

