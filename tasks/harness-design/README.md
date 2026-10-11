# Task 2 — Harness design

**Can you build a loop that makes inference faster and keeps only valid improvements?**

Starting from **bland, stock Pi 1.0** and our ZML/LLMD baseline on one MI355X, build
an unattended optimization harness and submit its best Docker image. **We evaluate the
submitted image offline with a private, black-box benchmark.** Task 1 is not a prerequisite.

> **Draft:** the private evaluator still needs implementation; hardware, source access,
> and resource controls still need validation. See [release status](../../docs/RELEASE_STATUS.md).

## We provide at release

- A pinned engine/model, one isolated GPU, and [setup instructions](../../README.md).
- **Plain Pi 1.0.0**, stock prompt and `read`/`bash`/`edit`/`write` tools, with no supplied
  planner, subagents, custom optimization layer, or automated experiment/keep-revert loop.
- LLMD source/build access and permission to distribute your changes.
- The serving/image interface, resource limits, and API/GPU budget interfaces.
- A protocol smoke client, not the official benchmark or a performance score.

Unlike Task 1, you do **not** get the souped-up agent harness. Start from the isolated
plain profile and build the improvements yourself: orchestration, prompts/tools, experiment
management, measurement policy, and recovery. See the
[supplied harness profiles](../../agent-harness/README.md). Pi's coding model is separate
from the pinned Qwen model served by LLMD.

## Your job

Build this loop:

```text
profile → propose a change → build an image → measure locally → keep or revert → repeat
```

- Base experiments on evidence. Engine, build, packaging, and configuration changes count;
  replacing the serving engine does not.
- Choose your own development workloads, correctness checks, and measurement strategy.
  Measure one experiment at a time and explain your keep/reject decisions.
- Recover from bad builds, startup failures, timeouts, and invalid output without help.
- Log every attempt, including failures, with its change, image digest, results, and cost.
- Stop within budget and return the last image that passed your development checks.

Do not change the baseline lock, model/tokenizer/weights, or host policy. A manually
tuned image alone is not a substitute for the harness.

## Evaluation is black-box and offline

After submission, we independently run the final image on the same pinned model and
hardware. We assess time to first token, streaming smoothness, startup until valid
completed inference, and correctness, alongside harness/build quality.

The official evaluator's implementation, workloads, prompts, arrival schedules, exact
metric definitions, thresholds, weights, and scoring formula are private. There is no
candidate-facing grading CLI, API, benchmark manifest, or live scoring feedback. Your
local measurements are development evidence, not official scores or proof of passing.

**Hint:** read [Etalon §4](https://arxiv.org/html/2407.07000#S4) for ideas about evaluating
streaming inference and fluidity. It is background, not a specification of our hidden
benchmark. Optimize real serving behavior rather than guessing a test trace.

## Keep the supplied baseline pristine

Harness changes belong in `tasks/harness-design/harness/` or a declared Pi 1.0-derived
fork/overlay; engine patches may live in a declared source fork. The supplied baseline,
shared tools, and organizer tests must remain unchanged. Record your Pi base and harness
changes, including baseline/enhanced configurations and transcripts.

Before submission run `python -B -m tools.check_integrity --base takehome-start` and
record its result. See the [integrity warning](../../docs/INTEGRITY.md). This check does
not forbid changes to your own harness or give access to the hidden grader.

## Submit

Work in `tasks/harness-design/`; engine patches may live in a declared source fork.

| Artifact | Contents |
| --- | --- |
| Optimized image | Organizer-accessible `linux/amd64` OCI image by SHA-256 digest |
| Build recipe | Dockerfile, pinned source, patches/config, dependencies, and licenses |
| `harness/` | Runnable loop, development measurement configuration, `program.md` playbook, and `results.tsv` experiment log |
| Evidence and `NOTES.md` | Profiles, raw local measurement reports, decisions, failures, and limitations |
| `submission.json` | Completed [manifest](submission.example.json) matching the submitted image |

We review/replay the harness separately from private performance grading. Correctness,
complete output, honest accounting, and compliance are required. See the
[evaluation overview](RUBRIC.md).

## Time and resources

Proposed: **24–40 hours over two weeks**, **$200 API credit**, and **64 GPU-hours**.
One GPU at a time; reserve the final **8 GPU-hours** for your own validation, final build,
and submission. Budget your development measurements yourself; official evaluation is
organizer-funded after submission. Resources are not yet issued.

Before implementation, read the [harness contract](harness/README.md),
[image contract](../../docs/IMAGE_CONTRACT.md), [black-box evaluation policy](../../docs/BENCHMARK.md),
and [budget policy](../../docs/BUDGETS.md).
