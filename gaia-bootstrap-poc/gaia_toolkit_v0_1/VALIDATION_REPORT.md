# GAIA Toolkit V0.1 — Validation Report

Canonical clean-extraction test command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m unittest discover -s tests -v
```

Result: PASS

Test output:

```text
Set ARTIFACT_TOOL_RPC_DAEMON_STARTUP_TIMEOUT_S=<seconds> to increase the limit.
test_authorization (test_toolkit.ToolkitTests.test_authorization) ... ok
test_available (test_toolkit.ToolkitTests.test_available) ... ok
test_candidate (test_toolkit.ToolkitTests.test_candidate) ... ok
test_categories (test_toolkit.ToolkitTests.test_categories) ... ok
test_container_not_native (test_toolkit.ToolkitTests.test_container_not_native) ... ok
test_cross_host_semantics (test_toolkit.ToolkitTests.test_cross_host_semantics) ... ok
test_evidence_provenance (test_toolkit.ToolkitTests.test_evidence_provenance) ... ok
test_mapping_provenance (test_toolkit.ToolkitTests.test_mapping_provenance) ... ok
test_no_fuzzy_mapping (test_toolkit.ToolkitTests.test_no_fuzzy_mapping) ... ok
test_no_mutation_by_contract (test_toolkit.ToolkitTests.test_no_mutation_by_contract) ... ok
test_observation (test_toolkit.ToolkitTests.test_observation) ... ok
test_private_key_block (test_toolkit.ToolkitTests.test_private_key_block) ... ok
test_recommendation_not_authorization (test_toolkit.ToolkitTests.test_recommendation_not_authorization) ... ok
test_research_disabled (test_toolkit.ToolkitTests.test_research_disabled) ... ok
test_secret_block (test_toolkit.ToolkitTests.test_secret_block) ... ok
test_security_clean (test_toolkit.ToolkitTests.test_security_clean) ... ok
test_unavailable (test_toolkit.ToolkitTests.test_unavailable) ... ok
test_unknown (test_toolkit.ToolkitTests.test_unknown) ... ok
test_unknown_preserved (test_toolkit.ToolkitTests.test_unknown_preserved) ... ok

----------------------------------------------------------------------
Ran 19 tests in 0.003s

OK

```

Package sanitization: PASS
UNSAFE_PATH_COUNT=0

SECRET_VALUES_COLLECTED=NO
MUTATION_OPERATIONS=NONE

Human Owner validation: PASS
Architect implementation review: ACCEPTED / FROZEN
