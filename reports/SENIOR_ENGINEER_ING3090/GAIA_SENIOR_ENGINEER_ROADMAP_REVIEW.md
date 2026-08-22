# GAIA — Senior Engineer Roadmap Review

## Review of the ING_3090 direction

The proposed progression from engineering validation toward 3090 benchmarking, 1070 verification and eventual Domotics capability is directionally reasonable.

However, the ordering should be tightened.

## Recommended sequence

### Gate A — 1070 physical baseline

Complete and freeze P1→P10.

### Gate B — benchmark baseline

Establish repeatable model/runtime benchmark evidence on the 3090 only after the physical target baseline is known.

### Gate C — comparative model benchmark

If benchmark evidence demonstrates that the current model is limiting the intended task, test another candidate model under the same benchmark contract.

This is preferable to changing models based only on subjective impressions.

### Gate D — 1070 suitability

Only models/capabilities that pass the 3090 benchmark should be considered for 1070 physical verification.

### Gate E — Domotics micro-skill

Validate one bounded Domotics capability at a time.

## Important conclusion

A second model benchmark is a **reasonable future experiment**, not an immediate architectural requirement.

The benchmark should compare models under the same:

- task set;
- prompt/context contract;
- resource constraints;
- timeout rules;
- success criteria;
- evidence format.

No model should be selected solely from general benchmark reputation.
