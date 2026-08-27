# POC-001 Evidence Plan

## Overview
This document outlines the structured approach for collecting evidence during POC-001 execution, ensuring comprehensive documentation of both POC-A and POC-B architectures.

## Evidence Categories

### 1. Target Information
- **Hardware**: NVIDIA 3090 specifications and configuration
- **Software**: OS version, kernel version, environment details  
- **Runtime**: Ollama installation details and version
- **Network**: Local network configuration and connectivity

### 2. Software/Version Details
- **OpenCode**: Version, build information, installation method
- **Ollama**: Version, model availability, local runtime status
- **OpenClaw**: Version (if used), installation location, configuration
- **GAIA**: Framework version, E2 implementation details

### 3. Model/Provider Information  
- **AI Models**: Available models in Ollama, provider details
- **Model Selection**: Which model was used for the task
- **Performance Metrics**: Response times, execution duration
- **Quality Indicators**: Accuracy of generated code/output

### 4. Configuration Details
- **OpenCode Configuration**: Permission settings, workspace paths
- **GAIA Configuration**: Semantic contract parameters, capability profiles
- **Environment Variables**: Required and set variables for execution
- **Port Usage**: Network ports used by services

### 5. Skills Used
- **GAIA Skills**: List of skills invoked during the task
- **Skill Mapping**: How GAIA skills were projected to OpenCode capabilities
- **Execution Results**: Success/failure of skill applications
- **Performance Data**: Time and resource usage for each skill

### 6. Knowledge Subset Applied
- **Project Knowledge**: Relevant documentation provided to agent
- **Architect Knowledge**: Core architectural principles applied
- **Knowledge Injection Method**: How knowledge was delivered to OpenCode
- **Relevance Score**: Assessment of knowledge applicability

### 7. Task Execution Details
- **Task Description**: Bounded coding task executed
- **Step-by-Step Execution**: Chronological breakdown of operations
- **Command Sequence**: Exact commands used during execution
- **Tool Usage**: Tools and utilities invoked
- **File Operations**: Files created, modified, or accessed

### 8. Files Changed
- **Modified Files**: List of files changed during task execution  
- **Change Types**: Additions, modifications, deletions
- **Version Control Status**: Git status for changed files (should be clean)
- **Impact Analysis**: Assessment of changes made

### 9. Tests Executed
- **Test Suite**: Which tests were run
- **Test Results**: Pass/fail status and output
- **Execution Time**: Duration of test execution
- **Coverage Metrics**: What parts of code were tested

### 10. Results and Errors
- **Successful Operations**: Tasks completed as expected
- **Failed Operations**: Errors encountered and resolution attempts  
- **Unexpected Behavior**: Unforeseen issues during execution
- **Error Logs**: Detailed error information and stack traces

### 11. Timing and Resources
- **Execution Duration**: Total time for task completion
- **CPU Usage**: Processor utilization during operations
- **Memory Usage**: RAM consumption patterns
- **Storage Usage**: Disk space consumed by the process

### 12. Git Mutation Status
- **Repository State**: Current git status (should be clean)
- **Uncommitted Changes**: Any changes that were not committed
- **Working Directory**: Status of files in working directory
- **Branch Information**: Current branch and upstream status

## Evidence Collection Methods

### Automated Collection
- **Logs**: System and application logs for all components
- **Metrics**: Performance metrics from Ollama, OpenCode, and system
- **Status Checks**: Configuration and status verification scripts
- **Output Capture**: Standard output and error capture from commands

### Manual Documentation
- **Observation Notes**: Direct observations during execution  
- **Configuration Review**: Manual verification of settings
- **Boundary Verification**: Confirmation that architectural boundaries are maintained
- **Comparison Notes**: Observations comparing POC-A vs POC-B

## Evidence Organization

### Structured Format
All evidence will be organized using consistent markdown structures:

```
## Category Name

### Subcategory
- **Key Point 1**: Description and supporting evidence
- **Key Point 2**: Description and supporting evidence  
```

### Version Control
- Each piece of evidence will be timestamped
- Evidence will be grouped by POC variant (A vs B)
- Changes to evidence documentation will be tracked

## Quality Assurance

### Verification Steps
1. **Cross-Reference**: Verify that evidence from different sources aligns
2. **Reproducibility**: Ensure that the same task can produce consistent results  
3. **Boundary Validation**: Confirm architectural boundaries are maintained
4. **Policy Compliance**: Verify all capability policies are followed

### Error Handling
- **Missing Evidence**: Document when evidence cannot be collected
- **Inconsistent Data**: Note discrepancies in collected information
- **Unexpected Results**: Record any findings that contradict expectations
- **Security Concerns**: Flag any potential security issues discovered

## Evidence Review Process

### Pre-Execution
- Confirm all evidence collection tools are available and functional
- Verify that permission settings allow for comprehensive evidence gathering
- Prepare templates for consistent documentation

### During Execution  
- Collect evidence immediately after each phase of the task
- Document any deviations from planned execution
- Maintain real-time updates to evidence database

### Post-Execution
- Review all collected evidence against the original specification
- Validate that all required categories are covered
- Ensure no unauthorized access or operations occurred
- Prepare final evidence summary for comparison between POC-A and POC-B

## Expected Outcomes

The evidence collection will provide:
1. **Architectural Validation**: Confirmation of boundary enforcement in both approaches
2. **Performance Data**: Comparative performance metrics between architectures  
3. **Security Assessment**: Verification that capability policies are maintained
4. **Replaceability Evidence**: Proof that OpenCode remains replaceable
5. **Operational Insights**: Practical understanding of both architectural approaches

This structured approach ensures comprehensive evidence collection that will inform the final decision on OpenClaw value proposition.