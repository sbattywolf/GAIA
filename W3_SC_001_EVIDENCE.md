# W3-SC-001 Corrected Implementation Evidence

## Scenario

**W3-SC-001 — Single Home Read**

Concrete Resource: **LIGHT**

Example Resource:

`home.light.living_room`

External Resource Reference:

`light.living_room`

Semantic Capability:

`Read Current Resource State`

Operation: `Read`

Scope: **Exactly one Resource**

Normal Policy: `Allowed`

Normal Approval: `Not Required`

## Correction 1 — Router contract

The W3 Router no longer uses:

- `Callable[[Any], Any] | None`
- `RequestOutcome | Any`
- generic callback routing

Instead, the Router explicitly routes `READ_CURRENT_RESOURCE_STATE` to the
bounded `HomeCollaborator` and returns the explicit bounded union:

`RequestOutcome | ReadCurrentResourceStateOutcome`

The Core-to-Home dependency is explicit and thin. The Home Collaborator no
longer imports or receives the Core `Request` type.

The Home Collaborator receives only:

`ReadCurrentResourceStateRequest`

This is a bounded semantic input type, not a generic callback/provider
mechanism.

## Correction 2 — Policy / Approval matrix

The complete required matrix is represented inside the bounded T01–T10 set:

| Policy | Approval | Expected execution | Evidence test |
|---|---|---:|---|
| Allowed | Not Required | **Yes** | T01 |
| Denied | — | **No** | T09 |
| Indeterminate | — | **No** | T09 |
| ApprovalRequired | Not Granted | **No** | T10 |
| ApprovalRequired | Granted | **Yes** | T10 |

T10 deliberately verifies both sides of the approval boundary without adding a
new public test family.

## Correction 3 — Light boundary

The concrete Resource remains exactly one Light:

`living-room light`

The binding is explicitly composed as:

```text
Read Current Resource State
        ↓
one Light Resource
        ↓
bounded Home-light execution binding
        ↓
Home Assistant
        ↓
source-grounded Light Observation
```

The Home Assistant mapping is explicit:

`home.light.living_room` → `light.living_room`

The externally reported light state is preserved as:

- `ON`
- `OFF`
- `UNAVAILABLE`
- `STALE`

There is no mapping to `OPEN` / `CLOSED`.

`OpeningStateProvider` remains opening-specific. It is not generalized into a
universal provider.

No generic Home Assistant Resource framework or Resource Registry is added.

## T01–T10 final design

| Test | Scenario | Expected boundary evidence |
|---|---|---|
| T01 | Valid Light read | Allowed + Not Required executes exactly one read and returns observed light state |
| T02 | Light / Resource not found | No provider execution; explicit non-success |
| T03 | Malformed Resource Reference | Rejected before transport/provider execution |
| T04 | Home Assistant unavailable | Explicit source-unavailable outcome; no fabricated state |
| T05 | Unexpected external response | Explicit execution failure |
| T06 | Stale/inconsistent response | `STALE` is not presented as current success |
| T07 | Write attempt | Unsupported/rejected; zero provider calls |
| T08 | Out-of-scope request | Unsupported/rejected; no scope expansion |
| T09 | Policy Denied and Indeterminate | Neither executes; zero provider calls |
| T10 | ApprovalRequired without grant and with grant | Without grant: no execution. With grant: exactly one read executes |

## Validation evidence

The corrected implementation was syntax-compiled successfully and the patch
was generated from the verified baseline.

The Human Owner executed the authoritative local W3 test suite:

`python -m pytest -q tests/test_w3_single_home_read.py`

Result:

**T01–T10: PASS (10/10)**

The complete bounded W3 test suite passed locally on the verified checkout.

The local execution confirms the required T01–T10 behavioral boundaries,
including:

- exactly one successful Light read;
- no provider execution for invalid or unavailable cases;
- preservation of source-grounded Light state semantics;
- rejection of write and out-of-scope operations;
- Policy Denied / Indeterminate blocking;
- ApprovalRequired blocking without grant;
- ApprovalRequired execution with explicit grant.

## Architectural conclusion

Pending T01–T10 local execution, the implementation remains within the
approved bounded W3 architecture:

- exactly one Light Resource;
- one bounded Home Collaborator;
- semantic `Read Current Resource State` Capability;
- direct bounded Home-light execution binding;
- explicit Policy/Approval gate;
- read-only external boundary;
- structured outcomes;
- minimal evidence.

No new first-class GAIA concept is introduced.
No Accepted ADR is changed.
No Proposed document is promoted.
No generic provider framework is introduced.

Architectural hypothesis classification remains subject to final review of
the implementation diff and Architect review.
