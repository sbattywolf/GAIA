# STR-3: A/B Controlled Comparison Proposal

## A = 
The current GAIA Engineer implementation as defined in the ING_3090 baseline (referenced in STR-2).

## B = 
An alternative GAIA Engineer implementation using different capabilities/tools but maintaining the same semantic contract from STR-2.

## What is identical between A and B?
Both implementations must adhere to the four accepted STR-2 clauses:
1. Bounded Scope and Collaboration
2. Explicit Capability Use  
3. Boundary Preservation and Escalation
4. Evidence and Validation Discipline

## What is intentionally different?
- Available capabilities/tools used
- Specific approaches to boundary handling
- Methods for evidence collection and validation
- Implementation details of how semantic obligations are met

## What task/workload will both perform?
A representative engineering task that requires:
- Bounded scope management
- Capability use within defined boundaries  
- Boundary preservation when encountering ambiguity
- Evidence generation and validation

Example task: "Analyze the implications of a new repository structure change on existing documentation while maintaining semantic consistency with STR-2 requirements."

## What authority is given to each?
Both A and B are given identical authority to perform engineering tasks within the GAIA framework, with the same constraints as defined in STR-2.

## What capabilities/tools are available?
Both implementations have access to:
- Standard GAIA tooling and capability set
- The same documentation and reference materials  
- Access to the same repository state
- Same human owner communication channels

## What evidence must each produce?
Each implementation must produce observable behaviors that demonstrate adherence to STR-2 clauses, including:
- Clear documentation of decision-making processes
- Provenance tracking for all actions taken
- Identification of boundary crossings or violations
- Evidence generation and validation approaches

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
The implementations show different approaches to meeting semantic obligations but both remain within acceptable boundaries, resulting in different but valid outcomes.

### INSUFFICIENT EVIDENCE
Not enough data available from either implementation to make a determination about semantic equivalence or differences.

### BLOCKED
Either implementation is unable to proceed due to missing capabilities, unclear instructions, or other blocking conditions that prevent meaningful comparison.

## Evidence Model

Minimum evidence package required:
- OBSERVED: Actual behaviors demonstrated during task execution
- INFERRED: Logical conclusions drawn from observed behaviors  
- UNKNOWN: Scenarios where evidence cannot be obtained through the experiment
- BLOCKED: Conditions preventing any evidence collection

## NEXT GATE:
HUMAN OWNER / ARCHITECT REVIEW

The proposal itself does NOT authorize execution of the A/B experiment.

Execution requires the next explicit authorization.