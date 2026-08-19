# GAIA Local Engineer V0.1.1 — Evidence Discovery

Bounded implementation of the Architect-approved Local Engineer Evidence
Discovery capability.

## Boundary

The implementation provides only:

- `LIST_FILES`
- `SEARCH_TEXT`
- `READ_FILE`
- bounded discovery rounds
- provenance
- evidence-sufficiency separation
- delivery sanitization

It does not provide shell execution, network access, mutation, credential
acquisition, Git mutation, Linear integration, or Toolkit V0.1 changes.

## Discovery root

Every operation requires an explicit authorized `DiscoveryRoot`. The root is
canonicalized and is the containment boundary. Missing or unauthorized root
returns:

`ESCALATE / DISCOVERY_SCOPE_NOT_AUTHORIZED`

## Canonical deterministic test

From the extracted package directory:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -S -m unittest discover -s tests -v
```

The delivery package contains no generated Python bytecode.

## Validation note

The local V0.1.1 suite contains 37 deterministic tests. The frozen GAIA Toolkit V0.1 implementation was separately regression-tested from a clean extracted validation package with its own 19-test suite: 19/19 PASS. No Toolkit source was modified by this revision.
