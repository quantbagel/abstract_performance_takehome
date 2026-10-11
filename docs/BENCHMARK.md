# Task 2 — Black-box, offline evaluation policy

[Task 2: harness design](../tasks/harness-design/README.md) is evaluated by the organizer
**after submission**, using a private benchmark on the same pinned model and hardware.
The evaluator is frozen before candidates begin, but is not distributed or queryable.

## What candidates know

We care about real serving improvements across:

- **Time to first token:** how long a request waits for its first generated token.
- **Streaming smoothness:** whether generated text arrives at a usable, steady pace.
- **Startup:** time until a fresh server completes valid inference, not just readiness.
- **Correctness and completeness:** fast but wrong, shortened, or dropped output is not
  an improvement.
- **Engineering:** a reproducible image and an honest, bounded optimization loop.

The model, hardware/resource limits, serving ABI, allowed changes, and submission
requirements are public. See the [image contract](IMAGE_CONTRACT.md).

**Hint:** [Etalon §4](https://arxiv.org/html/2407.07000#S4) discusses streaming inference
and fluidity. It is useful background, not a promise that we use its exact implementation,
workloads, parameters, or scoring.

## What remains private

Evaluator source/binaries, prompts and reference answers, workload distributions and
arrival schedules, exact metric/aggregation definitions, thresholds, statistical tests,
weights, and scoring formula are organizer-only. No official quick/full evaluator,
grade-query endpoint, benchmark manifest, or raw grading traces are supplied during the
exercise. The smoke client and shared metric utilities are not the hidden benchmark.

## Development and submission

Candidates choose their own development measurements and correctness checks. The harness
uses those checks for keep/revert decisions and retains raw local reports, including
failures. Local results must be labeled as development evidence, not official scores.
A Task 1 suite may inform local experiments, but cannot replace official Task 2 grading.

Submit one final image by digest with source/build provenance, harness, experiment log,
and notes. We evaluate it independently with the frozen private benchmark and review the
harness separately. There is no mandatory hidden-model stage in this version.

Grading is organizer-funded and offline: no live feedback or iterative grading submissions
while candidates optimize. Any candidate-facing feedback is released only after the cohort
submission deadline; private prompts, reference answers, and raw grading traces remain
private. Infrastructure retries are documented, not a discretionary tuning channel.

No benchmark memorization, request-specific canned answers, hidden truncation, dropped
requests, external inference, or unsupported model/precision substitutions are permitted.
The submitted serving image must run with network egress disabled.

## Task 1 is separate

Task 1 designs its own benchmark using a supplied measurement runner. Its interface and
validation fixtures remain public as specified in that assignment; Task 2's black-box
policy does not make Task 1's measurement runner opaque. Use Etalon and the shared
measurement utilities as background, not an undisclosed Task 2 workload as your design.

**Draft:** the official evaluator still needs implementation and hardware validation.
This policy does not imply that a working grader or candidate-ready release exists.
