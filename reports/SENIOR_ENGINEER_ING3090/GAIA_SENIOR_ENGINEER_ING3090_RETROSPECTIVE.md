# GAIA — ING_3090 Engineering Retrospective

## What ING_3090 got right

The branch found and corrected concrete validation failures instead of hiding them.

The model inventory correction is particularly important because physical evidence must originate from the runtime being tested.

The JSON hardening is also legitimate: evidence generation must not fail because raw hardware/runtime strings contain characters that are unsafe for naïve JSON interpolation.

## What should be improved

### Validation semantics

The pipeline should represent evidence state explicitly and consistently.

### Runtime ownership

The runner, Compose configuration and endpoint assumptions need one coherent contract.

### Evidence provenance

Every observation should make it possible to distinguish:

- observed now;
- inferred;
- historical;
- unavailable;
- not executed.

### Physical proof

Repository code quality is not equivalent to successful physical execution.

## Retrospective lesson

The central lesson is:

> A validation framework is only as trustworthy as the provenance and semantics of the evidence it emits.

That principle should guide the next 1070 run and the later AI Architect retrospective.
