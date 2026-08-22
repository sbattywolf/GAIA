# GAIA — Senior Engineer Model Benchmark Review

## Question

Should ING_3090's roadmap evaluate another model on the 3090 as an additional benchmark?

## Answer

**Yes, conditionally.**

The correct trigger is not “try another model because it may be better.”

The trigger should be:

> establish a controlled baseline first, then test an alternative when the baseline exposes a measurable limitation.

## Minimum benchmark dimensions

- response correctness for the intended task;
- structured-output compliance where applicable;
- latency;
- VRAM/RAM pressure;
- repeatability;
- failure rate;
- context sensitivity;
- tool/capability adherence where relevant.

## Comparison rule

Keep the environment and task contract constant.

Only then is a model comparison meaningful.

## Relationship to 1070

The 3090 should be used for efficient comparative engineering/benchmarking.

The 1070 remains the physical constrained target where suitability must ultimately be verified.

3090 benchmark success is therefore **not** equivalent to 1070 acceptance.

## Recommendation

Do not add a model abstraction platform merely to benchmark two models.

Use the simplest repeatable benchmark mechanism available, and retain the benchmark evidence as a separate engineering artifact.
