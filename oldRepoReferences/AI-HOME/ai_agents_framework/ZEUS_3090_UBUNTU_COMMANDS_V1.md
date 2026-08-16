# ZEUS 3090 — Ubuntu Bootstrap Commands

## 00 — System information

```bash
cat /etc/os-release
uname -a
uname -m
lscpu
lspci | grep -i nvidia || true
df -h /
free -h
```

## 01 — Operating system update

```bash
sudo apt update
sudo apt full-upgrade -y
sudo reboot
```

## 02 — Base terminal and development tools

```bash
sudo apt update
sudo apt install -y \
  apt-transport-https \
  build-essential \
  ca-certificates \
  cmake \
  curl \
  direnv \
  fd-find \
  git \
  git-lfs \
  gnupg \
  htop \
  jq \
  make \
  nano \
  net-tools \
  nvtop \
  openssh-client \
  openssh-server \
  pipx \
  pkg-config \
  python3 \
  python3-dev \
  python3-pip \
  python3-venv \
  ripgrep \
  rsync \
  shellcheck \
  software-properties-common \
  tmux \
  tree \
  ufw \
  unzip \
  vim \
  wget \
  zip
sudo systemctl enable --now ssh
git lfs install
pipx ensurepath
```

## 03 — NVIDIA driver verification

```bash
nvidia-smi
```

## 04 — NVIDIA driver installation only if `nvidia-smi` fails

```bash
sudo apt update
sudo apt install -y ubuntu-drivers-common
ubuntu-drivers devices
sudo ubuntu-drivers install
sudo reboot
```

## 05 — NVIDIA verification after reboot

```bash
nvidia-smi
nvidia-smi --query-gpu=name,driver_version,memory.total,temperature.gpu,power.draw --format=csv
```

## 06 — Git configuration

```bash
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global fetch.prune true
git config --global core.autocrlf input
git config --global core.editor "code --wait"
git config --global --list
```

## 07 — Visual Studio Code repository

```bash
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /usr/share/keyrings/packages.microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
rm -f packages.microsoft.gpg
sudo apt update
sudo apt install -y code
code --version
```

## 08 — VS Code development extensions

```bash
code --install-extension eamodio.gitlens
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension redhat.vscode-yaml
code --install-extension tamasfe.even-better-toml
code --install-extension streetsidesoftware.code-spell-checker
code --list-extensions
```

## 09 — Ollama native installation

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama --version
sudo systemctl enable --now ollama
sudo systemctl status ollama --no-pager
curl -s http://127.0.0.1:11434/api/tags | jq
sudo ss -ltnp | grep 11434
```

## 10 — Primary local model

```bash
ollama pull qwen2.5-coder:14b
ollama list
ollama show qwen2.5-coder:14b
ollama run qwen2.5-coder:14b "Reply only with: ZEUS 3090 MODEL OK"
ollama ps
nvidia-smi
```

## 11 — Python quality and testing tools

```bash
pipx install poetry
pipx install pre-commit
pipx install ruff
pipx install uv
pipx install virtualenv
pipx list
```

## 12 — Workspace

```bash
mkdir -p ~/github_repos
cd ~/github_repos
```

## 13 — Repository clone

```bash
export ZEUS_REPOSITORY_URL="https://github.com/sbattywolf/home_assistant_framework.git"
git clone "$ZEUS_REPOSITORY_URL" ai_agents_framework
cd ai_agents_framework
git status
git branch --show-current
git checkout -b feature/zeus-phase-0-1
tree -a -L 3
```

## 14 — Python virtual environment

```bash
cd ~/github_repos/ai_agents_framework
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install pytest pytest-asyncio pytest-cov pytest-mock requests-mock respx
python --version
pytest --version
deactivate
```

## 15 — Local secrets protection

```bash
cd ~/github_repos/ai_agents_framework
printf '\n.venv/\n__pycache__/\n.pytest_cache/\n.coverage\nhtmlcov/\n.env\n.env.*\n!.env.example\n**/secrets.py\n*.db\n*.sqlite\n*.sqlite3\nlogs/\ndata/\nartifacts/\nopen_webui_backup/\n' >> .gitignore
git status --short
```

## 16 — SSH key for Git hosting

```bash
ssh-keygen -t ed25519 -C "REPLACE_WITH_EMAIL"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub
```

## 17 — Monitoring

```bash
watch -n 2 nvidia-smi
```

## 18 — Verification

```bash
git --version
python3 --version
pipx --version
code --version
ollama --version
ollama list
curl -s http://127.0.0.1:11434/api/tags | jq
nvidia-smi
sudo systemctl status ollama --no-pager
sudo systemctl status ssh --no-pager
```

# DEFERRED — Execute when Phase 2 Home Assistant test begins

## 19 — Docker conflicting packages removal

```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove -y "$pkg" 2>/dev/null || true; done
```

## 20 — Docker Engine repository

```bash
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
. /etc/os-release
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu ${UBUNTU_CODENAME:-$VERSION_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
newgrp docker
```

## 21 — Docker verification

```bash
docker version
docker compose version
docker run --rm hello-world
```

## 22 — VS Code container extensions

```bash
code --install-extension ms-azuretools.vscode-docker
code --install-extension ms-vscode-remote.remote-containers
```

## 23 — Home Assistant test directories

```bash
mkdir -p ~/zeus-lab/home-assistant-test/config
mkdir -p ~/zeus-lab/home-assistant-test/fixtures
mkdir -p ~/zeus-lab/home-assistant-test/backups
```

# DEFERRED — Execute only after Phase 5 requires a second model

## 24 — Optional architecture model

```bash
ollama pull qwen3:14b
ollama list
```

# DEFERRED — Execute only after a measured 14B benchmark failure

## 25 — Optional heavy model benchmark

```bash
ollama pull qwen3-coder:30b
ollama list
watch -n 2 nvidia-smi
```
