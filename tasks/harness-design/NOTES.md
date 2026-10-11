# Task 2 — Candidate notes

Replace this template. Keep claims tied to raw local measurement artifacts and image digests.
Label all results as development evidence: the official benchmark is private and runs
offline after submission, so no official score or grading report is available here.

## Image and reproducible build

Final digest, source revisions, build commands, runtime/compilation artifacts, and licenses.

## Pi baseline and harness enhancements

Pinned plain Pi 1.0.0 identity, baseline/enhanced configuration, prompts/tools/orchestration,
transcripts, coding-model usage, and attributable changes. Distinguish Pi's coding model
from the serving model. Record the immutable starter commit and protected-file integrity
check result; supplied infrastructure/tests must remain pristine.

## Bottlenecks and hypotheses

Profiles for prefill, streaming under load, and startup. Distinguish client, host, and engine.

## Results

Describe your development workloads, metric definitions, correctness/completeness checks,
baseline/candidate results, repetitions, uncertainty, and measurement cost. Explain why
these proxies are useful and where they may not generalize to unseen workloads.
Exploratory estimates are labeled; no invented scores or omitted failure metrics.

## Optimization loop

Keep/reject policy, budget accounting, crash/timeout recovery, and last-good-state behavior.

## Failed experiments and trade-offs

What did not work, evidence why, and what you reverted. Include limitations we can reproduce.

## Next steps

Prioritized work with another week/month, rather than a list of untested speed claims.

## Effort and resource use

Active human hours, cumulative API charges, allocated GPU-hours, CPU build usage,
benchmark wall time, and what you cut. These quantities are not interchangeable.
