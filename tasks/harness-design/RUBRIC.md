# Task 2 — Evaluation overview

**Black-box, offline grading.** We run the submitted image ourselves after submission,
on the same pinned model and hardware, with an independently authored private benchmark.
The evaluator is frozen before the cohort begins. Its exact metrics, thresholds, weights,
statistical tests, and scoring formula are not published.

## Validity first

Correctness, complete output, honest timing/token accounting, resource compliance,
offline serving, and build provenance are required. Wrong answers, shortened generations,
dropped requests, external inference, benchmark memorization, fabricated evidence, or
budget violations cannot earn performance credit.

## What we assess

- Reproducible improvements in first-token latency, streaming smoothness, and startup
  until valid completed inference across unseen workloads on the pinned model.
- An inspectable image, pinned source/build recipe, and attributable changes.
- A runnable Pi 1.0-derived unattended propose/build/measure/keep-or-reject loop,
  starting from the bland supplied profile, with attributable harness enhancements,
  useful local evidence, and bounded failure/budget recovery.
- Honest explanation of bottlenecks, trade-offs, unsuccessful experiments, and limitations.

A runnable optimization harness is required for performance credit. A manually tuned image
alone, or a script that only returns a preselected digest, is not this task. Record the
plain Pi baseline and candidate harness provenance; do not substitute the enhanced Task 1
harness. Supplied infrastructure/tests must pass the protected-file integrity check. Your own
measurement strategy informs your loop; it does not determine the official grade.

We may replay selected development experiments or use test doubles to review the harness
within the published allowance. This is separate from hidden performance evaluation and
does not expose the grader. No mandatory hidden-model optimization stage is part of v1.

## Guidance, not a scoring specification

Read [Etalon §4](https://arxiv.org/html/2407.07000#S4) for useful ideas about streaming
performance. Local proxy metrics and smoke results must not be presented as official
scores. Honest negative results are preferable to an invalid fast image.

See the [black-box evaluation policy](../../docs/BENCHMARK.md) and
[budget policy](../../docs/BUDGETS.md). There is no live grading feedback or iterative
submission oracle; feedback is only released after the cohort deadline.

**Draft:** grading is not active until the relevant [release status](../../docs/RELEASE_STATUS.md)
pass, including implementation, hardware validation, and calibration of the private grader.
