# Security / Sanitization

Default execution is read-only. Secret values are not collected.
Delivery sanitization rejects Python runtime artifacts, environment/secret files,
and private-key/credential-style artifacts.

SECRET_VALUES_COLLECTED=NO
MUTATION_OPERATIONS=NONE
