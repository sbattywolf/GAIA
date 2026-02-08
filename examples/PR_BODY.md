This PR contains ProjectV2 field-id mapping updates and a proposal for workflow edits.

Files changed:

- `examples/project_field_label_mapping.json` — populated with current field ids and single-select option ids.
- `examples/workflow_edits_proposal.json` — per-workflow proposed edits and mapping from field names to field/option ids.

Why:

- Align project automations and views with concrete field IDs to avoid brittle name-based rules.
- Provide a safe proposal for workflow rule updates that maintain consistent Status/Priority handling.

Next steps (in PR):

1. Review the proposed edits in `examples/workflow_edits_proposal.json`.
2. If acceptable, apply workflow changes via GitHub UI or a CI job with sufficient permissions (detailed changes may require repo owner rights).
3. Optionally create the `Sprint` iteration field by extending `examples/desired_project_fields.json` with `iterationConfiguration` and re-running `scripts/projectv2_ensure.py`.

Signed-off-by: GAIA automation
