# Candidate benchmark suite interface (draft)

The suite is **candidate-owned**. The measurement harness is **organizer-owned**.
This directory is a contract/starter, not an implemented benchmark or runner.
The organizer must supply and validate the plan/raw-event schemas before release.

Task 1 also receives the [enhanced Pi 1.0 coding-agent harness](../../../agent-harness/README.md)
for benchmark authoring/debugging. That harness and the trusted measurement runner are
separate, organizer-owned, and read-only. Neither is a candidate deliverable.

## Separation of responsibilities

1. Candidate supplies a versioned declarative workload/measurement plan (`workload.json`).
   It specifies prompts/seeds, arrivals, output policy, warmup, phases, repetitions,
   allowed cache-state requests, and deadlines within the organizer's schema.
2. The **fixed measurement harness** validates that plan, launches the pinned engine,
   applies isolation/cache policy, drives requests, and records immutable raw events.
   Candidate code cannot substitute client timestamps, token identities, or engine output.
3. Candidate `evaluate.py` consumes the captured events and plan, computes the benchmark's
   metrics/gates/comparison, and writes a structured report. The organizer also invokes
   it against held-out event fixtures. This is analysis, not an engine-optimization loop.

Proposed analysis invocation, from the repository root:

```text
python tasks/benchmark-design/suite/evaluate.py \
  --events <organizer-captured-read-only-event-directory> \
  --workload tasks/benchmark-design/suite/workload.json \
  --out <report.json>
```

Candidates implement `evaluate.py` and `workload.json`; neither exists in this draft.
The live fixed-harness invocation and exact JSON schemas remain organizer release work.
Before release, provide both commands, public example plans/events, and a conformance test.
Do not claim the shared `benchmarks.smoke` command is this full interface.

## Required report content

- Suite/config/source identity and referenced raw evidence; no hidden label dependency.
- Planned/offered/completed/failed/unfinished requests per cell/repetition.
- Output/quality validity, independent token counts, completion and client-lag checks.
- TTFT, Etalon fluidity/FTGR, and startup distributions with their populations/deadlines.
- Quick/full mode, cache/warmup state, sample sizes, uncertainty, and comparison decision.
- Explicit `valid`, `invalid`, or `inconclusive` results and reasons. Missing evidence is
  not a perfect score or an empty set of passing gates.
- Measured wall time, allocated GPU-hours, and launch/warmup/drain breakdown.

## Supplied validation evidence

Public fixture families cover bursts, stalls, late first tokens, reasoning channels,
Unicode/token-boundary behavior, missing completion, errors/drops, invalid output,
false usage counts, and misleading readiness. Clean/noisy control fixtures are necessary
for false-positive checks. Real driver/token compatibility is tested by the organizer,
not delegated to the candidate as an extra hidden implementation requirement.

Do not change root `tests/`, supplied harnesses, fixtures, baseline, or shared tools.
Candidate tests belong in this directory's `tests/` subdirectory. Run the
[protected-file integrity check](../../../docs/INTEGRITY.md) before submission; improving
your suite by weakening supplied tests is invalid.

The shared metric primitives may be imported as reference utilities. Workload/gate/SLO
choices remain the candidate's design. Nothing here can alter Task 2's fixed benchmark.
