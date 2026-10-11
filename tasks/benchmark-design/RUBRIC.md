# Task 1 rubric — Benchmark design

**Proposed 100-point rubric, independent of Task 2.** The fixed measurement harness and
engine remain unchanged; no engine speedup is required or scored. Freeze the fixture
matrix, criteria, and runner only after the task's hardware/interface pilot.

## Integrity gates

The suite must run within the fixed interface and declared budget, preserve raw evidence,
and leave the engine, supplied enhanced Pi harness, measurement runner, and organizer
tests/fixtures untouched. Protected paths must have no diff from the immutable starter;
run and report the [integrity check](../../docs/INTEGRITY.md). Candidate suite tests are
editable. Editing timestamps/token evidence,
using fault IDs as answers, fabricating runs, or using extra resources disqualifies.
An incomplete but honest suite receives a review of the implemented portions; missing
work is not silently treated as passing correctness.

## Scoring

| Area | Points | What we evaluate |
| --- | ---: | --- |
| Measurement validity | 30 | Correct TTFT/Etalon/startup definitions; complete output and quality gates; honest token/error accounting; explicit invalid/inconclusive states |
| Discrimination | 25 | Detects meaningful controlled regressions and invalid-fast variants without falsely condemning clean or noisy-but-equivalent controls |
| Statistical design | 20 | Justified workload coverage, repetitions/sample sizes, uncertainty, aggregation, and conclusions appropriate to available evidence |
| Compute efficiency | 15 | Measured launch/warmup/request/drain cost; useful quick/full plans; required evidence fits the run and allocation caps |
| Reproducibility and explanation | 10 | Runnable suite, pinned configs/seeds/source, tests, raw artifacts, and a specific account of limitations |

All three axes must have a substantive evaluation: TTFT, fluidity, and startup.
A single blended “fastness” score with no per-axis results is insufficient.

## Organizer validation matrix

We replay public and held-out events through the candidate evaluator and run selected
workload plans on the fixed engine/controlled variants. The runner passes **unlabeled**
evidence to the suite. The organizer alone owns fault ground truth.

- Delayed prefill should appear in TTFT, not be hidden by fast decode averages.
- Bursts can buffer useful slack; stalls can consume it. Token-level evidence must be
  used rather than treating each chunk as one token or penalizing every burst as bad.
- A readiness response before a completed valid generation must not stop startup timing.
- Wrong/incomplete output, dropped requests, misleading usage, or invalid token timing
  must be rejected rather than awarded an excellent performance score.
- A/A controls and realistic noise should not routinely produce confident regressions.
- Workload/metric parameters should not depend on fixture identity or held-out labels.

Publish the fault families and review criteria. Hidden seeds/severities prevent
memorization; hidden rubric changes do not. The task is not to discover an evaluator
exploit or predict an undisclosed engine name.

## Cost and independence

Proposed official allowance: **4 GPU-hours**. CPU fixture replay is covered by the
published supporting quota; one full on-device suite validation can use up to 3 GPU-hours,
leaving up to 1 for selected targeted probes. This does **not** promise a full GPU run
of every fault variant. Measure this plan in the organizer pilot and amend it before
release if it cannot establish meaningful discrimination.

Task 1 receives its own source/artifact review and score. Its suite does not become the
Task 2 grading benchmark for that candidate, even if both tasks are assigned.
