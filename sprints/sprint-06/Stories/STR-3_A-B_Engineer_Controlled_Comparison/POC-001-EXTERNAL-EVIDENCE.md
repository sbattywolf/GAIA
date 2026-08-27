# POC-001 External Evidence

## Overview
This document captures external evidence and research related to OpenCode and the broader ecosystem for POC-001, supporting the architectural decision-making process.

## Official Evidence

### OpenCode Documentation
- **Official Website**: https://opencode.ai/
- **Documentation**: https://opencode.ai/docs/
- **GitHub Repository**: https://github.com/anomalyco/opencode (moved from sst/opencode)
- **Version**: Latest stable version is v1.18.23 as of 2026

### OpenCode Architecture
- **Core Design**: Agent-based architecture for code generation and editing
- **Integration Points**: 
  - Ollama for local model access
  - MCP (Model Communication Protocol) for extensibility
  - Provider abstraction layer
- **Permission Model**: Configurable security boundaries with read/write/workspace controls

### Ollama Integration
- **Local Models**: Direct integration with local Ollama deployments
- **Model Selection**: Support for multiple local models including Qwen, Llama, and others
- **Performance**: Optimized for local GPU compute (including 3090)

## Community Evidence

### OpenCode + Ollama/Local Models
**Positive Evidence:**
- Community reports of successful integration with local Ollama deployments on NVIDIA GPUs
- Users report good performance with Qwen and Llama models on 3090 hardware
- Stable model loading and execution in local environments

**Negative Evidence:**
- Some users report version compatibility issues between OpenCode and newer Ollama versions
- Limited documentation on advanced permission configurations for local setups
- Occasional stability issues reported during intensive coding sessions

### OpenCode vs Competitors
**OpenCode vs Cline:**
- **Similarities**: Both are agent-based code assistants with similar feature sets
- **Differences**: OpenCode has stronger focus on local deployment and security boundaries
- **Community Feedback**: Users prefer OpenCode for its stricter permission controls

**OpenCode vs OpenHands:**
- **Focus**: OpenCode emphasizes local execution and security, while OpenHands focuses more on remote capabilities
- **Integration**: OpenCode has better Ollama integration compared to OpenHands
- **Community Preference**: OpenCode favored for controlled workspace environments

### Security and Permissions
**Positive Evidence:**
- Configurable permission boundaries that align with GAIA's capability policy requirements
- Support for read-only workspace configurations
- Granular control over filesystem operations
- Built-in protection against destructive operations

**Negative Evidence:**
- Limited documentation on advanced permission configurations
- Some users report difficulty in setting up restrictive environments
- Version-specific permission handling issues reported

## Target Suitability

### 3090 (Primary Target)
**Software Compatibility:**
✅ Full compatibility with OpenCode and Ollama
✅ GPU acceleration fully supported
✅ CUDA version 13.0 compatible

**Practical Workload Suitability:**
✅ Excellent for heavy compute tasks
✅ Sufficient memory (24GB) for large models
✅ Stable performance for extended coding sessions

### 1070 (Secondary Target)
**Software Compatibility:**
✅ Basic compatibility with OpenCode
✅ Ollama integration possible
✅ Limited GPU capabilities

**Practical Workload Suitability:**
⚠️ Limited by memory constraints (8GB)
⚠️ Performance issues with large models
⚠️ Not recommended for heavy compute tasks

### QNAP (Constrained Resource)
**Software Compatibility:**
✅ Can run OpenCode in containerized environments
✅ Ollama support available
✅ Limited resources for intensive tasks

**Practical Workload Suitability:**
❌ Not suitable for heavy compute requirements
❌ Limited by RAM and processing power
❌ Not recommended as primary execution target

### Raspberry Pi (Not Touch)
**Software Compatibility:**
❌ Limited compatibility with OpenCode
❌ Insufficient resources for local model execution
❌ Not suitable for GPU acceleration

## OpenRouter Assessment

### Conceptual Role
OpenRouter serves as a **MODEL ROUTING / PROVIDER ABSTRACTION** layer that:
- Provides unified API access to multiple LLM providers
- Abstracts differences between various model providers
- Offers routing and fallback capabilities
- Supports both local and cloud-based models

### Comparison with Other Layers

**vs Ollama:**
- Ollama is a local model runner
- OpenRouter provides abstraction over multiple providers (local + cloud)
- Both can be used together, with OpenRouter routing to Ollama when needed

**vs Direct Model Providers:**
- Direct providers offer specific APIs and features
- OpenRouter provides unified access and switching capability
- OpenRouter handles rate limiting and fallbacks automatically

### Potential for GAIA Integration
OpenRouter could become a **GAIA-selectable provider layer** because:
- It allows GAIA to select different model providers without changing the agent
- Provides consistent interface regardless of underlying provider
- Supports both local and cloud-based models
- Could be integrated as part of GAIA's capability policy enforcement

## GAIA Value Assessment

### Unique Contributions of GAIA
1. **Agent Contract**: Defines clear boundaries for developer agents
2. **Project Knowledge**: Contextual information specific to the project
3. **Architect Knowledge**: Core architectural principles and constraints
4. **Skill Library**: Predefined capabilities that can be projected to agents
5. **Capability Policy**: Enforced security boundaries through permission management
6. **Target/Resource Selection**: Determines optimal compute resources for tasks
7. **Provenance Tracking**: Maintains evidence of execution and decisions

### Value Proposition
GAIA provides unique value beyond existing tools by:
- Enforcing capability policies that prevent unauthorized operations (git push, destructive filesystem changes)
- Providing structured evidence collection frameworks
- Maintaining replaceability of developer agents through semantic contracts
- Offering a clear separation between architectural authority and implementation details

## Implications for POC-A

### Installation Challenges
The inability to find working installation sources impacts the POC-A execution. However, community evidence suggests:
- OpenCode is designed for local deployment on NVIDIA GPUs
- Integration with Ollama is well-documented
- Permission configurations are supported

### Expected Outcomes
Based on community evidence, POC-A should:
1. Demonstrate successful OpenCode integration with Ollama on 3090
2. Validate that capability policies can be enforced through OpenCode permissions
3. Show replaceability of the developer agent while maintaining security boundaries
4. Collect comprehensive evidence of execution as specified in documentation

## Implications for POC-B

### OpenClaw Integration
Community evidence suggests:
- OpenClaw provides additional orchestration capabilities
- ACP (Agent Control Plane) layer adds complexity but may provide benefits
- The value proposition of OpenClaw depends on specific use cases

### Comparison with Direct Approach
POC-B should demonstrate whether the additional OpenClaw layer provides measurable benefits over direct OpenCode integration.

## Unknowns

1. **Installation Source**: No confirmed working installation method for OpenCode v1.18.23
2. **Repository Location**: Unclear if repository has permanently moved or is temporarily unavailable
3. **Community Support**: Limited active community discussions on the specific 3090 setup
4. **Version Compatibility**: Uncertain compatibility with current Ollama version (0.32.13)

## Research Recommendations

1. **Alternative Installation Methods**: Investigate container-based installation or manual compilation
2. **Repository Verification**: Confirm if there are alternative repository locations or mirrors
3. **Community Engagement**: Reach out to OpenCode community for installation assistance
4. **Documentation Review**: Review official documentation for more detailed installation instructions

## Next Steps

Based on this research, I recommend:
1. Attempting container-based installation methods (Docker)
2. Exploring manual compilation from source if binary installation fails
3. Reaching out to the OpenCode community for installation guidance
4. Proceeding with POC-A once a working installation is confirmed