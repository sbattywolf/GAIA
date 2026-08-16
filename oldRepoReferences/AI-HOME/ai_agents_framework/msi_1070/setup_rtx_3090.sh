#!/bin/bash
# 🚀 AUTOMATED SETUP MANIFEST FOR NVIDIA RTX 3090 (24GB VRAM)
# Framework: Local AI Automation Framework v1.2.0
# Target OS: Ubuntu Desktop (Full Installation)

set -e
echo "🔥 Avvio installazione e configurazione dello stack pesante per la RTX 3090..."

# ---------------------------------------------------------------------
# FASE 1: REPOSITORY & DRIVER NVIDIA CON LIMITAZIONE TERMICA MINI-ITX
# ---------------------------------------------------------------------
echo "📦 Configurazione driver grafici e sblocco CUDA..."
sudo add-apt-repository ppa:graphics-drivers/ppa -y
sudo apt update

# Installazione del driver server headless di produzione e delle utils
sudo apt install -y nvidia-driver-550-server nvidia-utils-550-server

# 🚨 APPLICAZIONE DEL POWER LIMIT RIGIDO A 250W PER PREVENIRE IL SURRISCALDAMENTO IN MINI-ITX
echo "💾 Configurazione persistenza Power Limit a 250W..."
sudo nvidia-smi -pm 1
sudo nvidia-smi -pl 250
# Rendiamo persistente il limite termico al boot tramite systemd
sudo bash -c 'cat << EOF > /etc/systemd/system/nvidia-power-limit.service
[Unit]
Description=Imposta il Power Limit a 250W per la RTX 3090 Mini-ITX
After=nvidia-persistenced.service
Requires=nvidia-persistenced.service

[Service]
Type=oneshot
ExecStart=/usr/bin/nvidia-smi -pl 250
RemainAfterExit=yes

[Unit]
Description=Imposta il Power Limit a 250W per la RTX 3090 Mini-ITX

[Install]
WantedBy=multi-user.target
EOF'
sudo systemctl enable nvidia-power-limit.service

# ---------------------------------------------------------------------
# FASE 2: AMBIENTE DOCKER E CONVENZIONI HARDWARE PER AGENTI
# ---------------------------------------------------------------------
echo "🐳 Installazione Docker Engine e Nvidia Container Toolkit..."
sudo apt install -y docker.io docker-compose curl

# Abilitazione dell'utente locale senza password di root
sudo usermod -aG docker $USER

# Installazione del toolkit ufficiale per far ereditare la GPU a Docker
curl -fsSL https://github.io | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://github.io | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt update
sudo apt install -y nvidia-container-toolkit
sudo systemctl restart docker

# ---------------------------------------------------------------------
# FASE 3: ENVIRONMENT DI CODING, TESTING ED AUTOMAZIONE DEVOPS (OpenClaw)
# ---------------------------------------------------------------------
echo "🐍 Configurazione stack Python3, Testing e GitHub CLI..."
sudo apt install -y python3-pip python3-venv git gh python3-pytest python3-mock

# Installazione librerie core per gli agenti asincroni e connessione API
pip3 install --upgrade pip
pip3 install httpx pydantic asyncio telegram-text python-telegram-bot

# ---------------------------------------------------------------------
# FASE 4: ARCHIVIO E CONDIVISIONE MODELLI WINDOWS (MONTAGGIO NTFS)
# ---------------------------------------------------------------------
echo "💾 Predisposizione cartella di mount per i modelli condivisi con Windows..."
sudo mkdir -p /mnt/windows_models
sudo chmod 777 /mnt/windows_models

echo "🏁 Setup completato con successo! Riavvia la macchina ed esegui 'nvidia-smi' per validare i 24GB di VRAM."
