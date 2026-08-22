# GAIA 1070 Evidence Handoff Framework — v0.1

Purpose
-------
Small operator-side framework for the physical 1070 target.

It performs, in order:
1. fetch origin/ING_3090;
2. fast-forward the local checkout when safe;
3. verify the expected checkpoint;
4. run the existing GAIA 1070 validation runner;
5. capture runtime evidence;
6. preserve the validation log;
7. collect validation_evidence.json if produced;
8. generate a bounded evidence handoff report;
9. optionally commit and push ONLY the evidence report/artifacts to ING_3090.

Important
---------
- The 1070 is a validation/evidence actor, not an implementation actor.
- No source-code changes are made by this framework.
- It never uses git reset --hard, git clean, rebase, force-push, or git add .
- It refuses to push if the working tree contains tracked modifications.
- Untracked runtime directories are not staged.
- A missing validation_evidence.json is recorded as an evidence failure,
  never converted into PASS.
- The operator may set the expected checkpoint SHA explicitly.

Usage
-----
From the GAIA repository:

  ./gaia_1070_evidence/bin/gaia_1070_evidence_run.sh

Optional exact checkpoint:

  EXPECTED_COMMIT=1aba4ccd02db718c204a134468514926b013a11f \
    ./gaia_1070_evidence/bin/gaia_1070_evidence_run.sh

By default the script fetches origin/ING_3090 and fast-forwards the current
ING_3090 branch when it is safe. It then executes the existing runner.

To allow the evidence handoff report to be committed/pushed:

  PUSH_EVIDENCE=1 ./gaia_1070_evidence/bin/gaia_1070_evidence_run.sh

The push contains only generated evidence/report files under the framework's
evidence/report directories. It never commits source changes.

Output
------
A timestamped run directory is created under:

  gaia_1070_evidence/runs/<UTC_TIMESTAMP>/

The run contains:
- git metadata
- validation log
- validation_evidence.json if produced
- runtime summary
- final evidence handoff report

The framework returns the validation runner's exit code unless a Git safety
condition prevents the run.
