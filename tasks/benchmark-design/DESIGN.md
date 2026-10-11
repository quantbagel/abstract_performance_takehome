# Task 1 — Benchmark design report

Replace this template. Reference raw evidence and runnable suite/config/source revisions.

## Evaluation goals and workloads

Which user experiences are covered, what is omitted, and why these lengths/arrival rates?

## Metrics and validity

TTFT, Etalon fluidity/FTGR, startup boundaries, token/population accounting, and quality gates.
Which inputs make the result invalid or inconclusive rather than good or bad?

## Statistical policy

Warmup/cache states, repetitions, uncertainty, aggregation, and meaningful regression thresholds.

## Validation matrix

Public fault/regression fixtures and clean/noisy controls; expected behavior versus observations.
Discuss false positives, false negatives, and limitations without guessing hidden fixture labels.

## Measured compute cost

Quick/full per-phase wall time and allocated GPU-hours, including launch/warmup/drain/cleanup.
Explain why the requested samples fit within the task's allowance and suite-run ceiling.

## Reproducibility

Commands, suite/source/config identities, seeds, raw-event reports, and candidate tests.
Record the supplied enhanced Pi profile/release identity, immutable starter commit,
`tools.check_integrity` result, and the released task validation commands you ran.
Organizer harness/tests/fixtures must be unchanged; suite tests are candidate-owned.

## Effort and resource use

Active hours, task-specific API charges, allocated GPU-hours, CPU build/test use, and cuts.
This task does not require an optimized engine image or optimization harness.
