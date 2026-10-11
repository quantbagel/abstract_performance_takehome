# Task 2 — Candidate optimization harness contract (draft)

You start from the [plain Pi 1.0 profile](../../../agent-harness/README.md), implement
its optimization loop, and choose development measurements. No enhanced Task 1 harness
or prebuilt optimizer is supplied. The main output is an image digest, not a benchmark score. The organizer's official benchmark is private and
runs offline after submission; it is not an input to your harness. `run.py` is intentionally
not a solved optimizer in this starter repository. All paths below are repository-root-relative.

Example candidate-defined invocation:

```text
python tasks/harness-design/harness/run.py \
  --baseline baseline/lock.json \
  --development-benchmark tasks/harness-design/harness/development-benchmark.json \
  --budget-minutes 360 \
  --api-spend-limit-usd 200 \
  --out tasks/harness-design/submission.json \
  --results tasks/harness-design/harness/results.tsv
```

You define the local measurement configuration/schema and implement its invocation.
No organizer benchmark manifest, grader binary, or score endpoint is supplied.
Runtime invocation is a subset of the Task 2 candidate allowance, not an extra grant.
Task 1 credentials/leases cannot extend it.

The organizer supplies credential/balance/lease interfaces before task release. A CLI
flag is not a hard API spend cap. The actual proxy and compute leases enforce limits.

## Required behavior

1. Start from the pinned plain Pi 1.0.0 distribution with isolated task configuration.
   Preserve the supplied baseline; put candidate orchestration/prompts/tools under this
   directory or a declared Pi-derived fork/overlay. Record base identity, enhancements,
   effective tool/resources, transcripts, and coding-model usage. Read model/runtime/budget
   inputs; consult `program.md`, source, profiles, server logs, and raw local measurements. Do not embed benchmark answers or request-specific shortcuts.
2. Establish a measured development baseline, including correctness/completeness checks.
   Keep its image as a recoverable last-good state.
3. Form a hypothesis, save the patch/config, build a fresh candidate image, and resolve
   its digest. Isolate one engine experiment at a time on the assigned GPU.
4. Measure using your own development workloads and checks. Explain the keep/reject
   policy, noise handling, and limitations. Profiles or smoke success alone cannot
   substantiate a performance claim. Local checks do not certify an official grade.
5. Log every attempt, including build errors, startup timeouts, correctness failures,
   reversions, and interrupted runs. Keep the image/log/patch/config artifacts needed for replay.
6. Recover without a human. Terminate child process groups/containers, clean temporary
   state, restore last-good image/config, and continue if time and credits remain.
   Never `git reset --hard` an arbitrary user worktree.
7. Check API balance, lease time, and remaining compute before each experiment. Reserve
   final build/validation/submission time. On exhaustion or SIGTERM return the last image
   that passed your development checks; do not start a run that cannot fit the remaining lease.
8. Write the task-scoped `--out` manifest with `task=harness-design`, final image digest,
   development measurement configuration/evidence, and provenance on exit. Keep source/build
   and manifest synchronized; a launch tag cannot masquerade as a digest.
9. Run the [protected-file integrity check](../../../docs/INTEGRITY.md) against the
   released starter and record the result. Candidate harness diffs are expected; changes
   to supplied infrastructure/tests are not.

No requirement to discover a magic improvement. A reliable bounded loop with honest
negative results is better than fabricated progress or an optimizer that needs rescue.

## Experiment log

`results.tsv` contains one row per attempt. `image_digest` may be empty if the build
failed. `api_usd_cumulative` is reconciled with organizer billing, not model-estimated
spend. `gpu_hours_cumulative` comes from allocation accounting, not utilization.
Missing metrics stay blank, never zero. TSV fields escape tabs/newlines; artifacts keep
full multiline descriptions. Store raw local reports outside this summary table.

Outcome values: `baseline`, `improved`, `no_change`, `regressed`, `gate_failed`, `error`,
`interrupted`. These describe **your development checks only**. `kept` is `1` or `0`;
a kept state must have an image and a passing local validation report.

The `local_ttft_speedup`, `local_ftgr_speedup`, and `local_startup_s` columns are optional
local summaries, not official metrics. If you use them, document their definitions and
workloads in the referenced `development_report`; add clearly named columns for other
local metrics. Retain distributions, repetitions, failures, uncertainty, and measurement
cost in raw reports. There are no official grader reports to attach during development.
