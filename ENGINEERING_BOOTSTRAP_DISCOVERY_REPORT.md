# Engineering Bootstrap Discovery Report

## A. Existing Bootstrap/Setup Artifacts Discovered

### Reusable Artifacts:
1. **gaia_target_preflight/** - Host preflight utility with comprehensive system checks
2. **gaia_1070_model_runtime/** - Container-based model runtime environment
3. **gaia_1070_target_experiment/** - Experiment scripts for isolated Ollama testing
4. **gaia_1070_target_mock/** - Mock container implementation for testing
5. **gaia_domestic_agent_mvp/** - MVP domestic agent implementation

### Target-Specific Artifacts:
1. **gaia_1070_model_runtime/docker-compose.yml** - 1070-specific Docker configuration
2. **gaia_1070_target_experiment/** - Experiment scripts for 1070 target
3. **docker-compose.override.yml** - Host-specific override configurations

### Project-Specific Artifacts:
1. **PM001_EVIDENCE.md, PM002_EVIDENCE.md** - Project validation evidence
2. **test_preflight.py** - Unit tests for preflight functionality
3. **test_pm001_repeatable_bounded_read.py** - PM-001 capability tests

### Experimental Artifacts:
1. All 1070 directories contain experimental phase implementations
2. Various test scripts in different directories
3. Isolated container testing frameworks

### Obsolete/Unknown:
1. Some files in .pytest_cache and __pycache__ directories (temporary artifacts)
2. Legacy experiment scripts that may not be actively maintained

## B. Existing Privileged Operations Discovered

### Human Owner Required Privilege Operations:
1. **Docker installation/configuration** - requires package manager access
2. **Docker group setup** - requires user/group modification
3. **System packages** - requires sudo for apt/yum operations  
4. **NVIDIA host prerequisites** - requires driver installation
5. **Persistent host configuration** - requires /etc modifications

### Current Privilege Handling:
- All existing scripts require explicit human execution with appropriate permissions
- No automatic sudo escalation occurs
- No automatic package installations occur
- Host configuration modifications are not automated

## C. Existing 3090-Specific Logic

### 3090 Host Checks:
1. **gaia_target_preflight/gaia_preflight.py** - Comprehensive system checks for 3090 host
2. **Python environment validation** - checks for required packages and dependencies
3. **Docker daemon access verification** - ensures user has proper Docker permissions
4. **NVIDIA GPU information gathering** - collects 3090-specific GPU details

### 3090-Targeted Features:
1. **GPU-aware preflight checks** - specifically detects NVIDIA 3090 configuration
2. **Host-specific port validation** - understands 3090 network requirements
3. **Workspace space verification** - ensures sufficient disk space for experiments

## D. Existing 1070-Specific Logic

### 1070 Container Logic:
1. **Docker Compose setup** - creates isolated environment for 1070 target
2. **Port mapping isolation** - maps port 11435 to avoid host conflicts (11434)
3. **Model pulling** - specifies qwen2.5-coder:14b model for experiments
4. **GPU access configuration** - includes NVIDIA GPU support in container

### 1070-Specific Features:
1. **Isolated runtime environment** - prevents interference with host Ollama
2. **Specific model requirements** - targets qwen2.5-coder:14b for experiments
3. **Port isolation mechanism** - ensures no conflicts with host services

## E. Reusable/Common Candidates

### Common Components:
1. **Host system validation logic** - from gaia_preflight.py (system checks)
2. **Docker availability verification** - reusable Docker checking functions
3. **Process execution monitoring** - consistent command execution patterns
4. **Result reporting and evidence generation** - structured output format

### Cross-Platform Logic:
1. **Package manager detection** - identifies available package managers
2. **Command availability checks** - generic tool detection utilities
3. **Network port validation** - port checking mechanisms
4. **Resource monitoring** - disk space and memory checks

## F. Target-Specific Candidates

### 3090-Specific Logic:
1. **NVIDIA GPU detection** - 3090-specific GPU information gathering
2. **Host network configuration** - 3090 network environment specifics
3. **System permission model** - 3090 user/group access patterns

### 1070-Specific Logic:
1. **Container port mapping** - 1070 specific port isolation
2. **Model availability verification** - 1070 target model requirements
3. **GPU configuration in containers** - container-specific GPU access

## G. Recommended Future Directory/Package Structure

```
target_bootstrap/
├── common/               # Reusable components
│   ├── system_checks.py  # Generic host checks
│   ├── docker_utils.sh   # Docker utility functions  
│   ├── package_manager.py # Package manager detection
│   └── validation_utils.py # Validation utilities
├── privileged/           # Privileged operations (reviewed)
│   ├── docker_setup.sh   # Docker installation
│   ├── nvidia_setup.sh   # NVIDIA driver setup
│   └── group_management.sh # User/group configuration
├── safe/                 # Safe operations (no privileges)
│   ├── host_preflight.py # Host preflight validation
│   ├── container_setup.sh # Container environment
│   └── model_validation.sh # Model checking
├── validation/           # Validation modules  
│   ├── docker_validation.sh
│   ├── gpu_validation.sh
│   └── ollama_validation.sh
└── profiles/             # Target-specific configurations
    ├── ubuntu_3090.yaml
    ├── ubuntu_1070.yaml
    └── raspberry_pi4.yaml
```

## H. Recommended Metadata/Manifest Approach

### Manifest Structure:
```yaml
target: ubuntu_nvidia_3090
required:
  - python3
  - git  
  - curl
  - jq
  - docker
  - docker-compose
  - nvidia-smi
optional:
  - ollama
privileged:
  - docker_install
  - docker_group_setup
status:
  - required: present
  - optional: missing
  - privileged: sudo_required
```

## I. Recommended Privilege-Warning Convention

### Warning Format:
```
⚠ SUDO REQUIRED
Operation: Docker group setup
Scope: User sbatta added to docker group
Human Owner approval required.
```

### Implementation Pattern:
```bash
# Check for privilege requirement
if [ "$PRIVILEGE_REQUIRED" = "YES" ]; then
    echo "⚠ SUDO REQUIRED"
    echo "Operation: <description>"
    echo "Scope: <host mutation>"
    echo "Human Owner approval required."
    exit 1
fi
```

## J. Recommended Relationship with Target Host Preflight

### Recommended Flow:
```
TARGET PREFLIGHT
     ↓
Requirements manifest
     ↓
Missing prerequisites
     ↓
Privileged setup (reviewed)
     ↓
Post-install validation
     ↓
BASELINE READY
     ↓
Experiment/test stages
```

### Integration Points:
1. **Preflight as baseline** - gaia_target_preflight provides initial validation
2. **Bootstrap as enhancement** - target_bootstrap adds missing prerequisites
3. **Validation as verification** - each module validates its specific requirements

## K. Recommended Guard/Test/Validation/Evidence Structure

### Module Pattern:
```
GUARD      # Check prerequisites
   ↓
TEST       # Execute actual functionality  
   ↓
VALIDATE   # Verify correct behavior
   ↓
EVIDENCE   # Generate machine-readable proof
   ↓
SUMMARY    # Human-readable results
```

### Implementation Example:
```bash
# Guard phase - lightweight checks
if ! command -v docker &> /dev/null; then
    echo "BLOCKED: Docker not found"
    exit 1
fi

# Test phase - actual functionality
docker ps > /dev/null 2>&1

# Validate phase - verify correct behavior  
if [ $? -eq 0 ]; then
    echo "PASS: Docker daemon working"
else
    echo "FAIL: Docker daemon not responding"
    exit 1
fi
```

## L. E1 Documentation Changes Recommended

### Current Status:
- **SAFE / AUTO**: Read-only inspection, tests, validation, local evidence generation ✅
- **BOUNDED WORKSPACE MUTATION**: Create/modify project files (limited to test artifacts) ✅  
- **GIT MUTATION**: Commit/push only when explicitly authorized by task ✅
- **HOST MUTATION**: Human Owner approval required for system changes ✅
- **PRIVILEGED**: No sudo/root/system configuration allowed ✅
- **DESTRUCTIVE/UNKNOWN**: STOP - No destructive operations ✅

### Documentation Updates:
1. Add explicit privilege warning convention to documentation
2. Document the relationship between preflight and bootstrap utilities
3. Record current E1 policy in README or engineering documentation
4. Add guard/test/validation pattern guidelines
5. Add progressive engineering loop model documentation
6. Include classification model for discovered artifacts
7. Document end-of-cycle consolidation process

## M. Integration with Progressive Engineering Loop

The implementation now supports the progressive engineering loop by:

### Execution Process:
- Each module follows the execution → test → validation → evidence → classification → knowledge → next stage pattern
- All modules maintain PASS/FAIL/BLOCKED semantics as required
- Evidence generation is machine-readable and consistent across modules
- Classification of artifacts occurs during each cycle

### Knowledge Acquisition:
- Each phase produces specific knowledge about resource requirements, error handling, and system capabilities
- Failures are classified appropriately (FAILED, BLOCKED) to inform next iterations  
- Successful validations are classified as VALIDATED or REUSABLE for future use
- Experimental artifacts are marked as EXPERIMENTAL for continued evaluation

### Continuous Improvement:
- The guard tests implemented in validate.sh and test_p5.sh provide early detection of prerequisites
- Classification of failures reveals missing guards that should be added in future iterations
- Evidence from each stage can be used to improve the execution strategy of next stages
- All modules maintain autonomy while contributing to collective knowledge

## N. Future Expansion Considerations

### Next Cycle Improvements:
1. **Enhanced Guard Coverage** - Add more granular checks for resource constraints
2. **Improved Classification** - Expand classification model with more detailed categories  
3. **Better Evidence Integration** - Standardize evidence format across all modules
4. **Automated Consolidation** - Develop tools to assist with end-of-cycle reviews

### Cross-Target Learning:
1. **3090 vs 1070 differences** - Continue to reveal target-specific requirements
2. **Pattern recognition** - Identify when patterns appear consistently across targets
3. **Abstraction candidates** - Build evidence for when abstractions are justified
4. **Risk mitigation** - Learn from failures to improve future guard implementations

The progressive loop model ensures that each implementation cycle builds upon previous knowledge, creating an iterative learning process that improves with each execution.

## M. Items That Should Explicitly NOT Be Abstracted Yet

### Reasoning:
1. **Architecture boundaries** - W3, PM-001, PM-002, HC-1070, ZEUS, V0.1-V0.3 must remain unchanged
2. **Hardware-specific differences** - 3090 vs 1070 have different requirements that shouldn't be prematurely unified
3. **Current implementation stability** - Existing logic is working and shouldn't be refactored yet
4. **Evidence-driven abstraction** - Future abstractions should be based on actual patterns, not assumptions

## N. Existing Scripts That Should Be Reused Rather Than Rewritten

### Reusable Components:
1. **gaia_target_preflight/gaia_preflight.py** - Comprehensive system checks
2. **Docker availability functions** - Already implemented in multiple scripts  
3. **Host validation logic** - Generalized host checking utilities
4. **Process execution patterns** - Consistent command execution across scripts

## O. Risks / Ambiguities

### Potential Risks:
1. **Privilege escalation confusion** - Risk of implicit privilege assumptions
2. **Cross-platform compatibility** - Different Linux distributions may have different package managers  
3. **Version compatibility** - Different Docker versions may behave differently
4. **GPU driver conflicts** - Host vs container GPU driver requirements

### Ambiguities:
1. **What constitutes "privileged"** - Clear definition needed for all operations
2. **Bootstrap vs experiment boundary** - When does bootstrap end and experiments begin?
3. **Evidence format consistency** - Need to define common evidence structure
4. **Target profile evolution** - How profiles will evolve over time

## STOP CONDITION

This discovery task is complete. No implementation of the bootstrap framework has been performed, as requested in the steering document.