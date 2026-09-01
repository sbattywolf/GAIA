# GAIA REMOTE MAIN EXCLUSIONS

## Excluded Categories

The following categories of files and directories have been excluded from the remote main materialization:

### Runtime and Generated Material
- .env files and configuration with runtime secrets
- .venv/ - Python virtual environments
- __pycache__/ - Python bytecode cache
- node_modules/ - Node.js package cache
- build/ - Build output directories
- dist/ - Distribution packages
- .git/ - Git repository data
- ollama-data/ - Model data and cache
- OpenWebUI uploaded data - User-generated content
- runtime databases - Database files

### Temporary and Backup Material
- backup/* directories - Backup files
- temporary files - Runtime temporary files
- historical branches - Non-baseline material
- old repository material - Legacy references not required for baseline

### Security and Private Information
- private infrastructure configurations
- machine-specific secrets
- private network information
- API keys and tokens
- passwords and credentials
- raw logs and debug output

### Large Binary Files
- model data files
- large dataset files
- binary executables
- compressed archives
- multimedia content

## Important Excluded Paths

### Directories Excluded
- sprints/ - Sprint directories (source material, not core content)
- gaia-bootstrap-poc/ - Bootstrap proof-of-concept (experimental, not baseline)
- gaia_1070_physical_validation/ - Physical validation material (runtime specific)
- oldRepoReference/ - Legacy repository references (historical only)
- gaia_3090_model_stack/.env - Model stack runtime configuration
- gaia_1070_model_runtime/.env - Runtime environment variables

### Files Excluded
- *.env files - Runtime environment configurations
- .env.example - Example environment files with real values
- .env.sample - Sample environment files with real values
- compose.yaml - Docker composition with machine-specific values
- docker-compose.yml - Docker composition with machine-specific values
- config.json - Configuration with private information
- settings.json - Settings with runtime data

## Reason for Exclusion

These materials have been excluded to maintain the integrity of the GAIA remote main baseline:

1. **Security**: Runtime secrets and credentials would compromise security if included
2. **Coherence**: Only essential materials required for understanding the baseline are included
3. **Size**: Large binary files and generated content would bloat the repository
4. **Relevance**: Non-essential directories that don't contribute to GAIA's identity or framework
5. **Maintenance**: Excluding these items reduces ongoing maintenance burden

The exclusion criteria ensure that only the minimal, coherent set of artifacts required for the GAIA baseline are included while maintaining security and repository efficiency.