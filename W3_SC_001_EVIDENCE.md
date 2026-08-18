## Validation evidence

Human Owner local execution:
`python -m pytest -q tests/test_w3_single_home_read.py`

**T01–T10: PASS (10/10)**

This is the authoritative local test result supplied by the Human Owner.
Static/package validation is separate from local execution.

## Policy / Approval execution boundary

The W3-local `W3ExecutionGate` now executes in the Core `RequestRouter`, before
the `HomeCollaborator` and `ReadCurrentResourceStateCapability` are invoked.

Blocked decisions return directly from the Router:

- `Denied` → zero Capability calls
- `Indeterminate` → zero Capability calls
- `Required + Not Granted` → zero Capability calls

Permitted decisions continue to the bounded Home Collaborator:

- `Allowed + Not Required` → exactly one Capability/provider execution
- `Required + Granted` → exactly one Capability/provider execution

The Capability receives an already-authorized `ReadCurrentResourceStateRequest`
and does not evaluate Policy/Approval semantics.

T09/T10 distinguish Core-gate blocking from Capability rejection by counting
Capability invocations as well as provider calls.

## Validation evidence

Human Owner local execution:
`python -m pytest -q tests/test_w3_single_home_read.py`

**T01–T10: PASS (10/10)**

This is the authoritative local test result supplied by the Human Owner.
The Engineer workspace did not run or replace that local execution.

## Architectural conclusion

The implementation remains within the approved bounded W3 architecture.
No protected ADR was modified, no Proposed document was promoted, and no
generic Policy/Approval or provider framework was introduced.
