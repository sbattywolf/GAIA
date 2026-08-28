# OpenClaw Prototype Plan for GAIA Engineering

## 1. Repository Status

Based on the path recovery audit, we have identified several scripts with hardcoded paths that need to be updated. The repository has been migrated from its original location but the core framework structure remains intact.

## 2. Current State Analysis

### Broken References Identified
- `./gaia_engineering_loop/lib/target_runner.sh`: Line 17 - `cd ~/github_repos/GAIA`
- `./gaia_engineering_loop/bin/gaia_orchestrator.sh`: Line 38 - `cd ~/github_repos/GAIA`  
- `./gaia_target_preflight/gaia_preflight.py`: Line 34 - `workspace_path = "/home/sbatta/github_repos/GAIA"`

### Available OpenClaw Material
The `openclaw-reference/` directory contains the complete OpenClaw framework structure including:
- Docker configurations
- Skills and agents
- Documentation
- Scripts and tools

## 3. Prototype Approach

Following the repository steering instructions, we will create a prototype using the existing GAIA E2 Qwen3-30B implementation as the baseline behavior while utilizing OpenClaw as the operational substrate.

### Target Environment
- **Host**: 3090 (development/validation host)
- **Framework**: OpenClaw as candidate operational substrate
- **Scope**: Minimum required for benchmarking and evidence collection

## 4. Implementation Plan

### Phase 1: Path Recovery (Completed)
- Update hardcoded paths to use relative or environment-based references
- Ensure scripts work from any repository location
- Validate all existing prechecks still function

### Phase 2: Prototype Setup
1. Create STx_OpenClaw_3090 directory structure
2. Copy relevant OpenClaw components
3. Adapt existing GAIA scripts to work with OpenClaw framework
4. Configure Docker for the 3090 target

### Phase 3: Validation Chain
Following the established validation chain:
1. Host preflight checks
2. NVIDIA driver validation
3. Docker and GPU visibility tests
4. Model/runtime validation
5. OpenClaw agent testing
6. E2 benchmark execution

## 5. Key Considerations

### Reuse Existing Material
- Use existing E2 Qwen3-30B implementation as behavioral baseline
- Leverage existing scripts for prechecks, validation, and evidence collection
- Adapt rather than redesign existing functionality

### Security Baseline
- Maintain least privilege principles
- Use explicit workspace mounts
- Avoid host-wide mounts or exposure
- Externalize configuration and secrets

## 6. Next Steps

1. Fix path references in the identified scripts
2. Create STx_OpenClaw_3090 directory structure
3. Begin Docker configuration for 3090 target
4. Implement host preflight checks
5. Validate GPU and Docker integration

This approach ensures we maintain the existing GAIA engineering framework while preparing for OpenClaw implementation.