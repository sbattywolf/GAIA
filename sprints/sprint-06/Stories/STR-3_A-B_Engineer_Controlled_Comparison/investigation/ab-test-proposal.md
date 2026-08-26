# STR-3: A/B Controlled Comparison Proposal

## A = 
The current GAIA Engineer implementation as defined in the ING_3090 baseline (referenced in STR-2).

## B = 
An alternative GAIA Engineer implementation using different capabilities/tools but maintaining the same semantic contract from STR-2. This implementation should be selected from among available candidates, not predetermined as OpenClaw.

## What is identical between A and B?
Both implementations must adhere to the four accepted STR-2 clauses:
1. Bounded Scope and Collaboration
2. Explicit Capability Use  
3. Boundary Preservation and Escalation
4. Evidence and Validation Discipline

## What is intentionally different?
- Available capabilities/tools used (this is the primary difference being tested)
- Specific approaches to boundary handling
- Methods for evidence collection and validation
- Implementation details of how semantic obligations are met

## What task/workload will both perform?
A concrete, bounded engineering task that tests the semantic boundaries defined in STR-2:

**Task**: "Analyze a repository structure change and determine whether it impacts existing documentation while maintaining semantic consistency with STR-2 requirements."

This task:
- Requires bounded scope management
- Requires capability use within defined boundaries  
- Requires boundary preservation when encountering ambiguity
- Requires evidence generation and validation

The same task will be performed by both A and B to ensure concrete comparison.

## What authority is given to each?
Both A and B are given identical authority to perform engineering tasks within the GAIA framework, with the same constraints as defined in STR-2. The authority should be sufficient to complete the task while maintaining semantic boundaries.

## What capabilities/tools are available?
Both implementations have access to:
- Standard GAIA tooling and capability set
- The same documentation and reference materials  
- Access to the same repository state
- Same human owner communication channels

## What evidence must each produce?
Each implementation must produce observable behaviors that demonstrate adherence to STR-2 clauses, including:

### Minimum Evidence Package:
- **OBSERVED**: Actual behaviors demonstrated during task execution
- **INFERRED**: Logical conclusions drawn from observed behaviors (must be clearly marked as inference)
- **UNKNOWN**: Scenarios where evidence cannot be obtained through the experiment (must be clearly identified)
- **BLOCKED**: Conditions preventing any evidence collection (must be clearly documented)

## What behaviours will be observed?
1. Response to ambiguous instructions or unclear requirements
2. Handling of boundary condition scenarios  
3. Use of authorized capabilities vs unauthorized inferences
4. Evidence collection and validation approaches
5. Escalation behavior when encountering insurmountable obstacles

## What constitutes:

### PASS
Both implementations demonstrate the same semantic behaviors when evaluated against STR-2 contract, with equivalent evidence quality and completeness.

### FAIL  
The implementations show different approaches to meeting semantic obligations but both remain within acceptable boundaries, resulting in different but valid outcomes that are still consistent with STR-2.

### INSUFFICIENT EVIDENCE
Not enough data available from either implementation to make a determination about semantic equivalence or differences. This could be due to:
- Incomplete task execution
- Ambiguous task definition
- Insufficient evidence collection methods

### BLOCKED
Either implementation is unable to proceed due to missing capabilities, unclear instructions, or other blocking conditions that prevent meaningful comparison.

## Evidence Model Validation
The evidence model must distinguish between:
1. **OBSERVED**: Directly witnessed behaviors during execution
2. **INFERRED**: Logical conclusions from observed behaviors (must be clearly marked)
3. **UNKNOWN**: Scenarios where the experiment cannot provide evidence
4. **BLOCKED**: Conditions that prevent any evidence collection

## Semantic Test Validity
This experiment tests Engineer behavior specifically - how implementations respond to semantic constraints, not model quality, coding performance, or speed.

## Implementation Neutrality
The proposal defines the comparison framework without selecting a specific implementation for B. OpenClaw can be considered as one candidate after the framework is accepted, but the test itself should remain implementation-neutral.

## NEXT GATE:
HUMAN OWNER / ARCHITECT REVIEW

The proposal itself does NOT authorize execution of the A/B experiment.

Execution requires the next explicit authorization.

## Final Note
This proposal defines the framework for a controlled comparison between GAIA Engineer implementations. It is not an execution of the experiment itself, but rather a specification of how such an experiment should be conducted to test the semantic boundaries defined in STR-2.