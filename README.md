# GAIA Repository

## Overview
GAIA is a hybrid configuration platform integrating AI/LLM capabilities with service-oriented architecture. This repository contains the source code, documentation, and workflows for developing and maintaining GAIA.

## Key Documents

### 1. Branch Strategy
- **Purpose**: Defines the branching model for development.
- **Location**: [doc/Branch_Strategy.md](doc/Branch_Strategy.md)
- **Highlights**:
  - `main`: Stable production-ready code.
  - `develop`: Integration branch for ongoing development.
  - `feature/*`: Dedicated branches for new features.

### 2. Commit Workflow
- **Purpose**: Ensures consistent and traceable commits.
- **Location**: [doc/REFINED_COMMIT_WORKFLOW.md](doc/REFINED_COMMIT_WORKFLOW.md)
- **Highlights**:
  - Conventional Commits format.
  - Atomic commits for logical changes.

### 3. GitHub Labeling Strategy
- **Purpose**: Organizes and prioritizes tasks.
- **Location**: [doc/REFINED_GITHUB_LABELS.md](doc/REFINED_GITHUB_LABELS.md)
- **Highlights**:
  - Priority labels (e.g., `priority: high`).
  - Scope labels (e.g., `scope: ai`).
  - Automation for label assignment.

## Development Environment

### Prerequisites
- Python 3.9+
- Docker
- WSL 2 (Windows)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/gaia.git
   ```
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   ```bash
   source .venv/bin/activate  # Linux/Mac
   .\.venv\Scripts\Activate.ps1  # Windows
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Docker Configuration
- **Purpose**: Simplifies local development and testing.
- **Files**:
  - `Dockerfile`
  - `docker-compose.yml`
- **Commands**:
  ```bash
  docker-compose up
  ```

## Runtime Configuration

Certain runtime behaviours for local coordination can be configured via environment variables.

- `CLAIMS_BACKEND`: choose the claims backend. Values: `sqlite` (default) or `file`.
  - `sqlite` uses a repo-local SQLite DB at `.tmp/claims.db` for atomic, transactional claims.
  - `file` uses the legacy file-based `.tmp/claims/*.json` with `.lock` files.
- `CLAIMS_LOCK_TIMEOUT`: (float seconds) lock acquisition timeout used by the file lock fallback. Default `5.0` seconds.

To force the file-based backend in a shell session:

```bash
export CLAIMS_BACKEND=file
# or on Windows PowerShell
$env:CLAIMS_BACKEND='file'
```

To explicitly enable the SQLite backend (normally the default):

```bash
export CLAIMS_BACKEND=sqlite
# or on Windows PowerShell
$env:CLAIMS_BACKEND='sqlite'
```

The CI uses the SQLite backend by default to make tests more reliable; you can override these variables in CI if needed.

## Roadmap
- **Short-Term Goals**:
  - Optimize GitHub workflows.
  - Automate task movement in GitHub Projects.
- **Long-Term Goals**:
  - Transition to hybrid configurations.
  - Integrate AI/LLM services.

---

For detailed documentation, refer to the `doc/` directory.
