# GAIA Module Extraction Pattern

This document describes the formalized pattern for extracting reusable capabilities from the GAIA framework, based on the successful Module 1 extraction of `inventory_utils.sh`.

## Module Extraction Pattern

The process of extracting a module from GAIA follows these steps:

### 1. Identify Existing Capability
- Locate a self-contained capability within the GAIA framework
- Ensure it has clear inputs/outputs and well-defined behavior  
- Verify it's not tightly coupled to other framework components

### 2. Preserve AS-IS Implementation
- Make no semantic changes to the existing implementation
- Maintain identical behavior and interface
- Keep all comments, structure, and error handling exactly as-is

### 3. Identify Callers and Dependencies
- Document all callers of the capability (e.g., `source` statements)
- Map filesystem dependencies and path assumptions
- Identify configuration and environment requirements  

### 4. Define Capability Contract
- Specify inputs and outputs for each function
- Document error handling behavior  
- Define filesystem contract and dependencies
- Establish portability assumptions

### 5. Extract Without Semantic Changes
- Copy the implementation to a new location (`tools/` directory)
- Maintain identical code structure and formatting
- Do not modify or optimize the implementation

### 6. Validate Independently
- Create test cases that exercise all functionality
- Verify behavioral equivalence with original
- Test error conditions and edge cases

### 7. Compare BEFORE / AFTER
- Execute both implementations with identical inputs
- Confirm identical outputs and exit codes  
- Document any differences found

### 8. Preserve Provenance
- Maintain clear relationship between original and extracted versions
- Keep original as authoritative reference
- Document extraction date and process

### 9. Keep Original Authoritative
- Do not modify the original implementation
- Do not integrate into framework yet
- Maintain both copies for validation

### 10. Decide Separately Whether Integration is Justified
- Evaluate benefits of integration vs. maintenance burden  
- Consider path resolution and framework compatibility
- Make explicit decision about future adoption

## Module Integration Pattern

Module integration involves replacing the original sourcing with the extracted capability:

### Process:
1. Update `source` statements to reference extracted module location
2. Ensure proper path resolution within framework context
3. Verify all existing functionality remains intact  
4. Test integration thoroughly before deployment

## External Adoption Pattern

When evaluating external tools, the process should consider:

### Evaluation Criteria:
- Does an external implementation already exist?
- Can it be adopted without reimplementing?
- What evidence is required for adoption?
- What integration boundary is needed?

## Agent Construction Pattern

Agent construction composes capabilities and runtimes:

### Process:
1. Identify GAIA-owned modules
2. Select appropriate extracted leaf capabilities  
3. Integrate with external software/runtime substrates
4. Apply GAIA governance and semantic requirements
5. Produce a complete GAIA Agent

## Module Builder Responsibility

The future GAIA Module Builder should be capable of determining:

- Is this capability already present in GAIA?
- Can it be extracted?
- Should it remain GAIA-owned? 
- Does an external implementation already exist?
- Should we build or adopt?
- What evidence is required?
- What integration boundary is required?

## Agent Builder Responsibility

The future Agent Builder should consume:

- GAIA-owned modules
- Extracted leaf capabilities  
- External software
- Runtime substrates
- Evidence
- Integration contracts

## Module 1 Lessons

### What Module 1 Proved:
- Capabilities can be cleanly isolated from the framework
- Behavioral equivalence can be maintained during extraction
- The process is repeatable and controlled
- No Git operations or framework changes were required

### What Module 1 Did NOT Prove:
- Integration into the framework is feasible (but not demonstrated)
- The extracted module is ready for production use in framework context  
- Path resolution issues within the framework have been tested

### What Remains Unresolved:
- How path resolution works when integrating into framework
- Whether there are hidden dependencies or assumptions in the framework
- Full integration testing scenarios

### Why Original Authority Remains Unchanged:
- The original remains the authoritative reference implementation
- No behavioral changes were made during extraction  
- Framework stability must be preserved until integration is proven

### What Would Be Required for Integration:
- Path resolution testing within framework context
- Framework compatibility verification  
- Integration testing to ensure no regression

### What Evidence Would Be Required Before Authority Transition:
- Successful integration into framework with identical behavior
- Full regression testing confirming no functionality loss
- Path resolution validation in actual framework execution environment

## GAIA vs External Boundary

The boundary between GAIA-owned capabilities and external runtimes:

### GAIA-Owned:
- Core framework utilities that define GAIA's operational semantics
- Governance and policy enforcement components  
- Framework integration interfaces

### External:
- Runtime substrates like OpenClaw, Docker, Ollama
- Developer tools and plugins
- Domain-specific system integrations

This pattern allows for clear separation while enabling the future builder to evaluate both internal and external options.